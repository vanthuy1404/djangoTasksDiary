from asyncio.windows_events import NULL
from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import responses, Response

from .forms import CustomerUserCreationForm, CreateTaskForm, CreateDiaryForm
from rest_framework import generics
import requests
from .models import Tasks, Diary
from .serializers import TasksSerializer, DiarySerializer


# Create your views here.
def demo_app(request):
    if request.user.is_authenticated:
        return redirect('tasks-view')
    else:
        return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,'Signup successfully')
            return redirect('login')  # Chuyển hướng sau khi đăng ký thành công
    else:
        form = CustomerUserCreationForm()
    return render(request, "signup.html", {'form': form})


# views.py


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Đăng nhập thành công")
            return redirect('home')
        else:
            messages.error(request, 'Tài khoản hoặc mật khẩu không đúng')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def account_info(request):
    if request.user.id:
        user_info = {
            'username': request.user.username,
            'email': request.user.email,
            'address': request.user.address
        }
    else:
        user_info = {
            'username': NULL,
            'email': NULL,
            'address': NULL
        }
    return render(request, "account.html", {"user_info": user_info})


class TasksListCreationView(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer


class TaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    lookup_field = 'pk'


class TasksByDateView(APIView):
    def get(self, request, date, *args, **kwargs):
        tasks = Tasks.objects.filter(created_date=date)
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data)


class UniqueTasksDateView(APIView):
    def get(self, request, *args, **kwargs):
        tasks_date = Tasks.objects.values_list('created_date', flat=True)
        unique_date = list(set(tasks_date))
        return Response(unique_date)


def TasksView(request):
    if request.user.id:
        id_login = request.user.id
        username = request.user.username
    else:
        id_login = 0
        username = NULL
    base_url = "http://127.0.0.1:8000/api/tasks/"
    today = datetime.now().date()
    respone = requests.get(f'{base_url}{today}')
    tasks_list = []
    if respone.status_code == 200:
        tasks_list = respone.json()
    respone2 = requests.get(f'http://127.0.0.1:8000/api/tasks-date/')
    unique_date_list = []
    if respone2.status_code == 200:
        unique_date_list = respone2.json()
    unique_date_list = sorted(unique_date_list, reverse=True)
    history_list = []
    for date in unique_date_list:
        history_dict = {}
        respone3 = requests.get(f'{base_url}{date}')
        if respone3.status_code == 200:
            history_dict['date'] = date
            history_dict['value'] = respone3.json()
            history_list.append(history_dict)

    return render(request, 'tasks.html',
                  {'tasks_list': tasks_list, 'history_list': history_list, 'id_login': id_login, 'username': username})


def ChangeCompleted(request):
    if request.method == 'POST':
        task_id = request.POST.get('id')
        task = get_object_or_404(Tasks, id=task_id)
        task.isCompleted = not task.isCompleted
        task.save()
        return redirect('tasks-view')
    else:
        return HttpResponse("Error")


def createTask(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks-view')
    else:
        form = CreateTaskForm()
    return render(request, 'tasks.html', {'form': form})


def deleteTask(request):
    base_url = "http://127.0.0.1:8000/api/tasks/"
    if request.method == 'POST':
        task_id = request.POST.get("delete_id")
        response = requests.delete(f'{base_url}{task_id}')
        if response.status_code == 204:
            messages.success(request, "Delete successfully")
            return redirect('tasks-view')
        else:
            return HttpResponse("error")


# Diary
class DiaryListCreationView(generics.ListCreateAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer


class DiaryRetriveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Diary.objects.all()
    serializer_class = DiarySerializer
    lookup_field = 'pk'


def DiaryView(request):
    if request.user.id:
        id_login = request.user.id
    else:
        id_login = 0
    base_url = "http://127.0.0.1:8000/api/diary/"
    response = requests.get(base_url)
    if response.status_code == 200:
        diary_list = response.json()
        user_diaries = [diary for diary in diary_list if diary['customer'] == id_login]
        # Sắp xếp các nhật ký theo ngày tạo từ mới nhất đến cũ nhất
        user_diaries = sorted(user_diaries, key=lambda x: x['created_date'], reverse=True)
    else:
        user_diaries = []

    return render(request, 'diary.html', {'diary_list': user_diaries, 'id_login': id_login})
def createDiary(request):
    if request.method == 'POST':
        form = CreateDiaryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary-view')
    else:
        form = CreateDiaryForm()
    return render(request, 'diary.html', {'form': form})
