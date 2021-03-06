from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework import serializers

from .models import SocialAuthentication
from rest_framework import viewsets, permissions
from .serializers import SocialAuthenticationSerializer
from user.permissions import IsUpdateProfile, IsStaffOrTargetUser
from rest_framework.decorators import action
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login


class SocialAuthenticationView(viewsets.ModelViewSet):
    serializer_class = SocialAuthenticationSerializer
    queryset = SocialAuthentication.objects.all()
    permission_classes = (AllowAny)

    @action(methods=['post'], detail=True, permission_classes=[permission_classes])
    def provider(self, request, pk):
        providerIsFacebook = request.data['provider'] == "Facebook"

        name = request.data['name']
        password = make_password(pk)
        picture = request.data['picture']
        [first_name, last_name] = str.split(name)

        username = name.replace(" ", "")

        user, userCreated = User.objects.filter(
            Q(email=request.data['email'])
            | Q(facebook_id=pk)
            | Q(google_id=pk),
        ).get_or_create(
            email=request.data['email'],

            defaults={
                'facebook_id': pk,
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'picture': picture,
                'profile_uri': username
            } if(providerIsFacebook) else {
                'google_id': pk,
                'username': username,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'picture': picture,
                'profile_uri': username
            },
        )
        if user:
            # record already exist
            setattr(user, 'first_name', first_name)
            setattr(user, 'last_name', last_name)
            if(not getattr(user, 'picture')):
                setattr(user, 'picture', picture)
            if(providerIsFacebook):
                setattr(user, 'facebook_id', pk)
            else:
                setattr(user, 'google_id', pk)

        # if userCreated:
            # update record with defaults

        user.save()
        userSerialized = UserSerializer(user)
        update_last_login(None, user)

        token, created = Token.objects.get_or_create(user=user)

        socialAuthentication, socialAuthCreated = SocialAuthentication.objects.get_or_create(
            provider_id=pk,
            defaults={
                'provider': request.data['provider'],
                'user_id': user,
                'access_token': request.data['access_token'],
                'expires_in': request.data['expires_in'],
                'expires_at': request.data['expires_at'],
                'name': name,
                'email': request.data['email'],
                'picture': picture
            },
        )

        return Response({**{'token': token.key}, **userSerialized.data})
