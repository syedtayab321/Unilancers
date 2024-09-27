from django.shortcuts import render

# Create your views here.
def BuyerMessage(request):
    return render(request,'BuyerMessage.html')