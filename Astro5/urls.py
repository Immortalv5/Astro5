"""Astro5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from Astro import views
from Astro.models import UserProfileInfo
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views

from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from django.urls import path, include
from django.contrib.auth.models import User

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^res/iml.json$', views.resjson, name='resjson'),
    url(r'^$',views.index,name='index'),
    url(r'^book/',views.book,name='book'),
    url(r'^Astro/',include('Astro.urls')),
    url(r'^wallet/$', views.initiate_payment, name = 'initiate_payment'),
    url(r'^callback/$', views.callback, name = 'callback'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset_done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.RES_URL, document_root=settings.RES_ROOT)
urlpatterns += staticfiles_urlpatterns()
