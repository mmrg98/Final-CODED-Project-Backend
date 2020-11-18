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



'''class OrderItems(APIView):
	serializer_class = OrderSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):
		new_order, _ = Order.objects.get_or_create(customer=self.request.user, is_paid=False)
		item, added = Item.objects.get_or_create(product=Product.objects.get(id=request.data['product_id']),order=new_order)

		if added:
			item.quantity=request.data['quantity']
		else:
			item.quantity += request.data['quantity']
		item.save()

		new_total = (int(request.data['quantity'])*float(item.product.price))+float(new_order.total)
		new_order.total = new_total
		new_order.save()
		return Response(self.serializer_class(new_order).data, status=HTTP_200_OK)'''



class createPost(APIView):
	serializer_class = PostSerializer
	permission_classes = [IsAuthenticated]


	def post(self, request):
		profile = Profile.objects.get(user=self.request.user)

		try:
			post = Post(owner=profile, description=request.data['description'])
			post.save()

			#images_length = request.data['photos'].length
			image = Photo(image=request.data['image'], post=post)
			image.save()

			return Response(image.image.url, status=HTTP_200_OK)
		except:
			return Response({"msg": "Something went wrong"}, status=HTTP_400_BAD_REQUEST)


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
