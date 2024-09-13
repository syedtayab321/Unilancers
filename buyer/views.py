from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
import requests
from django.shortcuts import render, redirect,get_object_or_404
from buyer import models
from UniSeller import models as sellermodel
import stripe
from django.conf import settings
from django.urls import reverse
from .models import Payment

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
                    request.session['userid']=user.user_id
                    request.session['user_role']='buyer'
                    return redirect('buyerdashboard')
                else:
                    return render(request, 'buyersignup.html', {'error': 'Invalid username or password'})
            except Exception as e:
                return HttpResponse('wrong cridentials')
        return render(request,'buyersignup.html')
    return redirect('buyerdashboard')

def buyersignup(request):
    if request.session.get("buyeremail") is None:
        if request.method == "POST":
            name = request.POST.get("name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            try:
                User.objects.get(email=email)
                return HttpResponse("User already exists")
            except:
                users = User.objects.create_user(
                    username=name,  # Use email as username
                    password=password,
                    email=email
                )
                user = models.Buyersignup(user=users,name=name, email=email, password=password)
                user.save()
                return HttpResponse("Data created sucessfully")
        return render(request,'buyersignup.html')
    else:
        return redirect('buyerdashboard')

def buyerdashboard(request):
    user_id = request.session.get('userid')
    if not user_id:
        return HttpResponse('User ID not found in session', status=400)
    try:
        data = sellermodel.ProjectAppliedModal.objects.filter(posted_by=user_id)
        sellerdata=sellermodel.SellerSignUpModal.objects.all()
        active_projects=sellermodel.ProjectAppliedModal.objects.filter(posted_by=user_id,status='Approved')
        return render(request, 'buyerdashboard.html', {'data': data,'sellerdata':sellerdata,'active_projects':active_projects})
    except sellermodel.ProjectAppliedModal.DoesNotExist:
        sellerdata = sellermodel.SellerSignUpModal.objects.all()
        active_projects = sellermodel.ProjectAppliedModal.objects.filter(posted_by=user_id, status='Approved')
        return render(request, 'buyerdashboard.html', {'data': [],'sellerdata':sellerdata,'active_projects':active_projects})
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

def RequestApproval(request,id):
    data=sellermodel.ProjectAppliedModal.objects.filter(id=id)
    userdata=sellermodel.SellerSignUpModal.objects.filter(id=id)
    if data:
        sellermodel.ProjectAppliedModal.objects.filter(id=id).update(status='Approved')
        # Send an email to notify the user of approval
        subject = 'Your Project Request Has Been Approved!'
        message = f"Dear {userdata.username},\n\nYour Request for the  project '{data.project_name}' has been approved. You can now check your dashboard for further details.\n\nBest regards,\nUnilancers Team"
        recipient_email = userdata.university_email

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # The sender email address from settings
            [recipient_email],  # The recipient email
            fail_silently=False,  # Raise an error if the email fails
        );
        return redirect('buyerdashboard')
    else:
        return HttpResponse('No data found')

def RequestRejection(request,id):
    data=sellermodel.ProjectAppliedModal.objects.filter(id=id)
    if data:
        sellermodel.ProjectAppliedModal.objects.filter(id=id).update(status='Rejected')
        return redirect('buyerdashboard')
    else:
        return HttpResponse('No data found')

def PostedProjectDelete(request,id):
    data=models.Project.objects.filter(id=id)
    if data:
        models.Project.objects.filter(id=id).delete()
        return redirect('view_posted_projects')
    else:
        return HttpResponse('No data found')

def ViewGigs(request,sellerid):
    gigsdata=sellermodel.GigDataModal.objects.filter(seller_id=sellerid)
    return render(request,'buyer/templates/Components/GigsDetails.html',{'gigsdata':gigsdata})

# payment processing here
stripe.api_key = settings.STRIPE_SECRET_KEY
def payment_view(request):
    if request.method == 'POST':
        client_name = request.POST['client_name']
        amount = float(request.POST['amount'])
        currency = 'GBP'  # You can change this to other currencies

        # Create a Stripe charge
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),  # Stripe expects the amount in cents/pence
                currency=currency,
                source=request.POST['stripeToken'],
                description=f'Payment by {client_name}',
            )

            # Save the payment details in the database
            payment = Payment(
                client_name=client_name,
                amount=amount,
                currency=currency,
                stripe_charge_id=charge.id,
            )
            payment.save()

            return redirect('payment_success')

        except stripe.error.StripeError as e:
            return render(request, 'ProjectPayment.html', {'error': str(e)})

    return render(request, 'ProjectPayment.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def payment_success(request):
    return render(request, 'payments/payment_success.html')
def payment_failed(request):
    return render(request, 'payments/payment_failed.html')


def BuyerFeedback(request):
    buyer_email = request.session.get('buyeremail')
    BuyerData = models.Buyersignup.objects.get(email=buyer_email)
    if request.method == 'POST':
        message = request.POST['message']
        feedback = models.BuyerFeedback.objects.create(
            buyername=BuyerData.name,
            buyeremail=BuyerData.email,
            buyermessage=message,
        )
        return redirect('BuyerFeedback')
    return render(request, 'BuyerFeedback.html', {'BuyerData': BuyerData})
