from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from accounts.models import Blog, User
from django.contrib.auth import authenticate,login,logout
# Create your views here.
from django.contrib.auth.decorators import login_required
from accounts.permissions import is_doctor
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
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid email /password ","danger")
    return render(request,'home.html')
@login_required(login_url="/")
def dashboard(request):
    print(request.user.first_name,request.user.last_name)
    return render(request,'dashboard.html')
def Logout(request):
    logout(request)
    messages.success(request,'successfully logged out')
    return redirect('home')
def signup(request):
    print(request.POST)
    if request.method=="POST":
        try:
            print(request.FILES)
            data = request.POST
            address = " , ".join((data["address"], data['city'],data['state'],data['pincode'] ))
            print(address)
            user = User(
                first_name = data['firstname'],
                last_name = data["lastname"],
                is_doctor = True if data["profile"] == "doctor" else False,
                profile_picture =  request.FILES['profile_picture'],
                username = data["username"],
                email = data["email"],
                address = address ,

            )
            user.set_password(data['password'])
            user.save()
            messages.success(request,"Successfully Registered")
        except Exception as e:
            messages.error(request,"Got an error -> %s"%e,"danger")
    return render(request,'signup.html')

@is_doctor
def create_blog(request):
    
    if request.method=='POST':
        print("drafted",request.POST)
        data = {
            "title":request.POST["title"],
            "category":request.POST["category"],
            "summary":request.POST["summary"],
            "content":request.POST["content"],
            'image':request.FILES['image'],
        }
        data.update(is_drafted=request.POST.get('is_drafted')=='on')
        
        messages.info(request,"Successfully Posted.")
        request.user.blogs.create(**data)
        return redirect("posts")
    return render(request,'blogpost.html')

def posts(request):
    posts = Blog.objects.all().filter(is_drafted = False)
    print(posts.order_by('category'),"ordered")
    return render(request,'posts.html',locals())

@login_required(login_url='/')
def my_posts(request):
    posts = request.user.blogs.all()
    exclude_category =True 
    return render(request,'posts.html',locals())