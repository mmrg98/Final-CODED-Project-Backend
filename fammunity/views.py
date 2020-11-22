from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from .serializers import  (
	SignUpSerializer, ProfileSerializer, PostSerializer
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
	permission_classes = [AllowAny]

	def post(self, request):
		data = request.data
		files = request.FILES
		print("print request.FILES" ,files)
		print("print request.data" ,data)



		user_obj = User.objects.get(username="hanodi") #hend added this for testing
		profile = Profile.objects.get(user=user_obj) #hend added this for testing
		#profile = Profile.objects.get(user=self.request.user) #By Hamza
		post = Post.objects.create(owner=profile, description=data['description'])

		# # Iterate over items 
		itemsCounter = int(data['itemsCounter'])
		for i in range(itemsCounter):
			brand = Brand.objects.get(id=int(data['brand'+str(i)]))
			new_item = Item.objects.create(post=post,name=data['name'+str(i)],brand=brand,size=int(data['size'+str(i)]),price=int(data['price'+str(i)]))


		# Iterate over images 
		counter = int(data['counter'])
		for i in range(counter):
			print('files["photo"+str(i)]',files['photo'+str(i)])
			new_image = Photo.objects.create(post=post,image=files['photo'+str(i)])

		# Iterate over images from files
		# Create image and assign to "post"

		return Response(status=HTTP_200_OK)
		#return Response(image.image.url, status=HTTP_200_OK)


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
