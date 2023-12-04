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
    path('execute_full_scraper/', views.execute_FULLpublicJscraper, name='execute_scraper'),
    path('execute_link_scraper/', views.execute_LinkPublicScraper, name='execute_scraper'),
    # <-----Application related urls----->
    path('users/<int:user_id>/applications/', views.application_list),
    path('users/<int:user_id>/applications/<int:appl_id>/details', views.get_application_detail),
    path('users/<int:user_id>/applications/<int:appl_id>/update', views.update_application),
    path('users/<int:user_id>/applications/<int:appl_id>/delete', views.delete_application),
    path('users/<int:user_id>/applications/create/', views.create_user_application),
    # <-----Certification related urls----->
    path('users/<int:user_id>/certifications/', views.certification_list),
    path('users/<int:user_id>/certifications/<int:cert_id>/details', views.get_certification_detail),
    path('users/<int:user_id>/certifications/<int:cert_id>/update', views.update_certification),
    path('users/<int:user_id>/certifications/<int:cert_id>/delete', views.delete_certification),
    path('users/<int:user_id>/certifications/create/', views.create_user_certification),
    # <-----Education related urls----->
    path('users/<int:user_id>/educations/', views.education_list),
    path('users/<int:user_id>/educations/<int:edu_id>/details', views.get_education_detail),
    path('users/<int:user_id>/educations/<int:edu_id>/update', views.update_education),
    path('users/<int:user_id>/educations/<int:edu_id>/delete', views.delete_education),
    path('users/<int:user_id>/educations/create/', views.create_user_education),
    # <-----Language related urls----->
    path('users/<int:user_id>/languages/', views.language_list),
    path('users/<int:user_id>/languages/<int:lng_id>/details', views.get_language_detail),
    path('users/<int:user_id>/languages/<int:lng_id>/update', views.update_language),
    path('users/<int:user_id>/languages/<int:lng_id>/delete', views.delete_language),
    path('users/<int:user_id>/languages/create/', views.create_user_language),
    # <-----WorkExperience related urls----->
    path('users/<int:user_id>/work_experiences/', views.work_experience_list),
    path('users/<int:user_id>/work_experiences/<int:exp_id>/details', views.get_work_experience),
    path('users/<int:user_id>/work_experiences/<int:exp_id>/update', views.update_work_experience),
    path('users/<int:user_id>/work_experiences/<int:exp_id>/delete', views.delete_work_experience),
    path('users/<int:user_id>/work_experiences/create/', views.create_user_work_experience),
    # <-----User Profile related urls----->
    path('users/<int:user_id>/myProfile',views.get_user_info),
    path('users/<int:user_id>/myProfile/update',views.update_user_profile),
    # <-----Auth Related related urls----->
    path('deprecated_login/', LoginView.as_view(), name='login'),
    path('deprecated_logout/', LogoutView.as_view(), name='logout'),
    path('logoutTeste/',views.logoutTeste),
    # <-----Auth test urls----->
    path('login/', views.login_test),
    path('signup_test/', views.signup_test),
    path('response_test/',views.response_test),
    path('logout/',views.logout_test)
]
