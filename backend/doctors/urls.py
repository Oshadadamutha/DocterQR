from django.urls import path
from .views import (
    RegisterView, DoctorMeView, DoctorQRCodeView,
    DoctorQuestionListCreateView, DoctorQuestionDetailView,
    DoctorPatientListView, DoctorPatientAnswersView
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # 🔐 Auth
    path("register/", RegisterView.as_view(), name="doctor-register"),
    path("login/", TokenObtainPairView.as_view(), name="doctor-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="doctor-token-refresh"),

    # 🧑‍⚕️ Doctor profile
    path("me/", DoctorMeView.as_view(), name="doctor-me"),
    path("qr/", DoctorQRCodeView.as_view(), name="doctor-qr"),

    # ❓ Questions
    path("questions/", DoctorQuestionListCreateView.as_view(), name="doctor-questions"),
    path("questions/<int:pk>/", DoctorQuestionDetailView.as_view(), name="doctor-question-detail"),

    # 👩‍⚕️ Patients & Answers
    path("patients/", DoctorPatientListView.as_view(), name="doctor-patients"),
    path("patients/<int:patient_id>/answers/", DoctorPatientAnswersView.as_view(), name="doctor-patient-answers"),
]
