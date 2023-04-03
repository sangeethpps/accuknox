from django.db import transaction, IntegrityError

from ..functions import update_friend_request, base_query_set
from ..models import *


class FriendsAdapter:
    def __init__(self, request):
        self.request = request
        self.exceptions = []
        self.social_user_id = None
        self.friend_user_id = None

    def check_for_errors_in_friend_request(self):
        if 'friend_id' not in self.request.data:
            raise KeyError('missing param friend_id in request')
        social_user_queryset = SocialNetworkUsers.objects.filter(user_id=self.request.user.id)
        friend_social_queryset = SocialNetworkUsers.objects.filter(user_id=self.request.data['friend_id'])
        if not social_user_queryset.exists():
            raise Exception('user/social_user_id is not registered yet ')
        if not friend_social_queryset.exists():
            raise Exception('user/friend_id is not registered yet')
        self.social_user_id = social_user_queryset.values('id').first()['id']
        self.friend_user_id = friend_social_queryset.values('id').first()['id']
        return True

    def check_for_errors_in_get(self):
        social_user_queryset = SocialNetworkUsers.objects.filter(user_id=self.request.user.id)
        if not social_user_queryset.exists():
            raise Exception('user/social_user_id is not registered yet ')
        self.social_user_id = social_user_queryset.values('id').first()['id']
        return True

    def preprocess(self, request_type):
        if request_type in ['accept', 'reject', 'send']:
            return self.check_for_errors_in_friend_request()
        if request_type in ['get_friends_list']:
            return self.check_for_errors_in_get()

    def send_friend_request(self):
        try:
            self.preprocess(request_type='send')
            controller_obj = FriendsController(self.request, self.social_user_id, self.friend_user_id)
            return controller_obj.send_friend_request()
        except Exception as e:
            return str(e)

    def accept_friend_request(self):
        try:
            self.preprocess(request_type='accept')
            controller_obj = FriendsController(self.request, self.social_user_id, self.friend_user_id)
            return controller_obj.accept_friend_request()
        except Exception as e:
            return str(e)

    def reject_friend_request(self):
        try:
            self.preprocess(request_type='reject')
            controller_obj = FriendsController(self.request, self.social_user_id, self.friend_user_id)
            return controller_obj.reject_friend_request()
        except Exception as e:
            return str(e)

    def friends_list(self, status):
        try:
            self.preprocess(request_type='get_friends_list')
            controller_obj = FriendsController(self.request, self.social_user_id)
            return controller_obj.friends_list(status)
        except Exception as e:
            return str(e)


class FriendsController:
    def __init__(self, request, social_user_id, friend_user_id=None):
        self.request = request
        self.user_id = social_user_id
        self.friend_id = friend_user_id
        self.result = None
        self.exceptions = []

    @transaction.atomic()
    def send_friend_request(self):
        with transaction.atomic():
            try:
                user_obj = FriendsThrough.objects.create(social_network_user_id=self.user_id,
                                                         friend_id=self.friend_id,
                                                         relationship_type=RelationshipType.requested,
                                                         status=Status.pending)
                friend_obj = FriendsThrough.objects.create(social_network_user_id=self.friend_id,
                                                           friend_id=self.user_id,
                                                           relationship_type=RelationshipType.received,
                                                           status=Status.pending)

                self.result = {f'{user_obj.id}': {
                    'social_user': user_obj.social_network_user.user.email,
                    'friend':user_obj.friend.user.email,
                    'relationship_type':user_obj.relationship_type.title(), 'status':user_obj.status.title()
                },f'{friend_obj.id}': {
                    'social_user': friend_obj.social_network_user.user.email,
                    'friend':friend_obj.friend.user.email,
                    'relationship_type':friend_obj.relationship_type.title(), 'status':friend_obj.status.title()
                }}
            except Exception as e:
                transaction.set_rollback(True)
                self.exceptions.append(str(e))
            finally:
                return self.post_process()

    def accept_friend_request(self):
        with transaction.atomic():
            try:
                self.result = update_friend_request(self.user_id, self.request.data["friend_id"], Status.pending,
                                                    Status.accepted)
            except Exception as e:
                transaction.set_rollback(True)
                self.exceptions.append(str(e))
            finally:
                return self.post_process()

    def reject_friend_request(self):
        with transaction.atomic():
            try:
                self.result = update_friend_request(self.user_id, self.request.data["friend_id"], Status.pending,
                                                    Status.rejected)
            except Exception as e:
                transaction.set_rollback(True)
                self.exceptions.append(str(e))
            finally:
                return self.post_process()

    def friends_list(self, status):
        friends_queryset = base_query_set(self.user_id).filter(
            status=Status[status]).values('friend__user__email', 'status')
        self.result = []
        for friend in friends_queryset:
            self.result.append({'Friend': friend['friend__user__email'], 'Status': friend['status']})
        return self.post_process()

    def post_process(self):
        return {'result': self.result, 'exceptions': self.exceptions}
