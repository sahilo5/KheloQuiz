from django.shortcuts import render
from .models import Quiz, Question, UserResponse
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import requests
import json
# Create your views here.

def about_view(request, *args, **kwargs):
    return render(request, "pages/about.html") 


def get_api_response():

    prompt = f"Generate a JSON object containing 5 multiple-choice questions on the topic:"
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": "Bearer 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",
    },
    data=json.dumps({
        "model": "deepseek/deepseek-r1-zero:free",
        "messages": [
        {
            "role": "user",
            "content": prompt
        }
        ],   
    })
    ) 

    return response.json()   
    

# def main():
#     api_response = get_api_response()
#     print(api_response["choices"][0]["message"]["content"])
    


# if __name__ =="__main__":
#     main()

def quiz_view(request):
    quiz_data = None

    if request.method == "POST":
        topic = request.POST.get("topic", "General Knowledge")  # Default topic
        num_questions = request.POST.get("num_questions", "5")  # Default number of questions

        prompt = f"Generate a JSON object containing {num_questions} multiple-choice questions on {topic}."

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
        quiz_data = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

    return render(request, "pages/quiz.html", {"quiz_data": quiz_data})

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
        print(quiz_content)
        try:
            quiz_json = json.loads(quiz_content)  # Convert string to JSON
        except json.JSONDecodeError:
            return JsonResponse({"error": "Failed to parse JSON from API response"}, status=400)
    else:
        return JsonResponse({"error": "Invalid API response structure"}, status=400)

@login_required
def create_quiz(request):
    if request.method == "POST":
        topic = request.POST.get("topic", "General Knowledge")  # Default topic
        num_questions = request.POST.get("num_questions", "5")  # Default number of questions

        quiz_data = fetch_quiz_data(topic, num_questions)
        
        if not quiz_data:
            return JsonResponse({"error": "Failed to fetch quiz data"}, status=400)
        
        # Create a new Quiz instance
        quiz = Quiz.objects.create(
            user=request.user,
            name=f"{topic} Quiz",
            topic=topic,
            total_questions=num_questions,
            total_marks=num_questions  # Assuming 1 mark per question
        )
        
        # Store Questions
        for question_data in quiz_data.get("questions", []):
            # Ensure options is stored as a JSON object
            options = question_data.get("options", [])
           
            if not isinstance(options, list):
                options = []

            # Create Question
            Question.objects.create(
                quiz=quiz,
                text=question_data["question"],
                question_type="Multiple Choice Question",  # Assuming all questions are MCQ
                options=options,  # JSONField must store a valid list
                correct_answer=question_data["answer"],
                explanation=question_data.get("explanation", "")
            )
        
        return JsonResponse({"message": "Quiz created successfully", "quiz_id": quiz.id})
    
    return JsonResponse({"error": "Invalid request method"}, status=405)