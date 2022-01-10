# MediaSubscription

## models.py

```
from django.db import models
from django.core.validators import FileExtensionValidator

class Walpaper(models.Model):
    """Database model for wallpapers"""
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images', validators=[
                              FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    CATEGORY = (
        ('Free', 'Free'),
        ('Low quality', 'Low quality'),
        ('Medium quality', 'Medium quality'),
        ('High quality', 'High quality'),
    )
    subscribe = models.CharField(
        max_length=50, choices=CATEGORY, default='Free')

    def __str__(self):
        """Retrieve full name of user"""
        return self.title
```

## views.py

```
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .decorators import  imageSubscriber


@login_required
@imageSubscriber
def MediaSecurityCheck(request, file_type, file):
    document = get_object_or_404(ModelName, image='dir/'+file)
    path, file_name = os.path.split(file)
    # print('hieieiei')
    response = FileResponse(document.image)
    return response
```

## decorators.py

```
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from .models import Walpaper

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
```

## base/urls.py

```
from django.urls import path
from .           import views


urlpatterns = [
    path('media/<str:file_type>/<str:file>', views.MediaSecurityCheck, name='media'),

]
```

## High permission Id
test4@mail.com:test1234@

### Home
<img src="https://github.com/HSAkash/MediaSubscription/blob/main/Project_images/high_profile.png?raw=true" width="350" alt="accessibility text">

### Single Image Only permission(High)
<img src="https://github.com/HSAkash/MediaSubscription/blob/main/Project_images/high_profile_single_image.png?raw=true" width="350" alt="accessibility text">


## Low permission Id
test@mail.com:test1234@

## Home
<img src="https://github.com/HSAkash/MediaSubscription/blob/main/Project_images/low_profile.png?raw=true" width="350" alt="accessibility text">

## Low permission try to view high permission Image
<img src="https://github.com/HSAkash/MediaSubscription/blob/main/Project_images/low_profile_cant_show_high_image.png?raw=true" width="350" alt="accessibility text">
