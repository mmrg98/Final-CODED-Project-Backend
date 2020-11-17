from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import  (
	SignUpSerializer, ProfileSerializer
)
from .models import Profile, Follower, Post, Photo, Item, Comment, Like
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class SignUpAPIView(CreateAPIView):
	serializer_class = SignUpSerializer


class ProfileView(RetrieveAPIView):
	serializer_class = ProfileSerializer

	def get_object(self):
		return self.request.user.profile


class UpdateProfile(APIView):
	serializer_class = ProfileSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		profile = Profile.objects.get(user=self.request.user)
		try:
			profile.user.first_name= request.data['first_name']
			profile.user.last_name= request.data['last_name']
			profile.user.email= request.data['email']
			profile.user.save()

			profile.save()
			return Response(profile.user.username, status=HTTP_200_OK)
		except:
			return Response({"msg": "Something went wrong"}, status=HTTP_400_BAD_REQUEST)
