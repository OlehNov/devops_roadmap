# Generated by Django 5.0.6 on 2024-09-26 19:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('glamp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='glamp',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glamp', to=settings.AUTH_USER_MODEL, verbose_name='Власник'),
        ),
        migrations.AddField(
            model_name='attributeglamp',
            name='glamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='glamp.glamp', verbose_name='Glamp'),
        ),
        migrations.AddField(
            model_name='picture',
            name='glamp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='picture', to='glamp.glamp', verbose_name='Glamp'),
        ),
        migrations.AddField(
            model_name='glamp',
            name='type_glamp',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='glamp', to='glamp.typeglamp', verbose_name='Тип Глемпу'),
        ),
    ]
