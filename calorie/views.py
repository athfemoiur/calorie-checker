from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView

from calorie.forms import CalorieProfileCreateForm, UserFoodForm
from calorie.models import CalorieProfile, Food, UserFood
import csv

from django.http import HttpResponse


class HomeView(LoginRequiredMixin, DetailView):
    template_name = 'home.html'

    def get_object(self, queryset=None):
        return User.objects.select_related('calorie_profile').annotate(
            calorie_sum=Coalesce(Sum('foods__food__calorie'), 0)).get(
                id=self.request.user.id)


class CalorieProfileCrateView(LoginRequiredMixin, CreateView):
    model = CalorieProfile
    template_name = 'calorie/profile/create.html'
    success_url = reverse_lazy('calorie_profile_detail')
    form_class = CalorieProfileCreateForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CalorieProfileDetailView(LoginRequiredMixin, DetailView):
    model = CalorieProfile
    template_name = 'calorie/profile/detail.html'

    def dispatch(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.filter(user=self.request.user).exists():
            return redirect('calorie_profile_new')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return queryset.get(user=self.request.user)


class CalorieProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CalorieProfile
    template_name = 'calorie/profile/edit.html'
    fields = ['max_daily_calorie']
    success_url = reverse_lazy('calorie_profile_detail')

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset, user=self.request.user)


class FoodListView(ListView):
    model = Food
    template_name = 'food/list.html'
    context_object_name = 'foods'
    ordering = '-calorie'


class FoodCreateView(LoginRequiredMixin, CreateView):
    model = Food
    template_name = 'food/create.html'
    success_url = reverse_lazy('food_list')
    fields = ['name', 'calorie']


class UserFoodListView(LoginRequiredMixin, ListView):
    template_name = 'user_food/list.html'

    def get_queryset(self):
        return UserFood.objects.filter(user=self.request.user).order_by(
            '-created_at').select_related('food')


class UserFoodCreateView(LoginRequiredMixin, CreateView):
    model = UserFood
    template_name = 'user_food/create.html'
    form_class = UserFoodForm
    success_url = reverse_lazy('user_food_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UsersCalorieListView(LoginRequiredMixin, ListView):
    template_name = 'users_calorie_list.html'

    def get_queryset(self):
        return User.objects.select_related('calorie_profile').annotate(
            calorie_sum=Coalesce(Sum('foods__food__calorie'), 0))


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv"'

    writer = csv.writer(response)
    writer.writerow(['Username', 'Max calorie per day', 'Calorie sum'])

    users = User.objects.select_related('calorie_profile').annotate(
        calorie_sum=Coalesce(Sum('foods__food__calorie'), 0)).values_list(
            'username', 'calorie_profile__max_daily_calorie', 'calorie_sum')
    for user in users:
        writer.writerow(user)

    return response
