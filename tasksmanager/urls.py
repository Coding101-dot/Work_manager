from django.conf.urls import url
from . import views
from tasksmanager.views import Task_delete, Project_delete
from django.views.generic import CreateView, DetailView, UpdateView
from tasksmanager.models import Supervisor, Task, Developer
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


app_name = 'tasksmanager'
urlpatterns = [
    url(r'^$', views.index, name='public_index'),
    url(r'login/$', LoginView.as_view(template_name='tasksmanager/login.html'), name="login"),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^tasks/$', views.tasks, name='tasks'),
    url(r'create_developer/$', login_required(CreateView.as_view(model=Developer, template_name=
        'tasksmanager/create_developer.html', success_url='create_developer', fields='__all__')),
        name='create_developer'),
    url(r'create_project/$', views.create_project, name='create_project'),
    url(r'add_task/$', views.add_task, name='add_task'),
    url(r'create_supervisor/$', login_required(CreateView.as_view(model=Supervisor, template_name=
        'tasksmanager/create_supervisor.html', success_url='create_supervisor', fields='__all__')),
        name='create_supervisor'),
    url(r'^task_detail_(?P<pk>\d+)$', views.task_detail, name="task_detail"),
    url(r'^task_list$', views.task_list, name='task_list'),
    url(r'^update_task_(?P<pk>\d+)$',login_required(UpdateView.as_view(model=Task,
        template_name='tasksmanager/update_task.html', success_url='tasks', fields='__all__')), name="update_task"),
    url(r'task_delete_(?P<pk>\d+)$', Task_delete.as_view(), name="task_delete"),
    url(r'project_delete_(?P<pk>\d+)$', Project_delete.as_view(), name='project_delete'),


    ]
