
from django.urls import path
from UniSeller import views
urlpatterns = [
    path('',views.index,name='index'),
    path('subscription',views.Subscription,name='subscription'),
    path('sellerlogin',views.SellerLogin,name='sellerlogin'),
    path('sellersignup',views.SellerSignUp,name='sellersignup'),
    path('confirmation',views.confirmation,name='confirmation'),
    path('main',views.SellerDashboard,name='main'),
    path('logout',views.logout_view,name='logout'),
    path('projectdetails/<str:projectname>/',views.ProjectDetails,name='projectdetails'),
    path('projectdetailsadd/<str:projectname>/', views.ProjectDetailsAdd, name='projectdetailsadd'),
    path('profile',views.Profile,name='profile'),
    path('tokenpage', views.TokenPage, name='tokenPage'),
    path('paymentpage', views.PaymentCard, name='paymentpage'),
    path('gigcreate',views.CreateGig,name='gigcreate'),
    path('sellerviewgigs/<int:id>/',views.ViewGig,name='sellerviewgigs'),
    path('sellergigdelete/<int:id>/',views.GigDelete,name='sellergigdelete'),
    path('messagepage',views.MessagePage,name='messagepage'),
    path('withdraw_project/<int:projectid>',views.Withdraw_project, name='withdraw_project'),
    path('SellerFeedback',views.SellerFeedback,name='SellerFeedback'),
]
