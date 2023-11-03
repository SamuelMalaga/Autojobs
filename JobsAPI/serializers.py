from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Job
    fields = ['job_id','job_title','company_name','job_link', 'job_description','double_check']
