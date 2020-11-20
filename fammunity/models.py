from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Profile(models.Model):
	GENDER = (
		("F", "Female"),
		("M", "Male")
	)
	followers = models.ManyToManyField("self", related_name="following", blank=True, null=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	gender = models.CharField(choices=GENDER, max_length=2, null=True)
	image = models.ImageField(upload_to='profile_image', default='profile.png')

	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user= instance)


class Post(models.Model):
	liked_by = models.ManyToManyField(Profile, related_name='likes', blank=True, null=True)
	description = models.TextField(max_length=500)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='owner')

	def __str__(self):
		return '%s ,id: %s' % (self.owner.user.username, self.id)



class Photo(models.Model):
	image = models.ImageField(upload_to='post_photos')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='photos')

	def __str__(self):
		return '%s' % (self.post.owner.user.username)


class Brand(models.Model):
	name = models.CharField(max_length=250)


class Item(models.Model):
	name = models.CharField(max_length=250)
	brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='items')
	size = models.IntegerField(blank=True,null=True)
	price = models.DecimalField(max_digits=4, decimal_places=2,blank=True,null=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='items')

	def __str__(self):
		return '%s:  %s' % (self.post.owner.user.username, self.name)


class Comment(models.Model):
	txt = models.TextField(max_length=300)
	commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
