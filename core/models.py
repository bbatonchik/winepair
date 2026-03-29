from django.db import models


class Wine(models.Model):
    WINE_TYPES = [
        ('red', 'Красное'),
        ('white', 'Белое'),
        ('sparkling', 'Игристое'),
    ]

class Wine(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20)  # red/white/rosé
    body = models.IntegerField(default=3)
    tannin = models.IntegerField(default=3)
    acidity = models.IntegerField(default=3)
    sweetness = models.IntegerField(default=3)
    price = models.IntegerField(default=1000)  #  добавляем цену
    country = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, blank=True)
    grape = models.CharField(max_length=100, blank=True)
    aroma = models.CharField(max_length=200, blank=True)
    food_pairing = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='wines/', blank=True, null=True)
    type = models.CharField(max_length=20, default='red')

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    main_ingredient = models.CharField(max_length=100)
    sauce_type = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
    
class RecommendationLog(models.Model):
    ingredient = models.CharField(max_length=50)
    sauce = models.CharField(max_length=50)
    budget = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ingredient} - {self.sauce}"
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email