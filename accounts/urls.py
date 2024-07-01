from django.urls import path

from accounts import views


urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('dashboard',views.dashboard,name="dashboard"),
    path('logout',views.Logout,name="logout"),
    path('postblog',views.postblog,name="blog_post")
]