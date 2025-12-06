from django.urls import path
from . import views

urlpatterns = [
    # Home pages
    path('', views.home, name='home'),
    
    # About and Services
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/air-transport/', views.air_transport, name='air_transport'),
    path('services/sea-transport/', views.sea_transport, name='sea_transport'),
    path('services/logistics/', views.logistics, name='logistics'),
    
    # News
    path('news/', views.company_news, name='company_news'),
    path('news/company/', views.company_news, name='company_news'),
    path('news/industry/', views.industry_news, name='industry_news'),
    path('news/recruitment/', views.recruitment, name='recruitment'),
    path('news/<slug:slug>/', views.post_detail, name='post_detail'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
    
    # Projects
    path('projects/', views.projects, name='projects'),

    # Feedback
    path('feedback/', views.feedback, name='feedback'),
    
    # Branch network
    path('contact/branches/', views.branch_network, name='branch_network'),
    
    # Search
    path('search/', views.search, name='search'),
]