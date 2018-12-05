from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class History(models.Model):
    user = models.CharField(max_length=100,default = 'user')
    reason = models.CharField(max_length=100,default = 'reason')
    howmuch = models.IntegerField(default = 0)
    def __str__ (self):
        return self.user +'/'+self.reason+'/'+str(self.howmuch)
class Tovar(models.Model):
    name = models.CharField(max_length=100,default = 'name')
    desc = models.CharField(max_length=500,default = 'desc')
    count = models.IntegerField(default = 1)
    url = models.CharField(max_length=500,default = 'url')
    price = models.IntegerField(default = 1)
    def __str__ (self):
        return self.name +'/'+self.desc+'/'+str(self.count) +'/'+self.url+'/'+str(self.price)
class zakaz(models.Model):
    user = models.CharField(max_length=100, default='user')
    tovar = models.CharField(max_length=100, default='name')
    idd = models.CharField(max_length=100, default='id')
    kartinka = models.CharField(max_length=100, default='url')
    def __str__(self):
        return 'Заказчик :' + self.user + ' Товар: ' + self.tovar
class passwords(models.Model):
    passw = models.CharField(max_length=100,default = '9')
    userr = models.CharField(max_length=100, default='user')
    first_n_last = models.CharField(max_length=100, default='user')
    def __str__(self):
        return self.userr + ' ' + self.passw + ' ' + self.first_n_last
class Task(models.Model):
    name = models.CharField(max_length=500, default='boo')
    count = models.IntegerField(default = 1)
    max_users = models.IntegerField(default = 1)
    full_text = models.CharField(max_length=500, default='boo')
    classes = models.CharField(max_length=500, default='dd')
    owner = models.CharField(max_length=500, default='dd')
    kodik = models.CharField(max_length=500, default='dd')
class vending(models.Model):
    casenum = models.CharField(max_length=100, default='1')
    tovname = models.CharField(max_length=500, default='case')
    kod = models.CharField(max_length=500, default='123')