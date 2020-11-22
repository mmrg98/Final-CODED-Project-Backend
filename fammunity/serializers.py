from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile,Post,Photo,Item,Comment
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

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model= Item
		fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
	photos=PhotoSerializer(many=True)
	items=ItemSerializer(many=True)
	liked_by = serializers.SerializerMethodField() #new
	class Meta:
		model= Post
		fields = ['id','description','photos','items','liked_by']

	def get_liked_by(self, obj): #new
		return obj.liked_by.all().count()

# Remove this serializer, not used.
class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model= Comment
		fields = ['txt']
