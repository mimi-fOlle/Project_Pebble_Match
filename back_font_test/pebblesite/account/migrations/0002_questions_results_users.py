# Generated by Django 3.2.18 on 2023-02-19 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('questions', models.CharField(max_length=250)),
                ('a_answer', models.CharField(max_length=100)),
                ('b_answer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('results_id', models.AutoField(primary_key=True, serialize=False)),
                ('results_question', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=40)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=60)),
                ('password', models.CharField(max_length=60)),
                ('remaining_pebble', models.CharField(max_length=50)),
            ],
        ),
    ]
