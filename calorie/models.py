from django.contrib.auth.models import User
from django.db import models


class CalorieProfile(models.Model):
    user = models.OneToOneField(User, related_name='calorie_profile', on_delete=models.CASCADE)
    max_daily_calorie = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.user}_calorie_profile'


class Food(models.Model):
    name = models.CharField(max_length=256)
    calorie = models.PositiveBigIntegerField()

    def __str__(self):
        return f'{self.name}'


class UserFood(models.Model):
    BREAK_FAST = 'break_fast'
    LAUNCH = 'launch'
    DINNER = 'dinner'
    MEAL_CHOICES = (
        ('b', BREAK_FAST),
        ('l', LAUNCH),
        ('d', DINNER),
    )
    user = models.ForeignKey(User, related_name='foods', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, related_name='users', on_delete=models.CASCADE)
    meal = models.CharField(max_length=10, choices=MEAL_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}_{self.food}'
