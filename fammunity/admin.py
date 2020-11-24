from django.contrib import admin
from .models import Profile,Post,Photo,Item,Comment,Brand,Follow


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender']
    list_filter = ['gender']
    search_fields = ['user__username',]
    list_display_links = ['user',]


class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name',]



class ItemInline(admin.TabularInline):
    model = Item


class PhotoInline(admin.TabularInline):
    model = Photo


class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'created','modified',]
    list_filter = ['owner', 'created','modified']
    search_fields = ['owner__username',]
    list_display_links = ['owner',]
    inlines = [
        ItemInline, PhotoInline,
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['txt', 'commenter','post']
    list_filter = ['commenter','post']
    search_fields = ['txt', 'commenter','post']
    list_display_links = ['commenter',]


admin.site.register(Profile,ProfileAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Item)
admin.site.register(Comment,CommentAdmin)