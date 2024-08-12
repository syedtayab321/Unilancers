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
            user= buyersignup.objects.get(email=email)
            return HttpResponse("User already exists")
        except:
            user = buyersignup(name=name, email=email, password=password)
            user.save()
            return HttpResponse("User created successfully")
   else:
        return render(request,'buyersignup.html') 

def buyerdashboard(request):
    return render(request, 'buyerdashboard.html')  # Render the dashboard template

    
       