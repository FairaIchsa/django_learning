from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_organiser = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=True)


class Organisation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, blank=True, related_name="leads", on_delete=models.SET_NULL)
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


def post_user_created_signal(sender, instance, created, **kwargs):
    if created and instance.is_organiser:
        Organisation.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)    # post_save - действие после сохранения
