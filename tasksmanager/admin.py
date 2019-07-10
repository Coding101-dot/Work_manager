from django.contrib import admin
from tasksmanager.models import UserProfile, Project, Task, Supervisor, Developer,DeveloperWorkTask

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Supervisor)
admin.site.register(Developer)
admin.site.register(DeveloperWorkTask)
