# Generated by Django 2.1.1 on 2018-09-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_tovar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='howmuch',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tovar',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='tovar',
            name='price',
            field=models.IntegerField(default=1),
        ),
    ]