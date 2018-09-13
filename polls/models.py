from django.db import models

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
    def __str__(self):
        return 'Заказчик :' + self.user + ' Товар: ' + self.tovar
