from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    """
    null=True -> Es obligatiorio para la base de datos
    blank=True -> Es opcional para el administrador
    """
    date_completed = models.DateTimeField(null=True, blank = True)
    importannt = models.BooleanField(default=False)
    user_owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + '- by '+ self.user_owner.username
    
    