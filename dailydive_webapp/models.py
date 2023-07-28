from django.db import models

# Create your models here.

class solutions(models.Model):
    id = models.AutoField(primary_key=True)
    sentiment = models.CharField(max_length=200)
    solution_title = models.CharField(max_length=200)
    solution_guide = models.CharField(max_length=200)
    img_url = models.CharField(max_length=200)

    def __str__(self):
        return self.sentiment

