from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    SendFriendRequest,
    AllFriendRequest,
    AcceptFriendRequest,
)

urlpatterns = [
    path('friend_request/', SendFriendRequest.as_view(), name='friend-request-sent'),
    path('friend_request/<int:user_id>', AllFriendRequest.as_view(), name='friend-request'),
    path('accept_friend_request/<int:friend_request_id>', AcceptFriendRequest.as_view(), name='friend-request-accept'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
