from django.contrib import admin
from .models import Buyersignup, Project

# Define an admin class for Buyersignup
class BuyersignupAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'password')
    search_fields = ('name', 'email')
    ordering = ('name',)

# Define an admin class for Project
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'project_budget', 'project_deadline','project_requirements','project_description' ,'created_at', 'updated_at','userid')
    search_fields = ('project_name', 'project_description')
    list_filter = ('project_deadline',)
    ordering = ('-created_at',)

# Register the admin classes with the admin site
admin.site.register(Buyersignup, BuyersignupAdmin)
admin.site.register(Project, ProjectAdmin)
