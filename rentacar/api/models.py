from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Cars(models.Model):
    car_model = models.CharField(max_length=200)
    cost = models.IntegerField(null=True)

    def __str__(self):
        return self.car_model

class UserInfo(AbstractUser):
    email = models.EmailField(max_length=200)
    date_of_birth = models.DateField(null=True)
    car_model = models.ForeignKey(Cars, on_delete=models.CASCADE, null=True, blank=True)
    
    

    def __str__(self):
        return self.username
    
class Renting(models.Model):
    car_model = models.ForeignKey(Cars, on_delete=models.CASCADE)
    pick_up_date = models.DateField()
    return_date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Rent {self.id} - {self.car_model}"
    
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.username} : {self.message}'
    
class Rating(models.Model):
    score = models.IntegerField(default=0, 
    
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0),
        ]
    
    )
    car_model = models.ForeignKey(Cars, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rating for {self.car_model} is {self.score}'
    


