# Generated by Django 3.2.16 on 2024-07-28 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
