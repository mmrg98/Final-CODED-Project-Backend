from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import  (
	SignUpSerializer, ProfileSerializer, PostSerializer
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


class CreatePost(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		data = request.data
		files = request.FILES
		print(files)

		profile = Profile.objects.get(user=self.request.user)
		post = Post.objects.create(owner=profile, description=request.data['description'])

		# Iterate over images from files
		# Create image and assign to "post"

		return Response(image.image.url, status=HTTP_200_OK)


class CreateComment(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		comment = Comment.objects.create(
			txt=request.data['txt'], 
			post_id=request.data['post_id'], 
			commenter=self.request.user.profile
		)
		return Response(comment.txt, status=HTTP_200_OK)


class UpdateProfile(APIView):
	serializer_class = ProfileSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user = self.request.user		
		user.first_name= request.data['first_name']
		user.last_name= request.data['last_name']
		user.email= request.data['email']
		user.save()

		profile = user.profile
		# Update Gender and Image
		profile.save()
		return Response(profile.user.username, status=HTTP_200_OK)
