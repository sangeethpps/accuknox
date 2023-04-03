from .models import FriendsThrough, RelationshipType, User, SocialNetworkUsers
import re


def update_friend_request(user_id, friend_id, status, update_status):
    user_obj = FriendsThrough.objects.get(social_network_user_id=user_id,
                                          friend_id=friend_id, relationship_type=RelationshipType.requested,
                                          status=status)
    user_obj.status = update_status
    user_obj.save()

    friend_obj = FriendsThrough.objects.get(social_network_user_id=friend_id,
                                            friend_id=user_id, relationship_type=RelationshipType.received,
                                            status=status)
    friend_obj.status = update_status
    friend_obj.save()
    return {f'{user_obj.id}': {
        'social_user': user_obj.social_network_user.user.email,
        'friend': user_obj.friend.user.email,
        'relationship_type': user_obj.relationship_type.title(), 'status': user_obj.status.title()
    }, f'{friend_obj.id}': {
        'social_user': friend_obj.social_network_user.user.email,
        'friend': friend_obj.friend.user.email,
        'relationship_type': friend_obj.relationship_type.title(), 'status': friend_obj.status.title()
    }}


def base_query_set(user_id):
    return FriendsThrough.objects.filter(social_network_user_id=user_id,
                                         relationship_type=RelationshipType.requested).all()


def create_dummy_users(**kwargs):
    user_emails = ["sangeeth@gmail.com", "chandru@gmail.com",
                   "sam@gmail.com", "tim@gmail.com", "raj@gmail.com",
                   "george@gmail.com", "christopher@gmail.com", "confluence@gmail.com",
                   "sundar@gmail.com", "bai@gmail.com", "peter@gmail.com", "bill@gmail.com"]
    for user_email in user_emails:
        if not User.objects.filter(email=user_email).exists():
            if re.search(r'[a-zA-Z0-9]+', user_email).group() == "sangeeth":
                user_obj = User.objects.create_superuser(email=user_email,
                                                    password=re.search(r'[a-zA-Z0-9]+', user_email).group())
            else:

                user_obj = User.objects.create_user(email=user_email,
                                                    password=re.search(r'[a-zA-Z0-9]+', user_email).group())

    return True
