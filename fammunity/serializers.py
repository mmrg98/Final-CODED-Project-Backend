from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile,Follower,Post,Photo,Item,Comment,Like
from rest_framework_simplejwt.tokens import RefreshToken


class SignUpSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	token = serializers.CharField(allow_blank=True, read_only=True)

	class Meta:
		model = User
		fields = ['username', 'email','first_name', 'last_name', 'password','token']

	def create(self, validated_data):

		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		token = RefreshToken.for_user(new_user)
		validated_data["token"] = str(token.access_token)
		return validated_data


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model= User
		fields = ['username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	class Meta:
		model= Profile
		fields = ['user','gender','image']


class PhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model= Photo
		fields = ['image']


class PostSerializer(serializers.ModelSerializer):
	images=PhotoSerializer(many=True)
	class Meta:
		model= Post
		fields = ['description', 'images']
