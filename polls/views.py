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
def findmax(array):
    maxx = -1
    top_user = {}
    for element in array:
        if int(element.email) > maxx:
            maxx = int(element.email)
            top_user = element
    return top_user
def earncoin(request):
    if request.user.is_authenticated:
        return render(request,'taski.html')
    else:
        return redirect('/')
def EnterPage(request):
    enter = request.POST.get('Enter')
    users = User.objects.all()
    kusers = []
    for user in users:
        if user.has_perm('Superuser status'):
            continue
        kusers.append(user)
    top_users = []
    if users:
        if len(kusers) < 11:
            for i in kusers:
                max = findmax(kusers)
                top_users.append(max)
                kusers.remove(max)
        else:
            for i in range(10):
                max = findmax(kusers)
                top_users.append(max)
                kusers.remove(max)
    if enter:
        if request.user.is_authenticated:
            return redirect('/menu/')
        return redirect('/login/')
    return (render(request,'Enter.html', context={'top':top_users}))
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
        return redirect('/')
def menu(request):
    global kontovar
    if request.user.is_authenticated:
        tovars = Tovar.objects.all()
        lk = request.POST.get('lk')
        for tovar in tovars:
            #k = tovar.name.replace(' ','')
            if request.POST:
                for i in request.POST:
                    l = i
            if request.POST.get(tovar.url):
                kontovar = tovar
                return redirect('/info/')
        if lk:
            return redirect('/perspage/')
        if tovars:
            return render(request, 'MainMenu.html', context = {'curuser':request.user,'tovars':tovars})
        else:
            return render(request, 'MainMenu.html', context={'curuser': request.user, 'tovars': [['Hello']]})
    else:
        return redirect('/')
def lk(request):
    if request.user.is_authenticated:
        ext = request.POST.get('exit')
        if ext:
            logout(request)
            return redirect('/')
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
        return redirect('/')
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
        return redirect('/')
def tasks(request):
    if request.user.is_authenticated and request.user.has_perm('Superuser status'):
        tasks = Task.objects.all()
        taski = []
        for task in tasks:
            if task.owner == request.user.username:
                taski.append(task)
        return render(request,taski)
def adminPan(request):
    if request.user.is_authenticated:
        if request.user.has_perm('Superuser status'):
            panel = request.POST.get('panelcon')
            paneltov = request.POST.get('paneltov')
            paneltask = request.POST.get('paneltask')
            if paneltask:
                return redirect('/task-panel/')
            if paneltov:
                return redirect('/spisok-zakazov/')
            if panel:
                return redirect('/control-users/')
            return render(request,'MainAdmin.html')
        else:
            return HttpResponse('Недостаточно прав')
    else:
        return redirect('/')
def panel(request):
    if request.user.is_authenticated:
        if request.user.has_perm('Superuser status'):
            users = User.objects.all()
            first = request.POST.get('first')
            last = request.POST.get('last')
            gradd = request.POST.get('grade')
            search = request.POST.get('search')
            if search:
                sps = []
                for user in users:
                    if search.lower() in user.first_name.lower():
                        sps.append(user)
                if sps:
                    return render(request, 'AdminPanel.html', context={'users': sps})
            for user in users:
                if request.POST.get(user.username):
                    if request.POST.get('reason') and request.POST.get('pop'):
                        k = int(user.email)
                        k += int(request.POST.get('pop'))
                        user.email = str(k)
                        user.save()
                        h = History(user = user.username,reason=request.POST.get('reason'),howmuch = int(request.POST.get('pop')))
                        h.save()
            if first and last and gradd:
                l = True
                for user in users:
                    if user.first_name == first + ' ' + last:
                        l = False
                if l:
                    password = PasswordGen()
                    if len(users) > 0:
                        print('kllklklk')
                        grd = passwords(userr='student_'+str(len(users)),passw=password,first_n_last=first+' '+last)
                        grd.save()
                        user = User.objects.create_user(username = 'student_'+str(len(users)),password = password,email = '0', first_name = first + ' ' + last, last_name = gradd)
                        user.save()
                        #grd = grade(grad=gradd, username = 'student_'+str(len(users)),password = password,email = '0', first_name = first + ' ' + last, last_name = password)
                        #grd.save()
                    else:
                        grd = passwords(userr='student_1', passw=password, first_n_last=first+' '+last)
                        grd.save()
                        user = User.objects.create_user(username = 'student_1',password = password,email = '0', first_name = first + ' ' + last, last_name = gradd)
                        user.save()
                        #grd = grade(grad=gradd, username = 'student_1',password = password,email = '0', first_name = first + ' ' + last, last_name = password)
                        #grd.save()
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
        return redirect('/')
def PasswordGen():
    passw = ''
    for i in range(10):
        a = random.choice(list('1234567890abcdefghigklmnopqrstuvyxwzABCDEFGHIGKLMNOPQRSTUVYXWZ'))
        passw += a
    return passw