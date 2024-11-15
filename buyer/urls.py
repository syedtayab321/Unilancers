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
from django.contrib import admin
from django.urls import path,include
from zope.interface import named

from buyer import views

urlpatterns = [
  path('buyerlogin/',views.buyerlogin, name="buyerlogin" ),
  path('signup/',views.buyersignup, name="signup"),
  path('buyerdashboard/',views.buyerdashboard , name="buyerdashboard"),
  path('add-project/', views.add_project, name='add_project'),
  path('view-posted-projects/', views.view_posted_projects, name='view_posted_projects'),
  path('buyerlogout/', views.logout_view, name='buyerlogout'),
  path('requestApproval/<int:id>',views.RequestApproval,name='requestApproval'),
  path('requestRejection/<int:id>',views.RequestRejection,name='requestRejection'),
  path('postedprojectdelete/<int:id>',views.PostedProjectDelete,name='postedprojectdelete'),
  path('viewgigs/<int:sellerid>',views.ViewGigs, name="viewgigs"),
  path('payment_view',views.payment_view,name='payment_view'),
  path('payment_success',views.payment_success,name='payment_success'),
  path('payment_failed',views.payment_failed,name='payment_failed'),
path('BuyerFeedback',views.BuyerFeedback,name='BuyerFeedback'),
]
