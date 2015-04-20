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
            name='Ignore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref_user_id', models.ForeignKey(related_name='ref_user_id', to=settings.AUTH_USER_MODEL)),
                ('user_id', models.ForeignKey(related_name='user_id', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('place', models.CharField(max_length=30)),
                ('desc', models.CharField(max_length=300)),
                ('tags', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=10)),
                ('rq_ppl', models.IntegerField(default=1)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('deadline', models.DateTimeField(null=True, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('desc', models.CharField(max_length=300)),
                ('served_ppl', models.IntegerField(default=1)),
                ('status', models.CharField(max_length=10)),
                ('slug', models.SlugField(unique=True)),
                ('problem_id', models.ForeignKey(to='problems.Problem')),
                ('user_id', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(default=b'profile_images/default.png', upload_to=b'profile_images', blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
