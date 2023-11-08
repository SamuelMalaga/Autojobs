from rest_framework import serializers
from .models import Job, Application, Certification, Education,Language,WorkExperience

class JobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Job
    fields = ['job_id','job_title','company_name','job_link', 'job_description','double_check']

class ApplicationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Application
    fields = ['appl_status','appl_closed_at','appl_started_at','appl_resume','appl_user_id','appl_job_id']

class CertificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Certification
    fields = ['cert_name','cert_institute','cert_emmited_at','cert_valid_until', 'cert_user' ]

class EducationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Education
    fields = ['edu_institute','edu_description','edu_start_time','edu_end_time','edu_user']

class LanguageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Language
    fields = ['lng_name','lng_country','lng_proficiency_level','lng_user']

class WorkExperienceSerializer(serializers.ModelSerializer):
  class Meta:
    model = WorkExperience
    fields = ['exp_company','exp_description','exp_start_time','exp_end_time','exp_user']

