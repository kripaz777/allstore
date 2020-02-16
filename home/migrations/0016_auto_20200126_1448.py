# Generated by Django 3.0.2 on 2020-01-26 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20200126_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=200)),
                ('old_price', models.IntegerField()),
                ('price', models.IntegerField()),
                ('brand', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('detail', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('availability', models.CharField(max_length=100)),
                ('for_gender', models.CharField(max_length=100)),
                ('img_product', models.ImageField(upload_to='product')),
            ],
        ),
        migrations.DeleteModel(
            name='product',
        ),
    ]
