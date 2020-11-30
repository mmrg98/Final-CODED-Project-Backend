from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile,Post,Photo,Item,Comment,Follow
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

class ProfileSerializer1(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model= Profile
        fields = ['id','user','gender','image']

class PostSerializer(serializers.ModelSerializer):
	photos=PhotoSerializer(many=True)
	items=ItemSerializer(many=True)
	likers_number = serializers.SerializerMethodField()
	liked = serializers.SerializerMethodField()
	owner = ProfileSerializer1()

	class Meta:
		model= Post
		fields = ['id','description','photos','items','likers_number', 'owner','liked']

	def get_likers_number(self, obj):
		return obj.liked_by.all().count()

	def get_liked(self, obj):
		user = self.context['request'].user
		if user.is_authenticated:
			return user.profile in obj.liked_by.all()
		return False



class ProfileSerializer(serializers.ModelSerializer):
	user=UserSerializer()
	posts=PostSerializer(many=True)
	followed=serializers.SerializerMethodField()
	following = serializers.SerializerMethodField()
	class Meta:
		model= Profile
		fields = ['id','user','gender','image','posts','following','followers','followed']

	def get_followed(self, obj):
		user = self.context['request'].user
		if user.is_authenticated:
			return obj.followers.filter(user_from=user.profile).exists()
		return False

	def get_following(self, obj):
		following_objs = obj.following.all()
		following_json = followingSerializer(following_objs, many=True).data
		return following_json



class followingSerializer(serializers.ModelSerializer):

	class Meta:
		model= Follow
		fields = ['user_to']


class LikeSerializer(serializers.ModelSerializer):
	liked_by = ProfileSerializer1(many=True)

	class Meta:
		model= Post
		fields = ['id','liked_by']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Comment
        fields = '__all__'
		

class CommentSerializerList(serializers.ModelSerializer):
	comments = CommentSerializer(many=True)
	class Meta:
		model= Post
		fields = ['comments']



