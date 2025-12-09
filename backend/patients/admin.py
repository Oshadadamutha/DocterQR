from django.contrib import admin
from .models import Patient, Question, Answer

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "doctor", "created_at")   # ✅ removed qr_code_id
    search_fields = ("name", "doctor__user__username")
    list_filter = ("doctor", "created_at")

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "doctor")

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("patient", "question", "response", "created_at")
