from django.shortcuts import render, redirect
from .models import Quiz, Question, UserResponse
from datetime import datetime
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import requests 
import json
from django.db.models import Avg,Count
from django.core.paginator import Paginator


# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from .models import Quiz
import re
import google.generativeai as genaiimport
from datetime import date
import google.generativeai as genai
today = date.today()

def fetch_quiz_data(topic, num_questions):
    """Fetch quiz questions from Google Gemini"""
    genai.configure(api_key="AIzaSyAygj8I5_EpaFqww-jMHfK8bKc2Us9yoPM")  # Replace with actual key

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Generate a JSON object with an array of {num_questions} multiple-choice questions on {topic}. "
        "The format should be: {'questions': [{'question': '...', 'options': [3], 'answer': '...', 'explanation': '...'}]}"
    )

    try:
        response = model.generate_content(prompt)
        raw_content = response.text.strip()

        # Clean the content if it's wrapped in ```json ... ``` or similar
        cleaned = re.sub(r"^```(?:json)?|```$", "", raw_content, flags=re.IGNORECASE).strip()

        print("✅ Gemini Response:")
        print(cleaned)

        quiz_json = json.loads(cleaned)
        return quiz_json

    except Exception as e:
        return {"error": str(e)}    
    




# def fetch_quiz_data(topic, num_questions):
#     """Fetch quiz questions from the AI API"""
#     prompt = f"Generate a JSON object with an array of {num_questions} multiple-choice questions on {topic}. The format should be: {{'questions': [{{'question': '...', 'options': [...], 'answer': '...', 'explanation': '...'}}]}}."

#     response = requests.post(   
#         url="https://openrouter.ai/api/v1/chat/completions",
#         headers={
#         "Authorization": "Bearer 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",
#             "Content-Type": "application/json",
#         },
#         data=json.dumps({
#             "model": "deepseek/deepseek-r1-zero:free",
#             "messages": [{"role": "user", "content": prompt}]
#         }),
#     )
    
    
#     response_json = response.json()


#     if "choices" in response_json and response_json["choices"]:
#         quiz_content = response_json["choices"][0].get("message", {}).get("content", "")

#         if quiz_content.startswith("\\boxed{"):
#             quiz_content = quiz_content[6:-1]  # Remove \boxed{ and trailing }
# # Remove markdown code block
#         quiz_content = re.sub(r"^```json\s*|```$", "", quiz_content.strip(), flags=re.MULTILINE)

#         # Fix double curly braces (common LLM mistake)
#         quiz_content = re.sub(r"^\s*{\s*{", "{", quiz_content)
#         quiz_content = re.sub(r"}\s*}\s*$", "}", quiz_content)

#         # Optional: remove extra whitespace or lines
#         quiz_content = quiz_content.strip()

#         print("✅ Cleaned content to parse:")
#         print(quiz_content)
#         try:
#             quiz_json = json.loads(quiz_content) 
#             return quiz_json # Convert string to JSON
#         except json.JSONDecodeError:
#             return {"error": "Request Failed"}
#     else:
#         return {"error": "Service Down"}

@login_required
def create_quiz(request):
    if request.method == "POST":
        topic = request.POST.get("topic", "General Knowledge")
        num_questions = int(request.POST.get("num_questions", "5"))
        
        raw_quiz = fetch_quiz_data(topic, num_questions)

        if "questions" in raw_quiz:
            questions = raw_quiz["questions"]

            # ✅ Save quiz metadata to database
            quiz_obj = Quiz.objects.create(
                user=request.user,
                name=f"{topic} Quiz",
                topic=topic,
                total_questions=len(questions),
                total_marks=len(questions),  # 1 mark per question (customize as needed)
                created_at=today    
            )

            # ✅ Create Question objects with question numbers
            for idx, q in enumerate(questions, start=1):
                Question.objects.create(
                    quiz=quiz_obj,
                    number=idx,  # 👈 Add question number here
                    text=q.get("question", ""),
                    question_type='MCQ',
                    options=q.get("options", []),
                    correct_answer=q.get("answer", ""),
                    explanation=q.get("explanation", "")
                )
            # ✅ Save quiz and metadata to session
            request.session['quiz'] = questions
            request.session['current_q'] = 0
            request.session['quiz_id'] = quiz_obj.id  # store quiz ID for later tracking
            
            # ✅ Clear previous completion flag so new quiz works
            request.session.pop('quiz_completed', None)

            return redirect('quiz_question')
        else:
            return render(request, "quiz_form.html", {
                "error": raw_quiz.get("error", "Something went wrong")
            })

    return render(request, "quiz_form.html")


@login_required
def quiz_question(request):
    quiz = request.session.get('quiz', [])
    current_q = request.session.get('current_q', 0)
    selected_answers = request.session.get('selected_answers', {})

    if request.session.get('quiz_completed'):
        return redirect('dashboard')

    # Save answer from POST
    if request.method == "POST":
        selected_option = request.POST.get('answer')
        if selected_option:
            selected_answers[str(current_q)] = selected_option
            request.session['selected_answers'] = selected_answers

        # Navigation logic
        if 'next' in request.POST:
            current_q = min(current_q + 1, len(quiz) - 1)
        elif 'prev' in request.POST:
            current_q = max(current_q - 1, 0)
        elif "submit" in request.POST:
            score = 0
            total = len(quiz)

            quiz_id = request.session.get("quiz_id")
            try:
                quiz_obj = Quiz.objects.get(id=quiz_id, user=request.user)
            except Quiz.DoesNotExist:
                quiz_obj = None

            for i, q in enumerate(quiz):
                selected = selected_answers.get(str(i))  # User's selected option
                correct_option = q.get("answer")         # Full correct answer like "C) Fuji"
                is_correct = selected == correct_option
                marks = 1 if is_correct else 0
                score += marks

                # Optional: Match the question from DB (assuming exact question text matches)
                db_question = Question.objects.filter(text=q.get("question")).first()

                if quiz_obj and db_question:
                    UserResponse.objects.create(
                        user=request.user,
                        quiz=quiz_obj,
                        question=db_question,
                        selected_answer=selected,
                        is_correct=is_correct,
                        marks_obtained=marks
                    )


            # Save total score
            if quiz_obj:
                quiz_obj.obtained_marks = score
                quiz_obj.save()

            request.session['quiz_completed'] = True  # 🧠 Used to prevent going back

            # ✅ Clear session data
            for key in ['quiz', 'current_q', 'selected_answers', 'quiz_id']:
                request.session.pop(key, None)
   
            request.session['quiz_completed'] = True
            return render(request, "quiz_complete.html", {
                "score": score,
                "total": total,
                "quiz_id": quiz_id,
            })

        request.session['current_q'] = current_q

    question = quiz[current_q] if current_q < len(quiz) else None

    return render(request, "quiz_question.html", {
        "question": question,
        "index": current_q + 1,
        "total": len(quiz),
        "is_first": current_q == 0,
        "is_last": current_q == len(quiz) - 1,
        "selected_answer": selected_answers.get(str(current_q), ""),
    })
    
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz, UserResponse

@login_required
def quiz_report(request, quiz_id):
    # Securely fetch the quiz and ensure it belongs to the logged-in user
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)

    # Fetch all user responses for this quiz
    responses = UserResponse.objects.filter(quiz=quiz, user=request.user).select_related('question')

    # Optional: Ensure old session quiz data is cleared after report is generated
    for key in ['quiz', 'current_q', 'selected_answers', 'quiz_id', 'quiz_completed']:
        request.session.pop(key, None)

    return render(request, "quiz_report.html", {
        "quiz": quiz,
        "responses": responses
    })

   #QUIZ Report 
@login_required
def quiz_report(request, quiz_id):
    # Fetch the quiz and ensure it's associated with the logged-in user
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)

    # Fetch all user responses for this quiz
    responses = UserResponse.objects.filter(quiz=quiz, user=request.user).select_related('question')

    # Calculate the total questions, score, and unanswered questions
    total_questions = quiz.total_questions  # This is directly from the Quiz model
    score = responses.filter(is_correct=True).count()  # Correct answers count

    # Calculate unanswered questions (where selected_answer is either None or "none")
    unanswered = responses.filter(Q(selected_answer__isnull=True) | Q(selected_answer="")).count()
    
    # Calculate the percentage and format it to two decimal places
    percentage = round((score / total_questions) * 100, 2) if total_questions else 0
    
    # incorrect 
    incorrect = total_questions - (score + unanswered)


    # Pass the data to the template
    return render(request, "quiz_report.html", {
        "quiz": quiz,
        "responses": responses,
        "total_questions": total_questions,
        "score": score,
        "unanswered": unanswered,
        "percentage": percentage,
        "incorrect": incorrect,
    })

def quiz_analysis_view(request):
    user = request.user
    quizzes = Quiz.objects.filter(user=user).order_by('-created_at')

    quiz_scores = [quiz.obtained_marks for quiz in quizzes]
    quiz_totals = [quiz.total_marks for quiz in quizzes]

    total_obtained = sum(quiz_scores)
    total_possible = sum(quiz_totals)

    average_score = round((total_obtained / total_possible) * 100, 2) if total_possible > 0 else 0

    # Pie Chart Data
    responses = UserResponse.objects.filter(user=user)
    correct = responses.filter(is_correct=True).count()
    incorrect = responses.filter(is_correct=False).exclude(Q(selected_answer__isnull=True) | Q(selected_answer="")).count()
    unanswered = responses.filter(Q(selected_answer__isnull=True) | Q(selected_answer="")).count()

    chart_data = {
        'Correct': correct,
        'Incorrect': incorrect,
        'Unanswered': unanswered,
    }
    # 🏆 Achievement Badges Logic
    badges = []
    total_quizzes = quizzes.count()

    if total_quizzes >= 5:
        badges.append("Completed 5 Quizzes 🎯")

    if total_quizzes >= 10:
        badges.append("Completed 10 Quizzes 🏅")

    if average_score >= 90:
        badges.append("Top Scorer (90%+) 🥇")

    if correct >= 50:
        badges.append("50+ Correct Answers 📚")

    # ✅ IMPORTANT: Do NOT limit quizzes here
    return render(request, 'Profile.html', {
        "user": user,
        'quiz_scores': quiz_scores,
        'total_quizzes': quizzes.count(),
        'average_score': average_score,
        'chart_data': chart_data,
        'recent_quizzes': quizzes,  # Send ALL quizzes, no slicing here
        'badges': badges,
    })
    
def all_quizzes(request):
    quizzes = Quiz.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(quizzes, 10)  # 10 quizzes per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/all_quizzes.html', {'page_obj': page_obj})
