from django.contrib import admin
from .models import Wine, Dish
from .models import RecommendationLog
from .models import Subscriber

admin.site.register(RecommendationLog)
admin.site.register(Wine)
admin.site.register(Dish)
admin.site.register(Subscriber)