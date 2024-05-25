from rest_framework import serializers

from .models import Tasks, Diary


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = ['id', 'title', 'description', "created_date", 'isCompleted', 'customer']


class DiarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Diary
        fields = ['id', 'title', 'content', 'created_date', 'customer']
