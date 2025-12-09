from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserSerializer, RegisterSerializer,
    PatientSerializer, AnswerSerializer, QuestionSerializer
)
from .models import DoctorProfile
import qrcode, io, base64

# Import related models
from patients.models import Patient, Question, Answer
from django.conf import settings

# ------------------------
# Doctor Auth & Profile
# ------------------------
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class DoctorMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor = DoctorProfile.objects.get(user=request.user)
        return Response({
            "id": doctor.user.id,
            "username": doctor.user.username,
            "email": doctor.user.email,
            "qr_code_id": str(doctor.qr_code_id),
        })


class DoctorQRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor = DoctorProfile.objects.get(user=request.user)

        # Generate link-based QR (🌐 change here)
        from django.conf import settings
        qr_data = f"{settings.FRONTEND_URL}/patient/register/{doctor.qr_code_id}"

        qr = qrcode.make(qr_data)
        buffer = io.BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return Response({
            "doctor_id": doctor.user.id,
            "qr_code_id": str(doctor.qr_code_id),
            "qr_link": qr_data,  # optional: add this field for reference
            "qr_image": f"data:image/png;base64,{qr_base64}"
        })


# ------------------------
# Doctor Question Management
# ------------------------
class DoctorQuestionListCreateView(generics.ListCreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(doctor=self.request.user.doctorprofile)

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user.doctorprofile)


class DoctorQuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Question.objects.filter(doctor=self.request.user.doctorprofile)


# ------------------------
# Doctor Patients & Answers
# ------------------------
class DoctorPatientListView(generics.ListAPIView):
    """List all patients under a doctor"""
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(doctor=self.request.user.doctorprofile)


class DoctorPatientAnswersView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_id = self.kwargs["patient_id"]
        return Answer.objects.filter(
            patient__doctor=self.request.user.doctorprofile,
            patient__id=patient_id
        )
