from django.db import models


class ToDo(models.Model):

    name = models.CharField(max_length=100)
    due_date = models.DateField()

    def __str__(self):
        return "{} ({})".format(self.name, self.due_date)
