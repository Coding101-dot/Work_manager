from django.shortcuts import render
from tasksmanager.models import Project, Task, Supervisor
from django.contrib.auth import logout, login, authenticate
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('tasksmanager:public_index'))


def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('tasksmanager:public_index'))

    context = {'form': form}
    return render(request, 'tasksmanager/register.html', context)



class form_create_project(forms.Form):
    Title = forms.CharField(label='Title', max_length=30)
    Description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    Client = forms.CharField(label='Client', max_length=15)


class form_add_task(forms.ModelForm):

    class Meta:
        model = Task
        exclude = ('Time Elapsed',
                   'User Profile')


class Task_delete(DeleteView):
    model = Task
    template_name = 'tasksmanager/confirm_delete_task.html'
    success_url = 'tasksmanager:tasks'

    def get_success_url(self):
        return reverse(self.success_url)


class Project_delete(DeleteView):
    model = Project
    template_name = 'tasksmanager/confirm_delete_project.html'
    success_url = 'tasksmanager:public_index'

    def get_success_url(self):
        return reverse(self.success_url)


def index(request):
    all_projects = Project.objects.all()
    return render(request, 'tasksmanager/index.html', {'action': "PROJECTS TO COMPLETE",
                                                       'all_projects': all_projects})


def tasks(request):
    all_tasks = Task.objects.all()
    return render(request, 'tasksmanager/tasks.html', {'action': 'Tasks and related projects',

                                                       'all_tasks': all_tasks})

@login_required
def create_project(request):
    if request.POST:
        form = form_create_project(request.POST)
        if form.is_valid():
            title = form.cleaned_data['Title']
            description = form.cleaned_data['Description']
            client = form.cleaned_data['Client']
            new_project = Project(Title=title, Description=description, Client=client)
            new_project.save()
            return HttpResponseRedirect(reverse('tasksmanager:public_index'))
        else:
            return render(request, 'tasksmanager/create_project.html',
                          {'form': form})
    else:
        form = form_create_project()
        return render(request, 'tasksmanager/create_project.html',
                      {'form': form})

@login_required
def add_task(request):
    if len(request.POST) > 0:
        form = form_add_task(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('tasksmanager:public_index'))
        else:
            return render(request, 'tasksmanager/add_task.html',
                          {'form': form})
    else:
        form = form_add_task
        return render(request, 'tasksmanager/add_task.html',
                      {'form': form})


def task_detail(request, pk):
    check_task = Task.objects.filter(id=pk)

    try:
        task = check_task.get()

    except (Task.DoesNotExist, Task.MultipleObjectsReturned):
        return HttpResponseRedirect(reverse('public_empty'))
    else:
        request.session['last_task'] = task.id
        return render(request, 'tasksmanager/task_detail.html', {'object': task})


def task_list(request):
    task_list = Task.objects.all()
    return render(request, 'tasksmanager/task_list.html', {'task_list': task_list})

