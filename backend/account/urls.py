from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    registration_view,
    login_view,
    logout_view,
    account_view,
)


urlpatterns = [
    path('register-user/', registration_view, name='register'),
    path('signin-user/', login_view, name='login'),
    path('logout-user/', logout_view, name='logout'),
    path('account/<user_id>/', account_view, name='account'),
    # path('search/', search_people, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
    