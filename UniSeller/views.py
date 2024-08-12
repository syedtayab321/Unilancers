from django.http import HttpResponse
from django.shortcuts import render,redirect
from UniSeller import models
from django.core.mail import send_mail
import random
import string
# Create your views here.
def index(request):
     return render(request,'index.html')
#seller login related
def SellerLogin(request):
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
            return render(request, 'SellerLogin.html', {'emailerror': 'email did not exists'})
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
                    send_mail(subject, message, 'syedhussain4508@gmail.com', [university_email])
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
    gig_data=models.GigDataModal.objects.all()
    return render(request, 'Dashboard/Main.html',{'data':gig_data})


def logout_view(request):
    request.session.flush()  # Clear all session data
    return redirect('index')

def ProjectDetails(request):
    if request.method =='POST':
          try:
              project_name=request.POST.get('project_name')
              seller_id=request.POST.get('seller_id')
              project_price=request.POST.get('project_price')
              project_token=request.POST.get('project_token')
              date_from=request.POST.get('date_from')
              date_to=request.POST.get('date_to')
              cover_letter=request.POST.get('cover_letter')
              models.ProjectAppliedModal.objects.create(
                      project_name=project_name,
                      seller_id=seller_id,
                      project_price=project_price,
                      project_tokens=project_token,
                      Date_from=date_from,
                      Date_to=date_to,
                      cover_letter=cover_letter,
                  )
              return render(request,'Dashboard/main.html')
          except Exception as e:
              return HttpResponse(e)
    return render(request,'Dashboard/ProjectRelated/ProjectDetails.html')

def Profile(request):
    return render(request,'Dashboard/ProfileUpdate.html')

def TokenPage(request):
    return render(request,'Dashboard/BidTokens.html')

def CreateGig(request):
    if request.method == 'POST':
        sellerId = request.POST.get('SellerId')
        gig_title = request.POST.get('gigTitle')
        gig_field = request.POST.get('gigField')
        gig_subfield = request.POST.get('gigSubField')
        gig_description = request.POST.get('gigDescription')
        gig_price = request.POST.get('gigPrice')
        gig_image1 = request.FILES.get('gigImage1')
        gig_image2 = request.FILES.get('gigImage2')
        gig_image3 = request.FILES.get('gigImage3')
        try:
            user=models.GigDataModal.objects.create(
                seller_id=sellerId,
                gig_title=gig_title,
                field=gig_field,
                sub_field=gig_subfield,
                description=gig_description,
                gig_price=gig_price,
                gig_image1=gig_image1,
                gig_image2=gig_image2,
                gig_image3=gig_image3,
            )
            return HttpResponse('sucessfully register data')
        except Exception as e:
            return HttpResponse(e)
    return render(request,'Dashboard/ManageGigs/CreateGig.html')