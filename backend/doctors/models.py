from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models
import uuid

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_code_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.user.username
