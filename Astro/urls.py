from django.urls import path
from django.conf.urls import url, include

from . import views

app_name = 'Astro'

urlpatterns = [
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^astro_register/$',views.astrologer_registration,name='astrologer_registration'),
    path('activate/<uid64>/<token>', views.user_verification, name = 'activate'),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
