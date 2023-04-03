from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _
from django.db.models.constraints import *
from django.db.models.expressions import Q, F, OuterRef


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        SocialNetworkUsers.objects.create(user=instance)


class Status(models.TextChoices):
    pending = 'PENDING', _('PENDING')
    accepted = 'ACCEPTED', _('ACCEPTED')
    rejected = 'REJECTED', _('REJECTED')


class RelationshipType(models.TextChoices):
    requested = 'REQUESTED', _('REQUESTED')
    received = 'RECEIVED', _('RECEIVED')


class SocialNetworkUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('SocialNetworkUsers', through='FriendsThrough',
                                     through_fields=('social_network_user', 'friend'),

                                     related_name='social_network', symmetrical=False)


class FriendsThrough(models.Model):
    social_network_user = models.ForeignKey(SocialNetworkUsers, related_name='social', on_delete=models.CASCADE)
    friend = models.ForeignKey(SocialNetworkUsers, related_name='friend', on_delete=models.CASCADE)
    relationship_type = models.CharField(choices=RelationshipType.choices, max_length=10, blank=False)
    status = models.CharField(choices=Status.choices, max_length=10, blank=False)

    class Meta:
        """
        i am trying to add check constraint since user cannot be a friend for himself and
        unique constraint for user,friend and type to avoid duplication
        """
        constraints = [UniqueConstraint(fields=('social_network_user', 'friend', 'relationship_type'),
                                        name='unique_social_friend_relation'),
                       CheckConstraint(check=~Q(social_network_user=F('friend')), name='user_not_as_friend')]
