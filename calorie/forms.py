from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from calorie.models import UserFood, Food, CalorieProfile


class CalorieProfileCreateForm(ModelForm):
    class Meta:
        model = CalorieProfile
        fields = ('max_daily_calorie', )


class UserFoodForm(ModelForm):
    food = forms.ModelChoiceField(
        Food.objects.all(),
        required=False,
        help_text='Choose your food from available options')
    food_name = forms.CharField(
        max_length=256,
        required=False,
        help_text='Add new food, if you can\'t find it in the list')
    calorie = forms.IntegerField(
        required=False,
        help_text='Add new food, if you can\'t find it in the list')

    class Meta:
        model = UserFood
        fields = ('food', 'food_name', 'calorie', 'meal')

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('food') and not (
                cleaned_data.get('food_name') and cleaned_data.get('calorie')):
            raise ValidationError(
                'Choose your food from the list or create your own here')
        if cleaned_data.get('food') and (cleaned_data.get('food_name')
                                         or cleaned_data.get('calorie')):
            raise ValidationError(
                'You can\'t choose a food and crate new food at the same time')
        if cleaned_data.get('food_name') and cleaned_data.get('calorie'):
            food = Food.objects.create(name=cleaned_data.get('food_name'),
                                       calorie=cleaned_data.get('calorie'))
            cleaned_data['food'] = food
        del cleaned_data['food_name']
        del cleaned_data['calorie']
        return cleaned_data
