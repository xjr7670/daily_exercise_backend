from django.db import models

# Create your models here.
class iCourse(models.Model):
    today = models.CharField(max_length=8)
    watched = models.CharField(max_length=1000)

    def __str__(self):
        return self.today + ' - ' + self.watched


class Pushup(models.Model):
    today = models.CharField(max_length=8)
    finish_num = models.IntegerField(default=0)

    def __str__(self):
        return self.today + ' - ' + self.finish_num
