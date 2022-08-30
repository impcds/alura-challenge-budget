# Generated by Django 4.1 on 2022-08-29 22:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('budget_api', '0007_despesa_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='despesa',
            name='usuario',
            field=models.ForeignKey(default='auth.User', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
