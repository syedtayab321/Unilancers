from django.contrib import admin
from .models import SellerSignUpModal, ProjectAppliedModal, GigDataModal, ChatRoom, Message, SellerFeedback

# Register SellerSignUpModal
@admin.register(SellerSignUpModal)
class SellerSignUpModalAdmin(admin.ModelAdmin):
    list_display = ('username', 'university_email', 'mobile_no', 'university_name', 'registration_number', 'study_field', 'skills', 'Date', 'password')
    search_fields = ('username', 'university_email')
    list_filter = ('Date',)

# Register ProjectAppliedModal
@admin.register(ProjectAppliedModal)
class ProjectAppliedModalAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'posted_by', 'seller_id', 'project_price', 'project_tokens', 'Date_from', 'Date_to', 'applied_date', 'cover_letter')
    search_fields = ('project_name', 'posted_by', 'seller_id')
    list_filter = ('applied_date', 'project_price')

# Register GigDataModal
@admin.register(GigDataModal)
class GigDataModalAdmin(admin.ModelAdmin):
    list_display = ('seller_id', 'gig_title', 'field', 'sub_field', 'description')
    search_fields = ('gig_title', 'field', 'sub_field')
    list_filter = ('field',)

# Register ChatRoom
@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'uniseller', 'buyer')
    search_fields = ('name', 'uniseller__username', 'buyer__username')
    list_filter = ('uniseller', 'buyer')

# Register Message
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender_is_seller', 'content', 'timestamp')
    search_fields = ('room__name', 'content')
    list_filter = ('timestamp', 'sender_is_seller')

# Register SellerFeedback
@admin.register(SellerFeedback)
class SellerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)
