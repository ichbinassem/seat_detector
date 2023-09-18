from django.db import models

class QueueEntry(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)  # Assuming codes are unique
