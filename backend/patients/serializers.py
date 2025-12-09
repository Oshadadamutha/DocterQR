from rest_framework import serializers
from .models import Patient, Question, Answer


# -------------------
# Patient
# -------------------
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "name", "doctor", "created_at"]
        read_only_fields = ["doctor", "created_at"]


# -------------------
# Question (for patients)
# -------------------
class QuestionSerializer(serializers.ModelSerializer):
    """
    For patients: only expose id + text of questions assigned to them
    """
    class Meta:
        model = Question
        fields = ["id", "text"]


# -------------------
# Answer (patient responds)
# -------------------
class AnswerSerializer(serializers.ModelSerializer):
    # Show question ID & text when returning
    question_id = serializers.IntegerField(source="question.id", read_only=True)
    question_text = serializers.CharField(source="question.text", read_only=True)

    class Meta:
        model = Answer
        fields = [
            "id",
            "patient",
            "question_id",
            "question_text",
            "response",
            "created_at",
        ]
        read_only_fields = ["created_at"]
