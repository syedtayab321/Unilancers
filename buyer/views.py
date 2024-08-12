from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from buyer import models
# Create your views here.
def buyerlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user=models.Buyersignup.objects.get(name=username)
            if user.password==password:
             request.session["email"]=user.email
             request.session["username"]=user.name
             return redirect('buyerdashboard')  # 'buyer_dashboard' is the name of your dashboard URL
            else:
              return render(request, 'buyersignup.html', {'error': 'Invalid username or password'})
        except Exception as e:
            return HttpResponse(e)
    return render(request,'buyersignup.html') 


def buyersignup(request):
   if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user= models.Buyersignup.objects.get(email=email)
            return HttpResponse("User already exists")
        except:
            user = models.Buyersignup(name=name, email=email, password=password)
            user.save()
            return HttpResponse("User created successfully")
   else:
        return render(request,'buyersignup.html') 

def buyerdashboard(request):
    return render(request, 'buyerdashboard.html')  # Render the dashboard template

def add_project(request):
    if request.method == 'POST':
        # Handle the form submission logic here.
        # For example, saving the project to the database.
        return HttpResponse("Project submitted successfully!")
    return HttpResponse("Add Project Page")  # Just for testing
       
def add_project(request):
    if request.method == 'POST':
        form = models.ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('buyerdashboard')  # Redirect to dashboard after saving
    else:
        form = models.ProjectForm()
    return render(request, 'buyer/add_project.html', {'form': form})
