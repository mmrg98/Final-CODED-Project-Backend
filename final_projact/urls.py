from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from fammunity import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view() , name='login'),
    path('signup/', views.SignUpAPIView.as_view(), name='register'),
    
    path('profile/', views.ProfileView.as_view(), name="profile"),
    path('user-profile/<int:owner_id>', views.UserProfileView.as_view(), name="user-profile"),
    path('profile/edit/', views.UpdateProfile.as_view(), name="edit-profile"),


    path('feeds/', views.Feeds.as_view(), name="feeds"),
    path('explore/', views.PostListView.as_view(), name="explore"),
    path('post/', views.CreatePost.as_view(), name="post"),

    path('like/', views.LikePost.as_view(), name="like"),
    path('likers/<int:post_id>', views.LikersListView.as_view(), name="likers"),

    path('follow/', views.FollowProfile.as_view(), name="follow"),



]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
