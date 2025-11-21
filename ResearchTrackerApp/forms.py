from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Research
from datetime import datetime

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ResearchForm(ModelForm):

    STATUS_CHOICE = (
        ('', 'Select Status'),
        ('Ongoing', 'Ongoing'),
        ('Conducted', 'Conducted'),
        ('Presented', 'Presented'),
        ('Published', 'Published')
    )

    COLLEGE_CHOICE = (
        ('COED', 'COED'),
        ('CAS', 'CAS'),
        ('CAFE', 'CAFE'),
        ('CHMT', 'CHMT'),
        ('COTE', 'COTE')
    )

    YEAR_CHOICES = [(str(year), str(year)) for year in range(datetime.now().year, 1900, -1)]

    JOURNAL_TYPE_CHOICES = (
        ("", "Select Type of Journal"),
        ("International", "International"),
        ("National", "National"),
        ("Local", "Local"),
    )

    Research_Title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder':  'Research Tracker System'}))
    College = forms.ChoiceField(choices=COLLEGE_CHOICE, widget=forms.Select(attrs={'class' : 'form-control'}))
    Status = forms.ChoiceField(choices=STATUS_CHOICE, widget=forms.Select(attrs={'class' : 'form-control'}))
    Year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select(attrs={'class' : 'form-control'}))
    Date_Started= forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))
    Date_Ended = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control'}))
    Date_Presented = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control hidden'}))
    Date_Ongoing = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control hidden'}))
    Date_Conducted = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control hidden'}))
    Date_Published = forms.DateField(required=False,  widget=forms.DateInput(attrs={'type': 'date', 'class' : 'form-control hidden'}))
    ispnNo = forms.CharField(required=False,  widget=forms.TextInput(attrs={'type': 'text', 'class' : 'form-control hidden'}))
    Publisher_Name = forms.CharField(required=False,  widget=forms.TextInput(attrs={'type': 'text', 'class' : 'form-control hidden'}))
    Journal_Type = forms.ChoiceField(required=False, choices=JOURNAL_TYPE_CHOICES,widget=forms.Select(attrs={'class' : 'form-control hidden'}))
    Journal_Index = forms.CharField(required=False, widget=forms.TextInput(attrs={ 'type': 'text', 'class' : 'form-control hidden '}))
    Author = forms.CharField(widget=forms.TextInput(attrs={'type': 'text', 'class' : 'form-control', 'placeholder' : 'Lastname F.'}))
    Document_File = forms.FileField(required=False, widget=forms.FileInput(attrs={'accept': '.pdf, .docx', 'class' : 'form-control'}))
    

    class Meta:
        model = Research
        fields = ('Research_ID', 'Research_Title', 'College', 'Year', 'Date_Started', 'Date_Ended', 'Status', 'Date_Presented', 'Date_Ongoing', 'Date_Conducted', 'Date_Published', 'ispnNo', 'Publisher_Name', 'Journal_Type', 'Journal_Index', 'Author', 'Document_File')

class ResearchFileUploadForm(forms.ModelForm):
    
    Document_File = forms.FileField(widget=forms.FileInput(attrs={'accept': '.pdf, .docx'}))
    
    class Meta:
        model = Research
        fields = ['Document_File']
class statusForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('', 'Select Status'),
        ('Presented', 'Presented'),
        ('Conducted', 'Conducted'),
        ('Ongoing', 'Ongoing'),
        ('Published', 'Published')
    )
    Status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Research
        fields = ['Status']

        
class ResearchStatusUpdateForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('Presented', 'Presented'),
        ('Conducted', 'Conducted'),
        ('On-going', 'On-going'),
        ('Published', 'Published')
    )

    Status = forms.ChoiceField(choices=STATUS_CHOICES)
    Date_Presented = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    Date_Conducted = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    Date_Ongoing = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    Date_Published = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Research
        fields = ['Status', 'Date_Presented', 'Date_Conducted', 'Date_Ongoing', 'Date_Published']
 