from django.urls import path

from accounts import views


urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('logout',views.Logout,name="logout"),
    path('create_blog',views.create_blog,name="create_blog"),
    path('posts',views.posts,name="posts"),
    path('my_posts',views.my_posts,name="my_posts")
]