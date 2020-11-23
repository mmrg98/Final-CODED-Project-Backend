from rest_framework.generics import (
	ListAPIView, CreateAPIView, RetrieveAPIView,
	RetrieveUpdateAPIView
)
from .serializers import  (
	SignUpSerializer, ProfileSerializer, PostSerializer,LikeSerializer
)
from .models import Profile, Post, Photo, Item, Comment,Brand
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User


class SignUpAPIView(CreateAPIView):
	serializer_class = SignUpSerializer


class ProfileView(RetrieveAPIView):
	serializer_class = ProfileSerializer

	def get_object(self):
		return self.request.user.profile


class PostListView(ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [AllowAny] 


class CreatePost(APIView):
	serializer_class = PostSerializer
	permission_classes = [AllowAny]

	def post(self, request):
		data = request.data
		files = request.FILES
		profile = request.user.profile # the original 



		post = Post.objects.create(owner=profile, description=data['description'])

		items_counter = int(data['itemsCounter'])
		for i in range(items_counter):
			Item.objects.create(
				post=post,
				name=data[f'name{i}'],
				brand_id = int(data[f'brand{i}']),
				size = int(data[f'size{i}']),
				price = int(data[f'price{i}'])
			)

		counter = int(data['counter'])
		for i in range(counter):
			file_value = files[f'photo{i}']
			Photo.objects.create(post=post,image=file_value)
			
		return Response(self.serializer_class(post).data,status=HTTP_200_OK)


class CreateComment(APIView): #new
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


class LikePost(APIView): #new
	permission_classes=[IsAuthenticated]
	permission_classes = [AllowAny]

	def post(self, request):
		profile = Profile.objects.get(user=self.request.user) #By mariam
		post = Post.objects.get(id=request.data['post_id'])

		if profile in post.liked_by.all():
			post.liked_by.remove(profile)
			post.save()
			return Response("false", status=HTTP_200_OK)

		else:
			post.liked_by.add(profile)
			post.save()			
			return Response("true", status=HTTP_200_OK)


class LikersListView(ListAPIView): #new
	queryset = Post.objects.all()
	serializer_class = LikeSerializer
	permission_classes = [AllowAny] 
