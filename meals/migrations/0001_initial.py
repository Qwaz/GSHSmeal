# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('allergy', models.IntegerField()),
                ('favorite_by', models.ManyToManyField(related_name=b'favorites', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('meal_type', models.IntegerField(choices=[(1, '\uc870\uc2dd'), (2, '\uc911\uc2dd'), (3, '\uc11d\uc2dd'), (4, '\uac04\uc2dd')])),
                ('food_from', models.TextField(blank=True)),
                ('kcal', models.FloatField(default=0)),
                ('carbohydrate', models.FloatField(default=0)),
                ('protein', models.FloatField(default=0)),
                ('fat', models.FloatField(default=0)),
                ('vitamin_a', models.FloatField(default=0)),
                ('thiamine', models.FloatField(default=0)),
                ('riboflavin', models.FloatField(default=0)),
                ('vitamin_c', models.FloatField(default=0)),
                ('calcium', models.FloatField(default=0)),
                ('iron', models.FloatField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('food', models.ForeignKey(to='meals.Food')),
                ('meal', models.ForeignKey(to='meals.Meal')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso_year', models.IntegerField()),
                ('iso_week', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='meal',
            name='foods',
            field=models.ManyToManyField(to='meals.Food', through='meals.Menu'),
            preserve_default=True,
        ),
    ]
