from rest_framework import parsers, renderers, permissions, authentication, views, generics
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response

from .friends import FriendsAdapter
from core.models import SocialNetworkUsers
from ..serializers import SocialNetworkSerializer
from django.db.models.expressions import Q


class JSONApi(views.APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (renderers.JSONRenderer,)
    parser_classes = (parsers.JSONParser,)


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class StandardResultsSetPagination(LimitOffsetPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class SendFriendRequest(JSONApi):
    throttle_scope = 'send_friend_request'

    @staticmethod
    def post(request):
        result = FriendsAdapter(request).send_friend_request()
        return Response(status=201, data=result)


class FriendRequest(JSONApi):
    @staticmethod
    def patch(request, status):
        if status == "accept":
            result = FriendsAdapter(request).accept_friend_request()
        elif status == "reject":
            result = FriendsAdapter(request).reject_friend_request()
        else:
            return Response(status=500, data={"status param not available"})
        return Response(status=200, data=result)


class FriendList(JSONApi):
    @staticmethod
    def get(request, status):
        if status in ['pending', 'accepted']:
            result = FriendsAdapter(request).friends_list(status)
        else:
            return Response(status=500, data={"status param not available"})
        return Response(status=200, data=result)


class SocialNetworkUsersView(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SocialNetworkSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = SocialNetworkUsers.objects.all()
        search_param = self.request.query_params.get('search', None)
        if search_param:
            queryset = queryset.filter(Q(user__email__icontains=search_param))
        return queryset
