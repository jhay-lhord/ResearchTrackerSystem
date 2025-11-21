from django.shortcuts import render, redirect
from .models import Research
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from datetime import date, timedelta, datetime
from django.db.models import F, Q
from django.urls import reverse
from django.views.generic import ListView
from .forms import ResearchForm, ResearchFileUploadForm, ResearchStatusUpdateForm, RegistrationForm, UserUpdateForm
from django.http import HttpResponseRedirect, JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json
import calendar
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.db import models, transaction, connection
from django.utils.translation import gettext_lazy as _
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView


app_name = 'ResearchTrackerApp'


# Create your views here.
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        return super().default(obj)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.success(request, ('Incorrect Username or Password'))
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def presented(request):
    submitted = False
    if request.method == 'POST':
        # Handle file upload for a specific research item
        research_id = request.POST.get('research_id')
        if research_id:
            print("Received Research ID:", research_id)
            try:
                research_id = int(research_id)
            except (ValueError, TypeError):
                raise Http404("Invalid Research ID")

            try:
                research = get_object_or_404(Research, Research_ID=research_id)
            except Http404:
                raise Http404("Research not found")
            fileUploadForm = ResearchFileUploadForm(request.POST, request.FILES, instance=research)
            if fileUploadForm.is_valid():
                fileUploadForm.save()
                return redirect('presented')
            
        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            print("Form is valid")
            print("Status:", form.cleaned_data['Status'])
            print("Date_Presented:", form.cleaned_data['Date_Presented'])
            print("Date_Ongoing:", form.cleaned_data['Date_Ongoing'])
            print("Date_Conducted:", form.cleaned_data['Date_Conducted'])
            print("Date_Published:", form.cleaned_data['Date_Published'])
            form.save()
            print('save')
            return HttpResponseRedirect("/dashboard/?submitted=True")

        else:
            print(form.errors)
    
    else:
        form = ResearchForm()
        if 'submitted' in request.GET:
            submitted = True
    # get data from the database where status is Presented
    research_presented = Research.objects.filter(Status="Presented").order_by('-created_at')
    print("result", research_presented)
    presented_result = None
    data = []
    for presented in research_presented:
        url = reverse('update_research', args=[presented.Research_ID])
        presentedItem = {
            'Research_ID': presented.Research_ID,
            'Research_Title': presented.Research_Title,
            'Author': presented.Author,
            'Status': presented.Status,
            'Date_Presented': presented.Date_Presented,
            'Date_Ongoing': presented.Date_Ongoing,
            'Date_Conducted': presented.Date_Conducted,
            'Date_Published': presented.Date_Published,
            'College': presented.College,
            'updated_at': presented.updated_at,
            'Document_File' : presented.Document_File,
            'updateUrl': request.build_absolute_uri(url),
        }
        data.append(presentedItem)
    presented_result = data
    print(presented_result)
    page_title = "Research Presented"

    # Count the number of every research status
    research_presented_count = Research.objects.filter(Status = "Presented").count()
    research_conducted_count = Research.objects.filter(Status = "Conducted").count()
    research_ongoing_count = Research.objects.filter(Status = "Ongoing").count()
    research_published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = research_presented_count + research_conducted_count + research_ongoing_count + research_published_count

    research_data_as_of_today = {
        'research_presented_count' : research_presented_count,
        'research_conducted_count' : research_conducted_count,
        'research_ongoing_count' : research_ongoing_count,
        'research_published_count' : research_published_count,
        'total_research_count' : total_research_count,
    }
    context = {
        "presented_result" : presented_result, 
        "form" : form, 
        "submitted": submitted, 
        "page_title": page_title,
        "research_data_as_of_today": research_data_as_of_today,
        }
    return render(request, 'presented.html', context )

def ongoing(request):
    submitted = False
    if request.method == 'POST':
        # Handle file upload for a specific research item
        research_id = request.POST.get('research_id')
        if research_id:
            print("Received Research ID:", research_id)
            try:
                research_id = int(research_id)
            except (ValueError, TypeError):
                raise Http404("Invalid Research ID")

            try:
                research = get_object_or_404(Research, Research_ID=research_id)
            except Http404:
                raise Http404("Research not found")
            fileUploadForm = ResearchFileUploadForm(request.POST, request.FILES, instance=research)
            if fileUploadForm.is_valid():
                fileUploadForm.save()
                return redirect('ongoing')

        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            print("Form is valid")
            print("Status:", form.cleaned_data['Status'])
            print("Date_Presented:", form.cleaned_data['Date_Presented'])
            print("Date_Ongoing:", form.cleaned_data['Date_Ongoing'])
            print("Date_Conducted:", form.cleaned_data['Date_Conducted'])
            print("Date_Published:", form.cleaned_data['Date_Published'])
            form.save()
            print('save')
            return HttpResponseRedirect("/dashboard/?submitted=True")   
        else:
            print(form.errors)

    else:
        form = ResearchForm()
        if 'submitted' in request.GET:
            submitted = True

    # get data from the database where Status is Ongoing
    research_ongoing = Research.objects.filter(Status="Ongoing").order_by('-created_at')
    ongoing_result = None
    data = []
    for ongoing in research_ongoing:
        url = reverse('update_research', args=[ongoing.Research_ID])
        ongoingItem = {
            'Research_ID': ongoing.Research_ID,
            'Research_Title': ongoing.Research_Title,
            'Author': ongoing.Author,
            'Status': ongoing.Status,
            'Date_Presented': ongoing.Date_Presented,
            'Date_Ongoing': ongoing.Date_Ongoing,
            'Date_Conducted': ongoing.Date_Conducted,
            'Date_Published': ongoing.Date_Published,
            'updated_at': ongoing.updated_at,
            'College': ongoing.College,
            'Document_File' : ongoing.Document_File,
            'updateUrl': request.build_absolute_uri(url),
        }
        data.append(ongoingItem)
    ongoing_result = data

    # Count the number of every research status
    research_presented_count = Research.objects.filter(Status = "Presented").count()
    research_conducted_count = Research.objects.filter(Status = "Conducted").count()
    research_ongoing_count = Research.objects.filter(Status = "Ongoing").count()
    research_published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = research_presented_count + research_conducted_count + research_ongoing_count + research_published_count

    research_data_as_of_today = {
        'research_presented_count' : research_presented_count,
        'research_conducted_count' : research_conducted_count,
        'research_ongoing_count' : research_ongoing_count,
        'research_published_count' : research_published_count,
        'total_research_count' : total_research_count,
    }

    page_title = "Research Ongoing"
    context = {
        "ongoing_result" : ongoing_result, 
        "form" : form, 
        "submitted" : submitted,
        "page_title": page_title,
        "research_data_as_of_today": research_data_as_of_today,
        }
    
    return render(request, 'ongoing.html', context)

def conducted(request):
    submitted = False
    if request.method == 'POST':
        # Handle file upload for a specific research item
        research_id = request.POST.get('research_id')
        if research_id:
            print("Received Research ID:", research_id)
            try:
                research_id = int(research_id)
            except (ValueError, TypeError):
                raise Http404("Invalid Research ID")

            try:
                research = get_object_or_404(Research, Research_ID=research_id)
            except Http404:
                raise Http404("Research not found")
            fileUploadForm = ResearchFileUploadForm(request.POST, request.FILES, instance=research)
            if fileUploadForm.is_valid():
                fileUploadForm.save()
                return redirect('conducted')

        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            print("Form is valid")
            print("Status:", form.cleaned_data['Status'])
            print("Date_Presented:", form.cleaned_data['Date_Presented'])
            print("Date_Ongoing:", form.cleaned_data['Date_Ongoing'])
            print("Date_Conducted:", form.cleaned_data['Date_Conducted'])
            print("Date_Published:", form.cleaned_data['Date_Published'])
            form.save()
            print('save')
            return HttpResponseRedirect("/dashboard/?submitted=True")
        else:
            print(form.errors)

    else:
        form = ResearchForm()
        if 'submitted' in request.GET:
            submitted = True
    

    # get data from the database where the Status is Conducted
    research_conducted = Research.objects.filter(Status="Conducted").order_by('-created_at')
    conducted_result = None
    data = []
    for conducted in research_conducted:
        url = reverse('update_research', args=[conducted.Research_ID])
        conductedItem = {
            'Research_ID': conducted.Research_ID,
            'Research_Title': conducted.Research_Title,
            'Author': conducted.Author,
            'Status': conducted.Status,
            'Date_Presented': conducted.Date_Presented,
            'Date_Ongoing': conducted.Date_Ongoing,
            'Date_Conducted': conducted.Date_Conducted,
            'Date_Published': conducted.Date_Published,
            'updated_at': conducted.updated_at,
            'College': conducted.College,
            'Document_File' : conducted.Document_File,
            'updateUrl': request.build_absolute_uri(url),
        }
        data.append(conductedItem)
    conducted_result = data

    # Count the number of every research status
    research_presented_count = Research.objects.filter(Status = "Presented").count()
    research_conducted_count = Research.objects.filter(Status = "Conducted").count()
    research_ongoing_count = Research.objects.filter(Status = "Ongoing").count()
    research_published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = research_presented_count + research_conducted_count + research_ongoing_count + research_published_count

    research_data_as_of_today = {
        'research_presented_count' : research_presented_count,
        'research_conducted_count' : research_conducted_count,
        'research_ongoing_count' : research_ongoing_count,
        'research_published_count' : research_published_count,
        'total_research_count' : total_research_count,
    }

    page_title = "Research Conducted"
    context = {
        "conducted_result" : conducted_result, 
        "form" : form, 
        "submitted" : submitted,
        "page_title": page_title,
        "research_data_as_of_today": research_data_as_of_today,
        }
    
    return render(request, 'conducted.html', context )

def published(request):
    submitted = False
    if request.method == 'POST':
        # Handle file upload for a specific research item
        research_id = request.POST.get('research_id')
        if research_id:
            print("Received Research ID:", research_id)
            try:
                research_id = int(research_id)
            except (ValueError, TypeError):
                raise Http404("Invalid Research ID")
            try:
                research = get_object_or_404(Research, Research_ID=research_id)
            except Http404:
                raise Http404("Research not found")
            fileUploadForm = ResearchFileUploadForm(request.POST, request.FILES, instance=research)
            if fileUploadForm.is_valid():
                fileUploadForm.save()
                return redirect('published')

        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            print("Form is valid")
            print("Status:", form.cleaned_data['Status'])
            print("Date_Presented:", form.cleaned_data['Date_Presented'])
            print("Date_Ongoing:", form.cleaned_data['Date_Ongoing'])
            print("Date_Conducted:", form.cleaned_data['Date_Conducted'])
            print("Date_Published:", form.cleaned_data['Date_Published'])
            form.save()
            print('save')
            return HttpResponseRedirect("/dashboard/?submitted=True")
        else:
            print(form.errors)

    else:
        form = ResearchForm()
        if 'submitted' in request.GET:
            submitted = True

    # get data from the database where status is Published
    research_published = Research.objects.filter(Status="Published").order_by('-created_at')
    published_result = None
    data = []
    for published in research_published:
        url = reverse('update_research', args=[published.Research_ID])
        publishedItem = {
            'Research_ID': published.Research_ID,
            'Research_Title': published.Research_Title,
            'Author': published.Author,
            'Status': published.Status,
            'Date_Presented': published.Date_Presented,
            'Date_Ongoing': published.Date_Ongoing,
            'Date_Conducted': published.Date_Conducted,
            'Date_Published': published.Date_Published,
            'updated_at': published.updated_at,
            'College': published.College,
            'Document_File' : published.Document_File,
            'updateUrl': request.build_absolute_uri(url),

        }
        data.append(publishedItem)
    published_result = data

    # Count the number of every research status
    research_presented_count = Research.objects.filter(Status = "Presented").count()
    research_conducted_count = Research.objects.filter(Status = "Conducted").count()
    research_ongoing_count = Research.objects.filter(Status = "Ongoing").count()
    research_published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = research_presented_count + research_conducted_count + research_ongoing_count + research_published_count

    research_data_as_of_today = {
        'research_presented_count' : research_presented_count,
        'research_conducted_count' : research_conducted_count,
        'research_ongoing_count' : research_ongoing_count,
        'research_published_count' : research_published_count,
        'total_research_count' : total_research_count,
    }

    page_title = "Research Published"
    context = {
        "published_result" : published_result, 
        "form" : form, 
        "submitted" : submitted,
        "page_title": page_title,
        "research_data_as_of_today": research_data_as_of_today,
        }
    return render(request, 'published.html', context)

def all_research(request):
    submitted = False
    if request.method == 'POST':
        # Handle file upload for a specific research item
        research_id = request.POST.get('research_id')
        if research_id:
            print("Received Research ID:", research_id)
            try:
                research_id = int(research_id)
            except (ValueError, TypeError):
                raise Http404("Invalid Research ID")

            try:
                research = get_object_or_404(Research, Research_ID=research_id)
            except Http404:
                raise Http404("Research not found")
            fileUploadForm = ResearchFileUploadForm(request.POST, request.FILES, instance=research)
            if fileUploadForm.is_valid():
                fileUploadForm.save()
                return redirect('all_research')  # Redirect to the research list page

        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():         
            form.save()
            return HttpResponseRedirect("/all_research/?submitted=True")

    else:
        form = ResearchForm()
        if 'submitted' in request.GET:
            submitted = True
    # Get all data from the database
    all_research_data = Research.objects.values().order_by('-created_at')
    data = []
    for research in all_research_data:
        url = reverse('update_research', args=[research['Research_ID']])
        
        updated_at = "None"
        if(research['updated_at']):
            updated_at = research['updated_at'].strftime('%b. %d, %Y, %I:%M %p')
        
        researchItem = {
            'Research_ID': research['Research_ID'],
            'Research_Title': research['Research_Title'],
            'Author': research['Author'],
            'Status': research['Status'],
            'College': research['College'],
            'created_at': research['created_at'].strftime('%Y-%m-%d'),
            'updated_at': updated_at,
            "update_url": request.build_absolute_uri(url), 
            'Document_File': research['Document_File']
        }
        data.append(researchItem)
    all_research_data_json = json.dumps(data, cls=DjangoJSONEncoder)

    # Count the number of every research status
    research_presented_count = Research.objects.filter(Status = "Presented").count()
    research_conducted_count = Research.objects.filter(Status = "Conducted").count()
    research_ongoing_count = Research.objects.filter(Status = "Ongoing").count()
    research_published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = research_presented_count + research_conducted_count + research_ongoing_count + research_published_count

    research_data_as_of_today = {
        'research_presented_count' : research_presented_count,
        'research_conducted_count' : research_conducted_count,
        'research_ongoing_count' : research_ongoing_count,
        'research_published_count' : research_published_count,
        'total_research_count' : total_research_count,
    }

    page_title = "All Research"
    context = {
        "all_research_data_json": all_research_data_json, 
        "form" : form, 
        "submitted" : submitted,
        "page_title": page_title,
        "research_data_as_of_today": research_data_as_of_today,
        }

    return render(request, 'all-research.html', context)

def update_research(request, research_id):
    submitted = False
    research = get_object_or_404(Research, Research_ID=research_id)

    if request.method == 'POST':

        # for updating the status
        selected_status = request.POST.get('status')

        presented_date = request.POST.get('date_Presented')
        conducted_date = request.POST.get('date_Conducted')
        ongoing_date = request.POST.get('date_Ongoing')
        published_date = request.POST.get('date_Published')
        ispn_No = request.POST.get('ispn_No')
        publisher_name = request.POST.get('publisher_Name')
        journal_type = request.POST.get('Journal_Type')
        journal_index = request.POST.get('journal_Index')
        print('journal type', journal_type)

        if selected_status is not None:
            research.Status = selected_status
            print("status saved", selected_status)
        if presented_date is not None:
            research.Date_Presented = presented_date
            print("date presented saved", presented_date )
        if conducted_date is not None:
            research.Date_Conducted = conducted_date
            print("date conducted saved", conducted_date)
        if ongoing_date is not None:
            research.Date_Ongoing = ongoing_date
            print("date conducted saved", ongoing_date)
        if published_date is not None:
            research.Date_Published = published_date
            print("date published saved", published_date)
        if ispn_No is not None:
            research.ispnNo = ispn_No
            print("ispn No", ispn_No)
        if publisher_name is not None:
            research.Publisher_Name = publisher_name
            print("publisher Name", publisher_name)
        if journal_type is not None:
            research.Journal_Type = journal_type
            print("Journal Type", journal_type)
        if journal_index is not None:
            research.Journal_Index = journal_index
            print("Journal Index", journal_index)


        research.updated_at = datetime.now()
        research.save()
        print("research saved")
        return redirect('update_research', research_id=research_id)

        # for adding Research Information
        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            print("Form is valid")
            print("Status:", form.cleaned_data['Status'])
            print("Date_Presented:", form.cleaned_data['Date_Presented'])
            print("Date_Ongoing:", form.cleaned_data['Date_Ongoing'])
            print("Date_Conducted:", form.cleaned_data['Date_Conducted'])
            print("Date_Published:", form.cleaned_data['Date_Published'])
            form.save()
            print('save')
            return HttpResponseRedirect("/dashboard/?submitted=True")

        else:
            print(form.errors)
    else:
        form = ResearchForm()
        if 'submitted' in request.GET:
            submitted = True

    # Count the number of every research status
    research_presented_count = Research.objects.filter(Status = "Presented").count()
    research_conducted_count = Research.objects.filter(Status = "Conducted").count()
    research_ongoing_count = Research.objects.filter(Status = "On-going").count()
    research_published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = research_presented_count + research_conducted_count + research_ongoing_count + research_published_count

    research_data_as_of_today = {
        'research_presented_count' : research_presented_count,
        'research_conducted_count' : research_conducted_count,
        'research_ongoing_count' : research_ongoing_count,
        'research_published_count' : research_published_count,
        'total_research_count' : total_research_count,
    }

    page_title = 'Research Details'
    context = {
        'research' : research, 
        "form" : form, 
        "submitted" : submitted,
        "page_title" : page_title,
        "research_data_as_of_today": research_data_as_of_today, 
         }

    return render(request, 'update_research.html', context )

@login_required
def dashboard(request):
    submitted = False
    if request.method == "POST":
        print("form posted")
        research_id = request.POST.get('research_id')
        if research_id:
            print("Received Research ID:", research_id)
            try:
                research_id = int(research_id)
            except (ValueError, TypeError):
                raise Http404("Invalid Research ID")

            try:
                research = get_object_or_404(Research, Research_ID=research_id)
            except Http404:
                raise Http404("Research not found")
            fileUploadForm = ResearchFileUploadForm(request.POST, request.FILES, instance=research)
            if fileUploadForm.is_valid():
                fileUploadForm.save()
                return redirect('dashboard')

        form = ResearchForm(request.POST, request.FILES)
        if form.is_valid():
            print('valid')
            print("Form is valid")
            print("Status:", form.cleaned_data['Status'])
            print("Date_Presented:", form.cleaned_data['Date_Presented'])
            print("Date_Ongoing:", form.cleaned_data['Date_Ongoing'])
            print("Date_Conducted:", form.cleaned_data['Date_Conducted'])
            print("Date_Published:", form.cleaned_data['Date_Published'])
            form.save()
            print('save')
            return HttpResponseRedirect("/dashboard/?submitted=True")
        else:
            print(form.errors)
        
    else:
        form = ResearchForm()
        if 'submitted' in request.GET:
            submitted = True
    # Count the number of every research status
    research_presented_count = Research.objects.filter(Status = "Presented").count()
    research_conducted_count = Research.objects.filter(Status = "Conducted").count()
    research_ongoing_count = Research.objects.filter(Status = "Ongoing").count()
    research_published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = research_presented_count + research_conducted_count + research_ongoing_count + research_published_count

    research_data_as_of_today = {
        'research_presented_count' : research_presented_count,
        'research_conducted_count' : research_conducted_count,
        'research_ongoing_count' : research_ongoing_count,
        'research_published_count' : research_published_count,
        'total_research_count' : total_research_count,
    }
    end_date = date.today()
    
    date_labels = []
    conducted_data = []
    presented_data = []
    ongoing_data = []
    published_data = []

    # Calculate the labels for the past five months
    for i in range(5):
        
        last_day_of_month = end_date.replace(day=calendar.monthrange(end_date.year, end_date.month)[1])
        first_day_of_month = end_date.replace(day=1)
        label = first_day_of_month.strftime("%B %Y")
        date_labels.append(label)

        presented_count = Research.objects.filter(Status="Presented", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()
        conducted_count = Research.objects.filter(Status="Conducted", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()
        ongoing_count = Research.objects.filter(Status="Ongoing", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()
        published_count = Research.objects.filter(Status="Published", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()


        presented_data.append(presented_count)
        conducted_data.append(conducted_count)
        ongoing_data.append(ongoing_count)
        published_data.append(published_count)

        end_date = end_date - timedelta(days=end_date.day)

    date_labels
    presented_data.reverse()
    conducted_data.reverse()
    ongoing_data.reverse()
    published_data.reverse()

    research_data_in_five_months = {
        "labels": date_labels,
        "presented": presented_data,
        "conducted": conducted_data,
        "ongoing": ongoing_data,
        "published": published_data,
    }
    research_data_json = json.dumps(research_data_in_five_months)
    print(research_data_json)


    # get data from the database for the past 1 month for recently added
    month_ago = timezone.now() - timedelta(days=30)
    recent_research = Research.objects.filter(created_at__gte=month_ago).order_by('-created_at')
    recent_result = None
    recent_data = []

    for recent in recent_research:
        url = reverse('update_research', args=[recent.Research_ID])
        recentItem = {
            'Research_ID': recent.Research_ID,
            'Research_Title': recent.Research_Title,
            'Author': recent.Author,
            'Status': recent.Status,
            'Date_Presented': recent.Date_Presented,
            'Date_Ongoing': recent.Date_Ongoing,
            'Date_Conducted': recent.Date_Conducted,
            'Date_Published': recent.Date_Published,
            'updated_at': recent.updated_at,
            'College': recent.College,
            'Document_File' : recent.Document_File,
            'updateUrl': request.build_absolute_uri(url),
        }
        recent_data.append(recentItem)
    recent_result = recent_data
    page_title = "Dashboard"
    context = {
        "research_data_json" : research_data_json,
        "research_data_as_of_today" : research_data_as_of_today,
        "recent_result": recent_result, 
        "form" : form,
        "submitted": submitted,
        "page_title": page_title,
        }

    return render(request, 'dashboard.html', context)

def delete_file(request, research_id):
    try:
        research = Research.objects.get(Research_ID=research_id)
        if research.Document_File:
            research.Document_File.delete() 
        return redirect('all_research')   
    except Research.DoesNotExist:
        print("error")

def research_reports(request):
    end_date = date.today()
    
    date_labels = []
    conducted_data = []
    presented_data = []
    ongoing_data = []
    published_data = []

    # Calculate the labels for the past five months
    for i in range(5):
        
        last_day_of_month = end_date.replace(day=calendar.monthrange(end_date.year, end_date.month)[1])
        first_day_of_month = end_date.replace(day=1)
        label = first_day_of_month.strftime("%B %Y")
        date_labels.append(label)

        presented_count = Research.objects.filter(Status="Presented", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()
        conducted_count = Research.objects.filter(Status="Conducted", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()
        ongoing_count = Research.objects.filter(Status="Ongoing", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()
        published_count = Research.objects.filter(Status="Published", created_at__gte=first_day_of_month, created_at__lte=last_day_of_month).count()


        presented_data.append(presented_count)
        conducted_data.append(conducted_count)
        ongoing_data.append(ongoing_count)
        published_data.append(published_count)

        end_date = end_date - timedelta(days=end_date.day)

    date_labels
    presented_data.reverse()
    conducted_data.reverse()
    ongoing_data.reverse()
    published_data.reverse()

    research_data_in_five_months = {
        "labels": date_labels,
        "presented": presented_data,
        "conducted": conducted_data,
        "ongoing": ongoing_data,
        "published": published_data,
    }
    research_data_json = json.dumps(research_data_in_five_months)
    print(research_data_json)

    # Count the number of every research status
    presented_count = Research.objects.filter(Status = "Presented").count()
    conducted_count = Research.objects.filter(Status = "Conducted").count()
    ongoing_count = Research.objects.filter(Status = "Ongoing").count()
    published_count = Research.objects.filter(Status = "Published").count()
    total_research_count = presented_count + conducted_count + ongoing_count + published_count

    presented_percentage = None
    presented_rounded = None
    conducted_percentage = None
    conducted_rounded = None
    ongoing_percentage = None
    ongoing_rounded = None
    conducted_percentage = None
    conducted_rounded =None
    published_percentage = None
    published_rounded = None

    if (total_research_count):
        if(presented_count):
            presented_percentage ="{:.2f}".format(presented_count / total_research_count * 100)
            presented_rounded = (presented_count / total_research_count)
        if(conducted_count):
            conducted_percentage ="{:.2f}".format(conducted_count / total_research_count * 100)
            conducted_rounded = (conducted_count / total_research_count)
        if(ongoing_count):
            ongoing_percentage = "{:.2f}".format(ongoing_count / total_research_count * 100)
            ongoing_rounded = (ongoing_count / total_research_count)
        if(published_count):
            published_percentage = "{:.2f}".format(published_count / total_research_count * 100)
            published_rounded = (published_count / total_research_count)
        
    print(presented_rounded, ongoing_rounded, published_rounded, conducted_rounded)

    print(presented_percentage, conducted_percentage, ongoing_percentage, published_percentage, total_research_count)


    research = {
        'presented_count' : presented_count,
        'conducted_count' : conducted_count,
        'ongoing_count' : ongoing_count,
        'published_count' : published_count,
        'total_research_count' : total_research_count,
        'presented_percentage' : presented_percentage,
        'conducted_percentage': conducted_percentage,
        'ongoing_percentage': ongoing_percentage,
        'published_percentage': published_percentage,
        

    }
    research_json = json.dumps(research)
    context = {
        'research_json': research_json,
        'research_data_json': research_data_json,
        'presented_percentage' : presented_percentage,
        'conducted_percentage': conducted_percentage,
        'ongoing_percentage': ongoing_percentage,
        'published_percentage': published_percentage,
        'presented_rounded': presented_rounded,
        'conducted_rounded': conducted_rounded,
        'ongoing_rounded': ongoing_rounded,
        'published_rounded': published_rounded,
        'total_research_count': total_research_count,
        }
    return render(request, 'research-reports.html', context)

@login_required
def user_account(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            print("user updated")
            return redirect('user_account')  # Change 'profile' to the name of your profile view
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'user-account.html', {'form': form})

def ongoing_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    all_ongoing_data = Research.objects.filter(Status = "Ongoing")

    # Create table data
    ongoing_data = [['Research ID', 'Research Title', 'Author', 'Status', 'College']]
    for ongoing in all_ongoing_data:
        ongoing_data.append([ongoing.Research_ID, ongoing.Research_Title, ongoing.Author,  ongoing.Status, ongoing.College])

    # Create a table and set its style
    table = Table(ongoing_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Other rows background color
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Cell borders
    ]))

    styles = getSampleStyleSheet()

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,
        spaceAfter=30,
    )
    title = "Research Ongoing Details"
    elements.append(Paragraph(title, h2_style))
    elements.append(table)


    # Build the PDF document
    doc.build(elements)

    buffer.seek(0)

    # Return the PDF as a response
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="ongoing_report.pdf"'

    response['Content-Title'] = 'PDF Reports'
    return response

# conducted pdf
def conducted_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    all_conducted_data = Research.objects.filter(Status = "Conducted")

    # Create table data
    conducted_data = [['Research ID', 'Research Title', 'Author', 'Status', 'College']]
    for conducted in all_conducted_data:
        conducted_data.append([conducted.Research_ID, conducted.Research_Title, conducted.Author,  conducted.Status, conducted.College])

    # Create a table and set its style
    table = Table(conducted_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Other rows background color
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Cell borders
    ]))

    styles = getSampleStyleSheet()

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,
        spaceAfter=30,
    )
    title = "Research Conducted Details"
    elements.append(Paragraph(title, h2_style))
    elements.append(table)


    # Build the PDF document
    doc.build(elements)

    buffer.seek(0)

    # Return the PDF as a response
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="conducted_report.pdf"'

    response['Content-Title'] = 'PDF Reports'
    return response

# presented pdf
def presented_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    all_presented_data = Research.objects.filter(Status = "Presented")

    # Create table data
    presented_data = [['Research ID', 'Research Title', 'Author', 'Status', 'College']]
    for presented in all_presented_data:
        presented_data.append([presented.Research_ID, presented.Research_Title, presented.Author,  presented.Status, presented.College])

    # Create a table and set its style
    table = Table(presented_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Other rows background color
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Cell borders
    ]))

    styles = getSampleStyleSheet()

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,
        spaceAfter=30,
    )
    title = "Research Presented Details"
    elements.append(Paragraph(title, h2_style))
    elements.append(table)


    # Build the PDF document
    doc.build(elements)

    buffer.seek(0)

    # Return the PDF as a response
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="presented_report.pdf"'

    response['Content-Title'] = 'PDF Reports'
    return response

# published
def published_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    all_published_data = Research.objects.filter(Status = "Published")

    # Create table data
    published_data = [['Research ID', 'Research Title', 'Author', 'Status', 'College']]
    for published in all_published_data:
        published_data.append([published.Research_ID, published.Research_Title, published.Author,  published.Status, published.College])

    # Create a table and set its style
    table = Table(published_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Other rows background color
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Cell borders
    ]))

    styles = getSampleStyleSheet()

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,
        spaceAfter=30,
    )
    title = "Research Published Details"
    elements.append(Paragraph(title, h2_style))
    elements.append(table)


    # Build the PDF document
    doc.build(elements)

    buffer.seek(0)

    # Return the PDF as a response
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="published_report.pdf"'

    response['Content-Title'] = 'PDF Reports'
    return response

def all_research_pdf(request):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    all_research_data = Research.objects.all()

    # Create table data
    research_data = [['Research ID', 'Research Title', 'Author', 'Status', 'College']]
    for research in all_research_data:
        research_data.append([research.Research_ID, research.Research_Title, research.Author,  research.Status, research.College])

    # Create a table and set its style
    table = Table(research_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Header row background color
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Header row text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center-align all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row padding
        ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Other rows background color
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Cell borders
    ]))

    styles = getSampleStyleSheet()

    h2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Normal'],
        fontSize=14,
        alignment=1,
        spaceAfter=30,
    )
    title = "All Research Details"
    elements.append(Paragraph(title, h2_style))
    elements.append(table)


    # Build the PDF document
    doc.build(elements)

    buffer.seek(0)

    # Return the PDF as a response
    response = FileResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="published_report.pdf"'

    response['Content-Title'] = 'PDF Reports'
    return response