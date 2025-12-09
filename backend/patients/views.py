from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Patient, Question, Answer
from doctors.models import DoctorProfile
from .serializers import QuestionSerializer, AnswerSerializer, PatientSerializer


# -------------------
# Patient Endpoints
# -------------------

# Manual patient creation (doctor logged in)
class PatientCreateView(generics.CreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        doctor = self.request.user.doctorprofile
        serializer.save(doctor=doctor)


# Patient registers via Doctor's QR (public)
class PatientRegisterByQRView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, doctor_qr):
        doctor = get_object_or_404(DoctorProfile, qr_code_id=doctor_qr)
        name = request.data.get("name")
        if not name:
            return Response({"error": "Patient name is required"}, status=status.HTTP_400_BAD_REQUEST)

        patient = Patient.objects.create(doctor=doctor, name=name)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# GET questions for a specific patient (only those assigned)
class PatientQuestionsView(APIView):
    def get(self, request, doctor_qr, patient_id):
        doctor = get_object_or_404(DoctorProfile, qr_code_id=doctor_qr)
        patient = get_object_or_404(Patient, id=patient_id, doctor=doctor)

        # ✅ Only return questions assigned to this patient
        questions = Question.objects.filter(patients=patient, doctor=doctor)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)



# POST answers for a patient
class PatientAnswersView(APIView):
    def post(self, request, doctor_qr, patient_id):
        doctor = get_object_or_404(DoctorProfile, qr_code_id=doctor_qr)
        patient = get_object_or_404(Patient, id=patient_id, doctor=doctor)

        answers_data = request.data  # {question_id: "response"}
        for q_id, response in answers_data.items():
            question = get_object_or_404(Question, id=q_id, doctor=doctor, patients=patient)
            Answer.objects.create(
                patient=patient,
                question=question,
                response=response
            )

        return Response({"message": "Answers submitted successfully"}, status=201)



# Doctor can see their patients (patient-side listing for admin view if needed)
class PatientListView(generics.ListAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(doctor__user=self.request.user)
