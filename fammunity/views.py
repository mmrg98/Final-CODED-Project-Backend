from rest_framework.generics import (
	ListAPIView, CreateAPIView, RetrieveAPIView,
	RetrieveUpdateAPIView
)
from .serializers import  (
	SignUpSerializer, ProfileSerializer, PostSerializer,LikeSerializer
)
from .models import Profile, Post, Photo, Item, Comment,Brand, Follow
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
	permission_classes = [IsAuthenticated]

	def post(self, request):
		data = request.data
		files = request.FILES
		profile = request.user.profile

		post = Post.objects.create(owner=profile, description=data['description'])

		items_counter = int(data['itemsCounter'])
		for i in range(items_counter):
			Item.objects.create(
				post=post,
				name=data[f'name{i}'],
				brand_id = int(data[f'brand{i}']),
				price = int(data[f'price{i}'])
			)

		counter = int(data['counter'])
		for i in range(counter):
			file_value = files[f'photo{i}']
			Photo.objects.create(post=post,image=file_value)

		return Response(self.serializer_class(post,context={'request':request}).data ,status=HTTP_200_OK)


class CreateComment(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		comment = Comment.objects.create(
			txt=request.data['txt'],
			post_id=request.data['post_id'],
			commenter=self.request.user.profile
		)
		return Response({"comment": comment.txt}, status=HTTP_200_OK)


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
		profile.gender= request.data['gender']
		profile.image = files['image']
		profile.save()
		return Response({"username": profile.user.username}, status=HTTP_200_OK)


class LikePost(APIView):
	permission_classes=[IsAuthenticated]

	def post(self, request):
		profile = self.request.user.profile
		post = Post.objects.get(id=request.data['post_id'])

		if profile in post.liked_by.all():
			post.liked_by.remove(profile)
			post.save()
			return Response({"liked": False}, status=HTTP_200_OK)
		else:
			post.liked_by.add(profile)
			post.save()
			return Response({"liked": True}, status=HTTP_200_OK)


class LikersListView(RetrieveAPIView):
    queryset = Post.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id'
    serializer_class = LikeSerializer
    permission_classes = [AllowAny] 


class UserProfileView(RetrieveAPIView):
    queryset = Profile.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'owner_id'
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny] 


class Follow(APIView):
	permission_classes=[IsAuthenticated]
	# permission_classes = [AllowAny]

	def post(self, request):
		user = request.user.profile
		user_to_follow = Profile.objects.get(user=request.data['profile_id'])
		
		follow_obj, created = Follow.objects.get_or_create(
			user_from = user,
			user_to = user_to_follow,
		)

		if not created:
			follow_obj.delete()
		
		follow = user.following.all().values_list('user_to__username', flat=True)
		return Response({"follow": follow}, status=HTTP_200_OK)


class Feeds(ListAPIView):
	serializer_class = PostSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		user = Profile.objects.get(user=self.request.user)
		queryset = Post.objects.filter(owner__in=user.followers.all()).order_by('created')
		return Response({"feeds": [post.description for post in queryset]}, status=HTTP_200_OK)
