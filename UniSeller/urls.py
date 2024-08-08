"""
URL configuration for unilancers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from UniSeller import views
urlpatterns = [
    path('',views.index,name='index'),
    path('sellerlogin',views.SellerLogin,name='sellerlogin'),
    path('sellerlogindata',views.SellerLoginData,name='sellerlogindata'),
    path('sellersignup',views.SellerSignUp,name='sellersignup'),
    path('sellersignupdata',views.SellerSingUpData,name='sellersignupdata'),
    path('confirmation',views.confirmation,name='confirmation'),
    path('main',views.SellerDashboard,name='main'),
    path('logout',views.logout_view,name='logout'),
    path('projectdetails',views.ProjectDetails,name='projectdetails'),
    path('profile',views.Profile,name='profile'),
    path('tokenpage', views.TokenPage, name='tokenPage'),
]
