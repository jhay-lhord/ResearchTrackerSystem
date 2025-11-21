from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.user_login, name="login"),
    path('dashboard/', login_required(views.dashboard), name="dashboard"),
    path('all_research/', views.all_research, name="all_research"),
    path('delete_file/<int:research_id>/', views.delete_file, name="delete_file"),
    path('update_research/<int:research_id>/', views.update_research, name='update_research'),
    path('research-reports/', views.research_reports, name='research_reports'),
    path('presented', views.presented, name='presented'),
    path('ongoing', views.ongoing, name='ongoing'),
    path('conducted', views.conducted, name='conducted'),
    path('published', views.published, name='published'),
    path('user_logout', views.user_logout, name='logout'),
    path('user_account', views.user_account, name='user_account'),

    path('ongoing_reports', views.ongoing_pdf, name='ongoing_pdf'),
    path('conducted_reports', views.conducted_pdf, name='conducted_pdf'),
    path('presented_reports', views.presented_pdf, name='presented_pdf'),
    path('published_reports', views.published_pdf, name='published_pdf'),
    path('all_research_pdf', views.all_research_pdf, name='all_research_pdf'),
    

 #reset password
path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'), 
path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]