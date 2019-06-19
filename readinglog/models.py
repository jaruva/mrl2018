from django.db import models

# Create your models here.
class UserBooks(models.Model):
    #deprecated
    username = models.CharField(max_length=30)
    books_read = models.TextField(null=True)
    
    def __str__(self):
        return self.username

class Meta:
    app_label = 'readinglog'