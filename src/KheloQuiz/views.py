from django.shortcuts import render
from Gen_Quiz.models import Quiz,UserResponse
from django.db.models import Avg


def home(request):
    return render(request, 'layouts/welcome_screen.html')  

def generate_quiz(request):
    return render(request, 'generated_quiz.html')  

def about(request):
    return render(request, 'about.html') 

def setting(request):
    return render(request, 'setting.html')

# def profile(request):
#     recent_quizzes = Quiz.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'Profile.html', {'recent_quizzes': recent_quizzes})

# def profile(request):
#     user = request.user
#     quizzes = Quiz.objects.filter(user=user).order_by('-created_at')

#     total_quizzes = quizzes.count()
#     recent_quizzes = quizzes[:5]

#     total_score = 0
#     total_possible = 0
#     correct_answers = 0
#     incorrect_answers = 0
#     unanswered = 0

#     for quiz in quizzes:
#         user_answers = UserAnswer.objects.filter(quiz=quiz)
#         for answer in user_answers:
#             if answer.selected_answer:
#                 if answer.is_correct:
#                     correct_answers += 1
#                     total_score += 1
#                 else:
#                     incorrect_answers += 1
#             else:
#                 unanswered += 1
#             total_possible += 1

#     average_score = round((total_score / total_possible) * 100, 2) if total_possible else 0

#     chart_data = {
#         "Correct": correct_answers,
#         "Incorrect": incorrect_answers,
#         "Unanswered": unanswered,
#     }

#     return render(request, 'Profile.html', {
#         'user': user,
#         'total_quizzes': total_quizzes,
#         'average_score': average_score,
#         'chart_data': chart_data,
#         'recent_quizzes': recent_quizzes,
#     })