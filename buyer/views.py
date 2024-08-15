from django.http import HttpResponse
from django.shortcuts import render, redirect
from buyer import models
from UniSeller import models as sellermodel

def buyerlogin(request):
    if request.session.get('buyeremail') is None:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            try:
                user = models.Buyersignup.objects.get(name=username)
                if user.password == password:
                    request.session["buyeremail"] = user.email
                    request.session["buyerusername"] = user.name
                    request.session['userid']=user.id
                    return redirect('buyerdashboard')
                else:
                    return render(request, 'buyersignup.html', {'error': 'Invalid username or password'})
            except Exception as e:
                return HttpResponse(e)
        return render(request,'buyersignup.html')
    return redirect('buyerdashboard')


def buyersignup(request):
    if request.session.get("buyeremail") is None:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                user = models.Buyersignup.objects.get(email=email)
                return HttpResponse("User already exists")
            except:
                user = models.Buyersignup(name=name, email=email, password=password)
                user.save()
                return HttpResponse("Data created sucessfully")
        return render(request,'buyersignup.html')
    else:
        return redirect('buyerdashboard')


def buyerdashboard(request):
    # Check if the user ID is available in the session
    user_id = request.session.get('userid')
    if not user_id:
        return HttpResponse('User ID not found in session', status=400)

    try:
        data = sellermodel.ProjectAppliedModal.objects.filter(posted_by=user_id)
        return render(request, 'buyerdashboard.html', {'data': data})
    except sellermodel.ProjectAppliedModal.DoesNotExist:
        return render(request, 'buyerdashboard.html', {'data': []})
    except Exception as e:
        return HttpResponse(f'An error occurred: {str(e)}', status=500)
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
            userid=request.session.get('userid')
        )
        project.save()
        return redirect('buyerdashboard') 
    return render(request, 'buyer/add_project.html')
def view_posted_projects(request):
    user_id=request.session.get('userid')
    projects = models.Project.objects.filter(userid=user_id)
    return render(request, 'view_posted_projects.html', {'projects': projects})

def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('index')