# Generated by Django 3.0.1 on 2020-02-02 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200202_2155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='categorys',
        ),
    ]
