from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomerUser(AbstractUser):
    address = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)  # Đặt mặc định là False

    def __str__(self):
        return self.username


class Tasks(models.Model):
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=50)
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    isCompleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Diary(models.Model):
    customer = models.ForeignKey(CustomerUser, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_date = models.DateField(auto_now_add=True)
