from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Message

def chat_room(request, seller_id, buyer_id):
    user_role = request.session.get('user_role')

    # Check if user role is set in session
    if user_role is None:
        return HttpResponse("User role not set. Please log in.")

    try:
        # Fetch User instances
        seller = User.objects.get(id=seller_id)
        buyer = User.objects.get(id=buyer_id)

        # Determine the role of the current user
        if user_role == 'seller':
            # The current user is a seller
            receiver = buyer
        elif user_role == 'buyer':
            # The current user is a buyer
            receiver = seller
        else:
            return HttpResponse("User role not recognized")

        # Fetch messages between the seller and buyer
        messages = Message.objects.filter(
            (Q(sender=seller) & Q(receiver=buyer)) |
            (Q(sender=buyer) & Q(receiver=seller))
        ).order_by('timestamp')

        return render(request, 'chat/room.html', {
            'seller': seller,
            'buyer': buyer,
            'messages': messages,
            'receiver_id': receiver.id,
            'current_user_role': user_role,
        })

    except User.DoesNotExist:
        return HttpResponse("User does not exist")
