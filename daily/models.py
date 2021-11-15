from django.db import models

# Create your models here.
class iCourse(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    today = models.CharField(max_length=8)
    name = models.CharField(max_length=100)
    watched = models.CharField(max_length=1000)

    def __str__(self):
        return self.name + ' - ' + self.watched

    def __repr__(self):
        return self.name + ' - ' + self.watched


class Pushup(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    today = models.CharField(max_length=8)
    finish_num = models.IntegerField(default=0)

    def __str__(self):
        return self.today + ' - ' + str(self.finish_num)

    def __repr__(self):
        return self.today + ' - ' + str(self.finish_num)

    def __lt__(self, other):
        if not isinstance(other, Pushup):
            raise TypeError('Only compare to Pushup, '
                            'not other type!')
        return self.today < other.today
