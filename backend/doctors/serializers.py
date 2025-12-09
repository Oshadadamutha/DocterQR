from rest_framework import serializers
from django.contrib.auth.models import User
from .models import DoctorProfile
from patients.models import Patient, Answer, Question


# -------------------
# User & Doctor
# -------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )
        DoctorProfile.objects.create(user=user)
        return user


# -------------------
# Patients, Questions, Answers
# -------------------
class PatientMiniSerializer(serializers.ModelSerializer):
    """Lite version of Patient for embedding inside Questions"""
    class Meta:
        model = Patient
        fields = ["id", "name"]


class QuestionSerializer(serializers.ModelSerializer):
    # Patients shown with ID + Name (read), and can be written via `patient_ids`
    patients = PatientMiniSerializer(many=True, read_only=True)
    patient_ids = serializers.PrimaryKeyRelatedField(
        source="patients", queryset=Patient.objects.all(), many=True, write_only=True
    )
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "doctor", "patients", "patient_ids"]
        read_only_fields = ["doctor"]


class AnswerSerializer(serializers.ModelSerializer):
    # Return which question this answer belongs to
    question_id = serializers.IntegerField(source="question.id", read_only=True)
    question_text = serializers.CharField(source="question.text", read_only=True)

    class Meta:
        model = Answer
        fields = ["id", "question_id", "question_text", "response", "created_at"]
        read_only_fields = ["created_at"]


class PatientSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "name", "created_at", "answers"]
