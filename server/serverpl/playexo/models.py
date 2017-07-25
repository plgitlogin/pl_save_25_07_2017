# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from gitload.models import Strategy, PLTP, PL

from jsonfield import JSONField



class Role(models.Model):
    """ Default role are created at migration. See 'playexo/migrations/xxxx_add_role_data.py'
        If you add a new default role, do not forget to add it to the migration file. """
    ADMINISTRATOR = 'AD'
    INSTRUCTOR = 'IN'
    CONTENT_DEVELOPER = 'CD'
    LEARNER = 'LE'
    OBSERVER = 'OB'
    ROLES = (
        (ADMINISTRATOR, 'Administrateur'),
        (INSTRUCTOR, 'Professeur'),
        (CONTENT_DEVELOPER, 'Concepteur'),
        (LEARNER, 'Élève'),
        (OBSERVER, 'Observeur'),
    )
    
    role = models.CharField(primary_key = True, max_length=2, choices=ROLES, null = False, default=LEARNER)
    
    def __str__(self):
        return self.role
    

class Activity(models.Model):
    id = models.CharField(max_length=30, null=False, default=0)
    name = models.CharField(max_length=200, primary_key=True, null=False)
    strategy = models.ForeignKey(Strategy, null=False)
    pltp = models.ForeignKey(PLTP, null=False)
    
    def __str__(self):
        return self.name


class PLUser(models.Model):
    """ Extends User to add a Role """
    user = models.OneToOneField(User, primary_key = True, on_delete=models.CASCADE, null = False)
    role = models.ManyToManyField(Role)
    activity = models.ManyToManyField(Activity)
    
    def is_admin(self):
        return (ADMINISTRATOR in self.role.all() or self.is_staff or self.is_superuser)
    
    def have_role(self, role):
        return (role in self.role.all())
    
    def set_role(self, role):
        if not self.have_role(role):
            self.role.add(role)
    
    def unset_Role(self, role):
        if self.have_role(role):
            self.role.remove(role)


class Course(models.Model):
    id = models.CharField(max_length=30, primary_key=True, null = False)
    name = models.CharField(max_length=200, null = False)
    label = models.CharField(max_length=20, null = False)
    user = models.ManyToManyField(User)
    activity = models.ManyToManyField(Activity)
    
    def __str__(self):
        return str(self.id)+": ["+self.label+"] "+self.name


class Answer(models.Model):
    STARTED = 'ST'
    FAILED = 'FA'
    SUCCEEDED = 'SU'
    STATE = (
        (STARTED, 'Commencé'),
        (FAILED, 'Echoué'),
        (SUCCEEDED, 'Réussi'),
    )
    
    value = models.TextField(max_length = 50000, null = False)
    user = models.ForeignKey(User, null = False)
    pl = models.ForeignKey(PL, null = False)
    seed = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(null = False, default=timezone.now)
    state = models.CharField(max_length=2, choices=STATE, null = False, default=STARTED)
