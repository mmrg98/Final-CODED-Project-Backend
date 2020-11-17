from django.contrib import admin
from .models import Profile,Follower,Post,Photo,Item,Comment,Like


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'gender']
    list_display = ['user', 'gender']
    list_filter = ['gender']
    search_fields = ['user',]
    list_display_links = ['user',]

admin.site.register(Profile,ProfileAdmin)


class FollowerAdmin(admin.ModelAdmin):
    fields = ['user', 'follower']
    list_display = ['user', 'follower']
    list_filter = ['user', 'follower']
    list_display_links = ['user',]

admin.site.register(Follower,FollowerAdmin)


class PostAdmin(admin.ModelAdmin):
    fields = ['owner', 'created','modified','description']
    list_display = ['owner', 'created','modified','description']
    list_filter = ['owner', 'created','modified']
    search_fields = ['description',]
    list_display_links = ['owner',]

admin.site.register(Post,PostAdmin)


class PhotoAdmin(admin.ModelAdmin):
    fields = ['post', 'image']
    list_display = ['post', 'image']
    list_display_links = ['post',]

admin.site.register(Photo,PhotoAdmin)


class ItemAdmin(admin.ModelAdmin):
    fields = ['name', 'brand','store','size','price','post']
    list_display = ['name', 'brand','store','size','price','post']
    list_filter = ['brand','store','size','price']
    search_fields = ['name', 'brand','store','size','price','post']
    list_display_links = ['name',]

admin.site.register(Item,ItemAdmin)


class CommentAdmin(admin.ModelAdmin):
    fields = ['txt', 'commenter','post']
    list_display = ['txt', 'commenter','post']
    list_filter = ['commenter','post']
    search_fields = ['txt', 'commenter','post']
    list_display_links = ['commenter',]

admin.site.register(Comment,CommentAdmin)


class LikeAdmin(admin.ModelAdmin):
    fields = ['fan', 'post']
    list_display = ['fan', 'post']
    list_filter = ['fan']
    search_fields = ['post']
    list_display_links = ['fan',]

admin.site.register(Like,LikeAdmin)
