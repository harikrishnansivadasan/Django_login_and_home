from django.db import models

# Create your models here.
class MovieInfo(models.Model):
    mail = models.EmailField(max_length=255)
    password = models.IntegerField(null=True)
    confirm_password = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.year}) ({self.description})"

