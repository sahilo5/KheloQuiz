from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Quiz Table: Stores quizzes created by users
class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    name = models.CharField(max_length=255, default="Untitled Quiz")  # Name of the Quiz
    topic = models.CharField(max_length=255)
    subtopic = models.CharField(max_length=255, blank=True, null=True)
    total_questions = models.IntegerField(default=3)
    total_marks = models.IntegerField(default=3)
    obtained_marks = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.name} - {self.topic}"

# Question Table: Stores questions for each quiz
class Question(models.Model):
    QUESTION_TYPES = (
        ('MCQ', 'Multiple Choice Question'),
        ('FILL', 'Fill in the Blanks'),
    )

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    number = models.IntegerField()  # ✅ New field for question number
    text = models.TextField()
    question_type = models.CharField(max_length=4, choices=QUESTION_TYPES, default='MCQ')
    options = models.JSONField(blank=True, null=True)
    correct_answer = models.TextField()
    explanation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Q{self.number} in {self.quiz.name}"
# UserResponse Table: Stores user responses for each question
class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="responses")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    selected_answer = models.TextField(blank=True, null=True)  # Stores user's selected answer
    is_correct = models.BooleanField(default=False)
    marks_obtained = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.user.username} for {self.question.text}"

