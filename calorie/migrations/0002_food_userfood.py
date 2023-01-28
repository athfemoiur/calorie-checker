# Generated by Django 3.2 on 2023-01-15 19:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calorie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('calorie', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.CharField(choices=[('b', 'break_fast'), ('l', 'launch'), ('d', 'dinner')], max_length=10)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='calorie.food')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foods', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]