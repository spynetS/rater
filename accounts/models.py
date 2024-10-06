from django.contrib.auth.forms import User
from django.db import models

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="accounts")
    theme = models.TextField(default="")

    friends = models.ManyToManyField(to='self', related_name='friends')

    def __str__(self):
        return self.user.username
