from django.contrib import admin
from .models import Profile
from .models import Profile, Task, TaskCompletion
from .models import Question

admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(TaskCompletion)
admin.site.register(Question)

# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('title', 'points', 'due_date')

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('question_text', 'task')

# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'points')
