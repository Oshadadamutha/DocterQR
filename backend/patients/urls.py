from django.urls import path
from .views import (
    PatientQuestionsView,
    PatientAnswersView,
    PatientListView,
    PatientRegisterByQRView,
    PatientCreateView,
)

urlpatterns = [
    # 📋 Patients list for doctor (manage patients)
    path("", PatientListView.as_view(), name="patient-list"),

    # 🏥 Doctor manually creates patient
    path("create/", PatientCreateView.as_view(), name="patient-create"),

    # 🔗 Patient registers via doctor QR
    path("register/<uuid:doctor_qr>/", PatientRegisterByQRView.as_view(), name="patient-register-qr"),

    # ❓ Patient fetching questions
    path("<uuid:doctor_qr>/<int:patient_id>/questions/", PatientQuestionsView.as_view(), name="patient-questions"),

    # 📝 Patient submitting answers
    path("<uuid:doctor_qr>/<int:patient_id>/answers/", PatientAnswersView.as_view(), name="patient-answers"),
]
