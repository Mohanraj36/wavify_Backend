from django.urls import path
from .import views
from .views import RegisterAPI, LoginAPI, PlayListAPI
from knox import views as knox_views
from rest_framework.urlpatterns import format_suffix_patterns
app_name = "App"

urlpatterns = [
    path('', views.index, name="index"),
    path('songs', views.songs, name="songs"),
    path('songs/<int:id>', views.songs, name="songs"),
    path('search', views.search, name="search"),
    path('playlist', PlayListAPI.as_view(), name='playlist'),
    path('playlist/<int:pk>', PlayListAPI.as_view(), name='playlist'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='logoutall'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
