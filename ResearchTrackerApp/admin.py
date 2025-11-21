from django.contrib import admin
from .models import Research

# Register your models here.

@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ('Research_ID', 'Research_Title', 'Author', 'Status','Date_Presented', 'Date_Ongoing', 'Date_Conducted', 'Date_Published','Document_File')
    