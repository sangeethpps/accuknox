
from django.urls import path

from core.backend.views import FriendRequest, FriendList, SendFriendRequest, SocialNetworkUsersView

urlpatterns = [
    path("social-network/users/", SocialNetworkUsersView.as_view()),
    path("social-network/friend-request/send/", SendFriendRequest.as_view()),
    path("social-network/friend-request/<slug:status>/", FriendRequest.as_view()),
    path("social-network/friend-request/list/<slug:status>/", FriendList.as_view()),
]
