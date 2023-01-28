from django.contrib import admin

from calorie.models import UserFood, Food, CalorieProfile


class CalorieProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'max_daily_calorie']
    search_fields = ['user__username']


class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'calorie']
    search_fields = ['name']


class UserFoodAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'meal', 'created_at']
    search_fields = ['user__username', 'food_name']
    list_filter = ['meal']


admin.site.register(CalorieProfile, CalorieProfileAdmin)
admin.site.register(UserFood, UserFoodAdmin)
admin.site.register(Food, FoodAdmin)
