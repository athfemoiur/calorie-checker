from django.urls import path

from calorie.views import HomeView, CalorieProfileDetailView, CalorieProfileCrateView, \
    CalorieProfileUpdateView, FoodListView, FoodCreateView, UserFoodListView, UserFoodCreateView, \
    UsersCalorieListView, export_users_csv

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('calorie/profile/', CalorieProfileDetailView.as_view(), name='calorie_profile_detail'),
    path('calorie/profile/new/', CalorieProfileCrateView.as_view(), name='calorie_profile_new'),
    path('calorie/profile/edit/', CalorieProfileUpdateView.as_view(), name='calorie_profile_edit'),
    path('foods/', FoodListView.as_view(), name='food_list'),
    path('foods/new/', FoodCreateView.as_view(), name='food_new'),
    path('user-foods/', UserFoodListView.as_view(), name='user_food_list'),
    path('user-foods/new/', UserFoodCreateView.as_view(), name='user_food_new'),
    path('users-calorie/', UsersCalorieListView.as_view(), name='users_calorie_list'),
    path('users-calorie/export', export_users_csv, name='users_calorie_list_export'),
]
