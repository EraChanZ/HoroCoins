from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , login
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
import random
from polls.models import *
global kontovar
# Create your views here.
def EnterPage(request):
    enter = request.POST.get('Enter')
    if enter:
        return redirect('/login/')
    return (render(request,'Enter.html'))
@csrf_exempt
def loginn(request):
    passw = request.POST.get('pass')
    user = request.POST.get('login')
    if passw and user:
        print('goood')
        user = authenticate(username=user, password=passw)
        if user is not None:
            print('hhhhelllo')
            if user.is_active:
                print('hello')
                login(request, user)
                return redirect('/menu/')
            else:
                print('bliin')
                ...
        else:
            print('kekee')
    return (render(request,'Login.html'))
def info(request):
    global kontovar
    if request.user.is_authenticated:
        buy = request.POST.get('buy')
        if buy:
            if kontovar.count > 0:
                if int(request.user.email) - kontovar.price >= 0:
                    request.user.email = str(int(request.user.email) - kontovar.price)
                    request.user.save()
                    kl = PasswordGen()
                    z = zakaz(user = request.user.first_name, tovar = kontovar.name, idd = kl)
                    z.save()
                    kontovar.count -= 1
                    kontovar.save()
        return render(request,'info.html',context = {'tovar':kontovar})
    else:
        return redirect('/main/')
def menu(request):
    global kontovar
    if request.user.is_authenticated:
        tovars = Tovar.objects.all()
        lk = request.POST.get('lk')
        for tovar in tovars:
            if request.POST.get(tovar.name):
                kontovar = tovar
                return redirect('/info/')
        if lk:
            return redirect('/perspage/')
        if tovars:
            return render(request, 'MainMenu.html', context = {'curuser':request.user,'tovars':tovars})
        else:
            return render(request, 'MainMenu.html', context={'curuser': request.user, 'tovars': [['Hello']]})
    else:
        return redirect('/main/')
def lk(request):
    if request.user.is_authenticated:
        history = History.objects.all()
        zakazs = zakaz.objects.all()
        spisok = []
        for story in history:
            if story.user == request.user.username:
                spisok.append(story)
        kek = []
        for zaz in zakazs:
            if zaz.user == request.user.first_name:
                kek.append(zaz)
        return render(request,'perspage.html',context={'user':request.user,'history':spisok,'zakazs':kek})
    else:
        return redirect('/main/')
def product(request):
    if request.user.is_authenticated:
        if request.user.has_perm('Superuser status'):
            zakazs = zakaz.objects.all()
            for zak in zakazs:
                if request.POST.get(zak.idd):
                    zak.delete()
            return render(request,'Spisok.html',context = {'zakazs':zakazs})
        else:
            return HttpResponse('Недостаточно прав')
    else:
        return redirect('/main/')
def adminPan(request):
    if request.user.is_authenticated:
        if request.user.has_perm('Superuser status'):
            panel = request.POST.get('panelcon')
            paneltov = request.POST.get('paneltov')
            if paneltov:
                return redirect('/spisok-zakazov/')
            if panel:
                return redirect('/control-users/')
            return render(request,'MainAdmin.html')
        else:
            return HttpResponse('Недостаточно прав')
    else:
        return redirect('/main/')
def panel(request):
    if request.user.is_authenticated:
        if request.user.has_perm('Superuser status'):
            users = User.objects.all()
            first = request.POST.get('first')
            last = request.POST.get('last')
            for user in users:
                if request.POST.get(user.username):
                    if request.POST.get('reason') and request.POST.get('pop'):
                        k = int(user.email)
                        k += int(request.POST.get('pop'))
                        user.email = str(k)
                        user.save()
                        h = History(user = user.username,reason=request.POST.get('reason'),howmuch = int(request.POST.get('pop')))
                        h.save()
            if first and last:
                l = True
                for user in users:
                    if user.first_name == first + ' ' + last:
                        l = False
                if l:
                    password = PasswordGen()
                    if len(users) > 1:
                        user = User.objects.create_user(username = 'student_'+str(len(users)),password = password,email = '0', first_name = first + ' ' + last, last_name = password)
                        user.save()
                    else:
                        user = User.objects.create_user(username = 'student_1',password = password,email = '0', first_name = first + ' ' + last, last_name = password)
                        user.save()

            if users:
                nusers = []
                for user in users:
                    if user.has_perm('Superuser status'):
                        pass
                    else:
                        nusers.append(user)
                return render(request, 'AdminPanel.html',context = {'users':nusers})
            else:
                return render(request,'AdminPanel.html',context  = {'users':['Пока нету зарегестрированных юзеров']})
        else:
            return HttpResponse('У вас нет прав доступа')
    else:
        return redirect('/main/')
def PasswordGen():
    passw = ''
    for i in range(10):
        a = random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        passw += a
    return passw