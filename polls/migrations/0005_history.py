# Generated by Django 2.1.1 on 2018-09-12 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('polls', '0004_delete_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(default='user', max_length=100)),
                ('reason', models.CharField(default='reason', max_length=100)),
                ('howmuch', models.IntegerField(default=0, max_length=100)),
            ],
        ),
    ]
