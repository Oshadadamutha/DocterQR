from django.db import models
from doctors.models import DoctorProfile


class Patient(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="patients"
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.doctor.user.username})"


class Question(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="questions"
    )
    text = models.CharField(max_length=255)
    patients = models.ManyToManyField("Patient", blank=True, related_name="questions")

    def __str__(self):
        return self.text


class Answer(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.text} by {self.patient.name}"
