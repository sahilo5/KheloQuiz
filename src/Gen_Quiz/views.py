from django.shortcuts import render
from .models import Quiz, Question, UserResponse
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import json
import re

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
        topic = request.POST.get("topic", "General Knowledge")  # Default topic
        num_questions = request.POST.get("num_questions", "5")  # Default number of questions

        raw_quiz = fetch_quiz_data(topic, num_questions)

    if "questions" in raw_quiz:
        return render(request, "quiz_form.html", {"quiz": raw_quiz["questions"]})
    else:
        return render(request, "quiz_form.html", {"error": raw_quiz.get("error", "Something went wrong")})  
    
    return render(request, "quiz_form.html")

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
    
    
        