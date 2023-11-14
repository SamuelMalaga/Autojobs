"""
URL configuration for JobsAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from JobsAPI import views
from .views import LoginView,LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    # <-----Job related urls----->
    path('jobs/', views.job_list),
    path('jobs/<int:id>', views.job_detail),
    # <-----Scraper related urls----->
    path('execute-scraper/', views.execute_scraper, name='execute_scraper'),
    # <-----Application related urls----->
    path('applications/', views.application_list),
    path('applications/<int:id>', views.application_detail),
    # <-----Certification related urls----->
    path('certifications/', views.certification_list),
    path('certifications/<int:id>', views.certification_detail),
    path('users/<int:user_id>/certifications/create/', views.create_user_certification),
    # <-----Education related urls----->
    path('educations/', views.education_list),
    path('educations/<int:id>', views.education_detail),
    path('users/<int:user_id>/educations/create/', views.create_user_education),
    # <-----Language related urls----->
    path('languages/', views.language_list),
    path('languages/<int:id>', views.language_detail),
    path('users/<int:user_id>/languages/create/', views.create_user_language),
    # <-----WorkExperience related urls----->
    path('work_experiences/', views.work_experience_list),
    path('work_experiences/<int:id>', views.work_experience_detail),
    path('users/<int:user_id>/work_experiences/create/', views.create_user_work_experience),
    # <-----Auth Related related urls----->
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
