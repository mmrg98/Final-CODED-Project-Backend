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


class PhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model= Photo
		fields = ['id','image']


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model= Item
		fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
	photos=PhotoSerializer(many=True)
	items=ItemSerializer(many=True)
	likers_number = serializers.SerializerMethodField()
	liked = serializers.SerializerMethodField()
	owner_name = serializers.SerializerMethodField()

	class Meta:
		model= Post
		fields = ['id','description','photos','items','likers_number', 'owner','liked','owner_name']

	def get_likers_number(self, obj):
		return obj.liked_by.all().count()

	def get_liked(self, obj):
		user = self.context['request'].user
		if user.is_authenticated:
			return user.profile in obj.liked_by.all()
		return False

	def get_owner_name(self, obj):
		return obj.owner.user.username


class ProfileSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	posts=PostSerializer(many=True)
	class Meta:
		model= Profile
		fields = ['id','user','gender','image','posts']


class ProfileSerializer1(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model= Profile
        fields = ['id','user','gender','image']


class LikeSerializer(serializers.ModelSerializer):
	liked_by = ProfileSerializer1(many=True)

	class Meta:
		model= Post
		fields = ['id','liked_by']


	
