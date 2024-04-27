# Generated by Django 4.2 on 2024-04-27 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField(blank=True, null=True)),
                ('is_enable', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
