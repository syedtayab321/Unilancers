import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from UniSeller import models
from buyer import  models as buyer_models
from django.core.mail import send_mail
import random
import string
from datetime import datetime

# Create your views here.
def index(request):
    return render(request, 'index.html')


#seller login related
def SellerLogin(request):
    if 'email' in request.session:
        return redirect('main')
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = models.SellerSignUpModal.objects.get(university_email=email)
            if user.password == password:
                request.session['email'] = email
                request.session['username'] = user.username
                request.session['sellerId'] = user.id
                return redirect('main')
            else:
                return render(request, 'SellerLogin.html', {'passworderror': 'Wrong password'})
        except models.SellerSignUpModal.DoesNotExist:
            return render(request, 'SellerLogin.html', {'emailerror': 'Email does not exist'})
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    return render(request, 'SellerLogin.html')


#seller singup related
def generate_verification_code(length=6):
    digits = string.digits
    return ''.join(random.choice(digits) for i in range(length))


def SellerSignUp(request):
    if request.method == "POST":
        try:
            verification_code = generate_verification_code()
            profile = request.FILES.get('profile')
            username = request.POST.get('username')
            university_email = request.POST.get('university_email')
            university_name = request.POST.get('university_name')
            mobile_phone = request.POST.get('mobile_phone')
            university_reg_no = request.POST.get('university_reg_no')
            study_field = request.POST.get('field_of_study')
            skills = request.POST.get('skills')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            # Check if the email already exists
            try:
                user = models.SellerSignUpModal.objects.get(university_email=university_email)
                data = {'emailerror': 'Email already exists'}
                return render(request, 'sellerSignup.html', data)
            except:
                if password == confirm_password:
                    models.SellerSignUpModal.objects.create(
                        username=username,
                        profile_picture=profile,
                        university_email=university_email,
                        university_name=university_name,
                        mobile_no=mobile_phone,
                        registration_number=university_reg_no,
                        study_field=study_field,
                        skills=skills,
                        password=password,
                        verification_code=verification_code
                    )
                    subject = 'Account Verification Code'
                    message = f"""
                       Dear {username},
                       Your verification code is {verification_code}.
                       Thank you for signing up.
                       """
                    send_mail(subject, message, 'adminemail@gmail.com', [university_email])
                    context = {'university_email': university_email}
                    return render(request, 'confirmationpage.html', context)
                else:
                    data = {'error': 'Passwords do not match'}
                    return render(request, 'sellerSignup.html', data)
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")
    return render(request, 'sellerSignup.html')


def confirmation(request):
    if request.method == 'POST':
        email = request.POST['university_email']
        verification_code = request.POST['verification_code']

        # Fetch all users with the given university email
        users = models.SellerSignUpModal.objects.filter(university_email=email)

        # Initialize the context with an error message
        data = {
            'error': 'Please enter the correct verification code',
        }

        # Check if any user has the correct verification code
        for user in users:
            if user.verification_code == verification_code:
                request.session['email'] = email
                request.session['username'] = user.username
                request.session['sellerId'] = user.id
                return redirect('main')

        # If no match is found, render the confirmation page with the error message
        return render(request, 'confirmationpage.html', data)

    return render(request, 'confirmationpage.html')


def SellerDashboard(request):
    # gigs data
    gig_data = models.GigDataModal.objects.all()
    # applied projects data
    applied_projects = models.ProjectAppliedModal.objects.all()
    # active project
    active_projects = models.ProjectAppliedModal.objects.filter(status='Approved')
    today = datetime.now().date()
    for project in active_projects:
        end_date = project.Date_to
        if end_date:
            project.remaining_days = (end_date - today).days
        else:
            project.remaining_days = None
    #posted projects
    posted_project=buyer_models.Project.objects.all()
    return render(request, 'Dashboard/Main.html', {'projectdata':applied_projects,'gigdata':gig_data,'PostedProjects':posted_project,'active_projects':active_projects})


def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('index')


def ProjectDetails(request,projectname):
     data=buyer_models.Project.objects.get(project_name=projectname)
     return render(request, 'Dashboard/ProjectRelated/ProjectDetails.html',{'data':data})

def ProjectDetailsAdd(request,projectname):
    data = buyer_models.Project.objects.get(project_name=projectname)
    if request.method == 'POST':
            project_name = data.project_name
            posted_by=data.userid
            seller_id = request.POST.get('seller_id')
            project_price = request.POST.get('project_price')
            project_token = request.POST.get('project_token')
            date_from = request.POST.get('date_from')
            date_to = request.POST.get('date_to')
            cover_letter = request.POST.get('cover_letter')
            try:
                models.ProjectAppliedModal.objects.create(
                    project_name=project_name,
                    posted_by=posted_by,
                    seller_id=seller_id,
                    project_price=project_price,
                    project_tokens=project_token,
                    Date_from=date_from,
                    Date_to=date_to,
                    cover_letter=cover_letter,
                    status='pending'
                )
                return HttpResponse('Project Applied Successfully')
            except Exception as e:
                return HttpResponse(e)
    return render(request, 'Dashboard/ProjectRelated/ProjectApplyModal.html',{'data':data})


def Profile(request):
    if request.method == "POST":
        profile_picture = request.FILES.get('image')
        username = request.POST.get('username')
        university_email = request.POST.get('university_email')
        university_name = request.POST.get('university_name')
        mobile_phone = request.POST.get('mobile_phone')
        university_reg_no = request.POST.get('university_reg_no')
        study_field = request.POST.get('field_of_study')
        skills = request.POST.get('skills')

        try:
            # Ensure we fetch the existing user to update their information
            user = models.SellerSignUpModal.objects.get(university_email=university_email)

            # Update fields, including profile picture if provided
            user.username = username
            user.profile_picture = profile_picture if profile_picture else user.profile_picture
            user.university_email = university_email
            user.university_name = university_name
            user.mobile_no = mobile_phone
            user.registration_number = university_reg_no
            user.study_field = study_field
            user.skills = skills
            user.save()

            # Fetch updated user data
            userdata = models.SellerSignUpModal.objects.get(university_email=university_email)
            return render(request, 'Dashboard/ProfileUpdate.html', {'userdata': userdata})
        except models.SellerSignUpModal.DoesNotExist:
            return HttpResponse('User not found', status=404)
        except Exception as e:
            return HttpResponse(f'An error occurred: {e}')

    email = request.session.get('email')
    if not email:
        return HttpResponse('No email in session', status=400)

    try:
        userdata = models.SellerSignUpModal.objects.get(university_email=email)
        return render(request, 'Dashboard/ProfileUpdate.html', {'userdata': userdata})
    except models.SellerSignUpModal.DoesNotExist:
        return HttpResponse('User not found', status=404)


def TokenPage(request):
    return render(request, 'Dashboard/TokenRelated/BidTokens.html')


def CreateGig(request):
    if request.method == 'POST':
        sellerId = request.POST.get('SellerId')
        gig_title = request.POST.get('gigTitle')
        gig_field = request.POST.get('gigField')
        gig_subfield = request.POST.get('gigSubField')
        gig_description = request.POST.get('gigDescription')
        gig_image1 = request.FILES.get('gigImage1')
        gig_image2 = request.FILES.get('gigImage2')
        gig_image3 = request.FILES.get('gigImage3')
        totalgigs = models.GigDataModal.objects.filter(seller_id=sellerId)
        try:
           if len(totalgigs) <= 4:
               new_gig = models.GigDataModal.objects.create(
                   seller_id=sellerId,
                   gig_title=gig_title,
                   field=gig_field,
                   sub_field=gig_subfield,
                   description=gig_description,
                   gig_image1=gig_image1,
                   gig_image2=gig_image2,
                   gig_image3=gig_image3,
               )
               return redirect('main')
           else:
               return HttpResponse('You can only add 4 gig samples not more than that')
        except Exception as e:
            return HttpResponse(f'Error: {e}')

    return render(request, 'Dashboard/ManageGigs/CreateGig.html')


def ViewGig(request, id):
    gigdata = models.GigDataModal.objects.get(id=id)
    return render(request, 'Dashboard/ManageGigs/ViewGigsDetails.html', {'gigdata': gigdata})


def GigDelete(request, id):
    try:
        gig = models.GigDataModal.objects.get(id=id)
        gig.gig_image1.delete(save=False)
        gig.gig_image2.delete(save=False)
        gig.gig_image3.delete(save=False)
        gig.delete()
        return redirect('main')
    except models.GigDataModal.DoesNotExist:
        return HttpResponse('Gig not found', status=404)

def PaymentCard(request):
    return render(request,'Dashboard/TokenRelated/Payment.html')

def MessagePage(request):
    return render(request,'Dashboard/ManageMessages/Messages.html')