# Generated by Django 2.1.1 on 2018-09-13 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_tovar'),
    ]

    operations = [
        migrations.CreateModel(
            name='zakaz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='user', max_length=100)),
                ('tovar', models.CharField(default='name', max_length=100)),
            ],
        ),
    ]
