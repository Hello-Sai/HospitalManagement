from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import Blog, User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.contrib.auth.decorators import login_required

def home(request):
    if request.method=="POST":
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email,password=password)
        print(user,email,password)
        if user:
            login(request,user)
            messages.success(request,"logged in successfully")
            return redirect('/dashboard')
        else:
            messages.error(request,"Invalid email /password ","danger")
    return render(request,'home.html')
@login_required(login_url="/")
def dashboard(request):
    print(request.user.profile_picture)
    return render(request,'dashboard.html',{'user':request.user})
def Logout(request):
    logout(request)
    messages.success(request,'successfully logged out')
    return redirect('home')
def signup(request):
    if request.method=="POST":
        try:
            print(request.FILES)
            data = request.POST
            user = User(
                first_name = data['firstname'],
                last_name = data["lastname"],
                profile = data["profile"],
                profile_picture =  request.FILES['profile_picture'],
                username = data["username"],
                email = data["email"],
                address = data["address"],
            )
            user.set_password(data['password'])
            user.save()
            messages.success(request,"Successfully Registered")
        except Exception as e:
            messages.error(request,"Got an error -> %s"%e,"danger")
    return render(request,'signup.html')

def postblog(request):
    if request.method=='POST':
        data = request.POST.copy()
        print(data,request.FILES)
        data.pop('csrfmiddlewaretoken')
        data = {**data,'profile':request.FILES['image']}
        data.update(is_drafted=True if data['saveDraft']=='on' else False)
        print(data)
        # Blog.objects.create()
    return render(request,'blogpost.html')