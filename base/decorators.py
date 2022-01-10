from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .models import User, Walpaper


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper_func


filter_dic = {
    'Free': ['Free', ],
    'Low quality': ['Free', 'Low quality', ],
    'Medium quality': ['Free', 'Low quality', 'Medium quality', ],
    'High quality': ['Free', 'Low quality', 'Medium quality', 'High quality', ],
}


def imageSubscriber(view_func):
    def wrapper_func(request, *args, **kwargs):
        document = get_object_or_404(Walpaper, image='images/'+kwargs['file'])
        if request.user.subscribe in filter_dic.keys():
            if not document.subscribe in filter_dic[request.user.subscribe]:
                return HttpResponse('Please subscribe to view this image')
        return view_func(request, *args, **kwargs)
    return wrapper_func
