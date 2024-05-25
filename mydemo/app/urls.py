from django.urls import path
from . import views
urlpatterns = [
    path('', views.demo_app, name='home'),
    path('signup/', views.signup, name='sign-up'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_info, name='account-info'),
    path('api/tasks/', views.TasksListCreationView.as_view(), name='tasks-create'),
    path('api/diary/', views.DiaryListCreationView.as_view(), name='diary-create'),
    path('api/tasks-date/', views.UniqueTasksDateView.as_view(), name='unique-tasks-date'),
    path('api/tasks/<int:pk>', views.TaskRetrieveUpdateDestroy.as_view(), name='tasks-update-destroy'),
    path('api/diary/<int:pk>', views.DiaryRetriveUpdateDestroy.as_view(), name='diary-update-destroy'),
    path('api/tasks/<str:date>', views.TasksByDateView.as_view(), name='tasks-by-date-view'),
    path('tasks/', views.TasksView, name='tasks-view'),
    path('change-completed/', views.ChangeCompleted, name = 'change-completed'),
    path('create-task/', views.createTask, name = 'create-task'),
    path('delete-task/', views.deleteTask, name = 'delete-task'),
    path('diary/', views.DiaryView, name ='diary-view'),
    path('create-diary/', views.createDiary, name = 'create-diary'),
]
