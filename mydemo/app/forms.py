from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomerUser, Tasks, Diary


class CustomerUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'address']


class CustomerUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'address']


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['customer','title', 'description', 'isCompleted']
class CreateDiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['customer','title', 'content']
