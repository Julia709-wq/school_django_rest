from django.contrib import admin
from .models import Lesson, Course


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image',)
    search_fields = ('name', 'link',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image',)
    search_fields = ('name',)

