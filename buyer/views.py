from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from buyer import models
from UniSeller import models as sellermodel
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
    data=sellermodel.ProjectAppliedModal.objects.all()
    return render(request, 'buyerdashboard.html',{'data':data})  # Render the dashboard template

def add_project(request):
    if request.method == 'POST':
        # Handle the form submission logic here.
        # For example, saving the project to the database.
        return HttpResponse("Project submitted successfully!")
    return HttpResponse("Add Project Page")  # Just for testing
       
def add_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        project_requirements = request.POST.get('project_requirements')
        project_budget = request.POST.get('project_budget')
        project_deadline = request.POST.get('project_deadline')
        
        # Create and save the project instance
        project = models.Project(
            project_name=project_name,
            project_description=project_description,
            project_requirements=project_requirements,
            project_budget=project_budget,
            project_deadline=project_deadline,
            userid=1
        )
        project.save()
        return redirect('buyerdashboard') 
    return render(request, 'buyer/add_project.html')
def view_posted_projects(request):
    # Assuming you have a Project model that stores the project data
    projects = models.Project.objects.all  # Fetch projects created by the logged-in user
    return render(request, 'view_posted_projects.html', {'projects': projects})

def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('index')