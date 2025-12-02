from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def validate_file_extension(value):
    if not value.name.endswith(('.docx', '.pdf')):
        raise ValidationError(_('Only .docx and .pdf files are allowed.'))

class Research(models.Model):
    Research_ID = models.BigAutoField(primary_key=True)
    Research_Title = models.CharField(max_length=300)
    College = models.CharField(max_length=100)
    Year = models.CharField(max_length=20, default=datetime.now().year)
    Date_Started = models.DateField()
    Date_Ended = models.DateField()
    Status = models.CharField(max_length=200)
    Date_Presented = models.DateField(blank=True, null=True)
    Date_Ongoing = models.DateField(blank=True, null=True)
    Date_Conducted = models.DateField(blank=True, null=True)
    Date_Published = models.DateField(blank=True, null=True)
    ispnNo = models.CharField(max_length=200, blank=True, null=True)
    Publisher_Name = models.CharField(max_length=255, blank=True, null=True)
    Journal_Type = models.CharField(max_length=255, null=True, blank=True)
    Journal_Index = models.CharField(max_length=255, null=True, blank=True)
    Author = models.CharField(max_length=255)
    Document_File = models.FileField(upload_to = 'tmp/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.Research_Title


    class Meta:
        verbose_name = "Research"
        verbose_name_plural = "Researches"

    



