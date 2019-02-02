from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , login
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
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
        return render(request,'taski.html',context={'balance':request.user.email})
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
def info(request):
    global kontovar
    if request.user.is_authenticated:
        buy = request.POST.get('buy')
        if buy:
            if kontovar.count > 0:
                if int(request.user.profile.balance) - kontovar.price >= 0:
                    request.user.profile.balance = int(request.user.profile.balance) - kontovar.price
                    request.user.save()
                    kl = PasswordGen()
                    z = zakaz(user = request.user.first_name, tovar = kontovar.name, idd = kl, kartinka=kontovar.url)
                    z.save()
                    kontovar.count -= 1
                    kontovar.save()
        return render(request,'info.html',context = {'tovar':kontovar,'balance':request.user.email,'has_perm':request.user.has_perm('Superuser status')})
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
            return render(request, 'MainMenu.html', context = {'curuser':request.user,'tovars':tovars,'has_perm':request.user.has_perm('Superuser status')})
        else:
            return render(request, 'MainMenu.html', context={'curuser': request.user, 'tovars': [['Hello']],'has_perm':request.user.has_perm('Superuser status')})
    else:
        return redirect('/')
def lk(request):
    if request.user.is_authenticated:
        ext = request.POST.get('exit')
        okbtn = request.POST.get('subm')
        if ext:
            logout(request)
            return redirect('/')
        if okbtn:
            fpass = request.POST.get('firspass')
            spass = request.POST.get('confpass')
            print('Its new one '+fpass+'   '+spass)
            if fpass and spass:
                if fpass == spass and len(fpass) > 5:
                    request.user.set_password(fpass)
                    request.user.save()
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
        return render(request,'perspage.html',context={'user':request.user,'history':spisok,'zakazs':kek,'balance':request.user.email,'has_perm':request.user.has_perm('Superuser status')})
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
            zaregat_vseh = request.POST.get('zaregat')
            if zaregat_vseh:
                all_names = open('./templates/Students.txt')
                print(all_names)
                count = len(users)
                for stroka in all_names:
                    count += 1
                    password = PasswordGen()
                    info = [i.strip() for i in stroka.split(',')]
                    print(info)
                    print('-----------------------------------------------------------------------------------------------')
                    if len(users) > 0:
                        try:
                            print('kllklklk')
                            grd = passwords(userr='student_'+str(count),passw=password,first_n_last=info[1])
                            grd.save()
                            user = User.objects.create_user(username = 'student_'+str(count),password = password,email = '0', first_name = info[1], last_name = info[2])
                            user.save()
                        except:
                            pass
                    else:
                        try:
                            grd = passwords(userr='student_1', passw=password, first_n_last=info[1])
                            grd.save()
                            user = User.objects.create_user(username = 'student_1',password = password,email = '0', first_name = info[1], last_name = info[2])
                            user.save()
                        except:
                            pass
            if request.POST.get('zmak'):
                print('zmak')
                clas = request.POST.get('clas')
                howmuch = request.POST.get('howmuch')
                why = request.POST.get('why')
                print(clas,why,howmuch)
                if clas and howmuch and why:
                    for user in users:
                        if str(user.last_name) == str(clas):
                            print('URAAAAA VSE NORM')
                            k = int(user.profile.balance)
                            k += int(howmuch)
                            user.profile.balance = k
                            user.save()
                            h = History(user=user.username, reason=why,howmuch=int(howmuch))
                            h.save()
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
                        k = int(user.profile.balance)
                        k += int(request.POST.get('pop'))
                        user.profile.balance = k
                        user.save()
                        h = History(user = user.username,reason=request.POST.get('reason'),howmuch = int(request.POST.get('pop')))
                        h.save()
                    elif request.POST.get('rsn') and request.POST.get('otn'):
                        k = int(user.profile.balance)
                        k -= int(request.POST.get('otn'))
                        user.profile.balance = k
                        user.save()
                        h = History(user=user.username, reason=request.POST.get('rsn'),howmuch=int('-'+request.POST.get('otn')))
                        h.save()
            if first and last and gradd:
                l = True
                for user in users:
                    if user.first_name == first and user.last_name == last:
                        l = False
                if l:
                    print('keywordkeywordkeywordkeyword   '+gradd)
                    password = PasswordGen()
                    if len(users) > 0:
                        print('kllklklk')
                        grd = passwords(userr='student_'+str(len(users)),passw=password,first_n_last=first+' '+last)
                        grd.save()
                        user = User.objects.create_user(username = 'student_'+str(len(users)),password = password,email = '0', first_name = first , last_name = last)
                        user.profile.balance = 0
                        user.profile.grade=gradd
                        user.save()

                        #grd = grade(grad=gradd, username = 'student_'+str(len(users)),password = password,email = '0', first_name = first + ' ' + last, last_name = password)
                        #grd.save()
                    else:
                        grd = passwords(userr='student_1', passw=password, first_n_last=first+' '+last)
                        grd.save()
                        user = User.objects.create_user(username = 'student_1',password = password,email = '0', first_name = first, last_name = last)
                        user.profile.balance = 0
                        user.profile.grade = gradd
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
def teachpanel(request):
    if request.user.has_perm('Superuser status') and request.user.is_authenticated:
        return render(request,'teacherpanel.html',context={'user': request.user,'has_perm':request.user.has_perm('Superuser status')})
    else:
        return HttpResponse('Недостаточно прав')
def earnpan(request):
    return render(request,'kakzarabotat.html')
def PasswordGen():
    passw = ''
    for i in range(6):
        a = random.choice(list('12345678abcdzABCPRST'))
        passw += a
    return passw