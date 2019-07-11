from django.db import models


# Create your models here.


class UserProfile(models.Model):
    Name = models.CharField(max_length=15, name='Name', null=True, default=None, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Phone number",
                             null=True, default=None, blank=True)
    born_date = models.DateField(verbose_name="Born date", null=True,
                                 default=None, blank=True)
    last_connection = models.DateTimeField(verbose_name="Date of last connection", null=True, default=None, blank=True)
    age = models.IntegerField(verbose_name="Age", default=0)

    def __str__(self):
      return self.Name


class Project(models.Model):
    title = models.CharField(max_length=50, name='Title')
    description = models.CharField(max_length=1000, name='Description')
    client = models.CharField(max_length=100, name='Client')

    def __str__(self):
        return self.Title


class Supervisor(UserProfile):
    specialisation = models.CharField(max_length=25, name='Specialisation')


class Developer(UserProfile):
    Supervisor = models.ForeignKey(Supervisor, name='Supervisor', on_delete=models.CASCADE)


class Task(models.Model):
    Title = models.CharField(max_length=50, name='Title')
    description = models.CharField(max_length=1000, name='Description')
    time_elapsed = models.IntegerField(name='Time Elapsed', null=True,
                                       default=None, blank=True)
    importance = models.IntegerField(name='Importance')
    project = models.ForeignKey(Project, name='Project', null=True,
                                default=None, blank=True, on_delete=models.CASCADE)
    app_user = models.ForeignKey(UserProfile, name='UserProfile', on_delete=models.CASCADE)
    developers = models.ManyToManyField(Developer, related_name='developers', through='DeveloperWorkTask')

    def __str__(self):
        return self.Title


class DeveloperWorkTask(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    time_elapsed_dev = models.IntegerField(name='Time Elapsed', null=True, default=None,
                                           blank=True)

