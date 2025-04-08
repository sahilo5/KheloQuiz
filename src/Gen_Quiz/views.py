from django.shortcuts import render, redirect
from .models import Quiz, Question, UserResponse
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import json
import re
from datetime import date
today = date.today()

def fetch_quiz_data(topic, num_questions):
    """Fetch quiz questions from the AI API"""
    prompt = f"Generate a JSON object with an array of {num_questions} multiple-choice questions on {topic}. The format should be: {{'questions': [{{'question': '...', 'options': [...], 'answer': '...', 'explanation': '...'}}]}}."

    response = requests.post(   
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
        "Authorization": "Bearer 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",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-zero:free",
            "messages": [{"role": "user", "content": prompt}]
        }),
    )
    
    
    response_json = response.json()

    if "choices" in response_json and response_json["choices"]:
        quiz_content = response_json["choices"][0].get("message", {}).get("content", "")

        if quiz_content.startswith("\\boxed{"):
            quiz_content = quiz_content[6:-1]  # Remove \boxed{ and trailing }
# Remove markdown code block
        quiz_content = re.sub(r"^```json\s*|```$", "", quiz_content.strip(), flags=re.MULTILINE)

        # Fix double curly braces (common LLM mistake)
        quiz_content = re.sub(r"^\s*{\s*{", "{", quiz_content)
        quiz_content = re.sub(r"}\s*}\s*$", "}", quiz_content)

        # Optional: remove extra whitespace or lines
        quiz_content = quiz_content.strip()

        print("✅ Cleaned content to parse:")
        print(quiz_content)
        try:
            quiz_json = json.loads(quiz_content) 
            return quiz_json # Convert string to JSON
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON from API response"}
    else:
        return {"error": "Invalid API response structure"}

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

    if current_q >= len(quiz):
        return render(request, "quiz_complete.html")  # or redirect to summary

    question = quiz[current_q]

    if request.method == "POST":
        # Save user response if needed here
        request.session['current_q'] = current_q + 1
        return redirect('quiz_question')

    return render(request, "quiz_question.html", {
        "question": question,
        "index": current_q + 1,
        "total": len(quiz)
    })
    #     if not quiz_data:
    #         return JsonResponse({"error": "Failed to fetch quiz data"}, status=400)
        
    #     # Create a new Quiz instance
    #     quiz = Quiz.objects.create(
    #         user=request.user,
    #         name=f"{topic} Quiz",
    #         topic=topic,
    #         total_questions=num_questions,
    #         total_marks=num_questions  # Assuming 1 mark per question
    #     )
        
        
    #     # Store Questions
    #     for question_data in quiz_data.get("questions", []):
    #         # Ensure options is stored as a JSON object
    #         options = question_data.get("options", [])
           
    #         if not isinstance(options, list):
    #             options = []
    #         print(options)
    #         # Create Question
    #         Question.objects.create(
    #             quiz_id=quiz.id,
    #             text=question_data["question"],
    #             question_type="MCQ",  # Assuming all questions are MCQ
    #             options=options,  # JSONField must store a valid list
    #             correct_answer=question_data["answer"],
    #             explanation=question_data.get("explanation", "")
    #         )
        
    #     return JsonResponse({"message": "Quiz created successfully", "quiz_id": quiz.id})
    
    # return JsonResponse({"error": "Invalid request method"}, status=405)
    
    
        