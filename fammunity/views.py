from rest_framework.generics import (
	ListAPIView, CreateAPIView, RetrieveAPIView,
	RetrieveUpdateAPIView
)
from .serializers import  (
	SignUpSerializer, ProfileSerializer, PostSerializer,LikeSerializer,BrandSerializer,CommentSerializer,CommentSerializerList
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

class BrandListView(ListAPIView):
	queryset = Brand.objects.all()
	serializer_class = BrandSerializer
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

		return Response(
			self.serializer_class(post,context={'request':request}).data,
			status=HTTP_200_OK
		)


class CreateComment(APIView):
	serializer_class = CommentSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		comment = Comment.objects.create(
			txt=request.data['txt'],
			post_id=request.data['post_id'],
			commenter=self.request.user.profile
		)
		return Response(self.serializer_class(comment).data, status=HTTP_200_OK)


class Comments(RetrieveAPIView):
	queryset = Post.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'post_id'
	serializer_class = CommentSerializerList
	permission_classes = [AllowAny]


	'''serializer_class = CommentSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		print("post id",self.request.data)
		return Comment.objects.filter(post_id=self.request.data['post_id'])'''


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
		profile.image = request.FILES['image']
		profile.save()
		return Response({"username": profile.user.username}, status=HTTP_200_OK)


class LikePost(APIView):
	serializer_class = LikeSerializer
	permission_classes=[IsAuthenticated]

	def post(self, request):
		profile = self.request.user.profile
		post = Post.objects.get(id=request.data['post_id'])

		if profile in post.liked_by.all():
			post.liked_by.remove(profile)
			liked = False
		else:
			post.liked_by.add(profile)
			liked = True

		return Response(
			{"liked": liked , 'likers':self.serializer_class(post).data},
			status=HTTP_200_OK
		)


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


class FollowProfile(APIView):
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

		follow = user.following.all().values_list('user_to__user__username', flat=True)
		return Response({"follow": follow}, status=HTTP_200_OK)


class Feeds(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user.profile
        followers= user.following.values_list('user_to', flat=True)
        queryset = Post.objects.filter(owner_id__in=followers).order_by('created')
        return queryset
#owner=user
