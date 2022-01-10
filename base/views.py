from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, FileResponse
import os
from .decorators import unauthenticated_user, imageSubscriber


from .models import User, Walpaper


def getwallpaper(request):
    walpapers = Walpaper.objects.all()
    filter_dic = {
        'Free': ['Free', ],
        'Low quality': ['Free', 'Low quality', ],
        'Medium quality': ['Free', 'Low quality', 'Medium quality', ],
        'High quality': ['Free', 'Low quality', 'Medium quality', 'High quality', ],
    }
    if request.user.subscribe in filter_dic.keys():
        walpapers = walpapers.filter(
            subscribe__in=filter_dic[request.user.subscribe])

    return walpapers


@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    walpapers = getwallpaper(request)
    context = {
        'user': request.user,
        'walpapers': walpapers
    }
    return render(request, 'base/index.html', context)


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
        else:
            print('some one try to login and failed')
            print(f'username:{email} and password : {password}')
            return HttpResponse('invalid user details supplied')
    return render(request, 'base/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
@imageSubscriber
def MediaSecurityCheck(request, file_type, file):
    document = get_object_or_404(Walpaper, image='images/'+file)
    path, file_name = os.path.split(file)
    # print('hieieiei')
    response = FileResponse(document.image)
    return response
