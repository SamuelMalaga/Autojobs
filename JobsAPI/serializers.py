from rest_framework import serializers
from .models import Job, Application, Certification, Education,Language,WorkExperience, User, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class JobSerializer(serializers.ModelSerializer):
  class Meta:
    model = Job
    fields = '__all__'
    #['job_id','job_title','company_name','job_link', 'job_description','double_check']

class ApplicationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Application
    fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Certification
    fields = '__all__'
    #['cert_name','cert_institute','cert_emmited_at','cert_valid_until', 'cert_user' ]

class EducationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Education
    fields = '__all__'
    #['edu_institute','edu_description','edu_start_time','edu_end_time','edu_user']

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
  class Meta:
    model = WorkExperience
    fields = '__all__'
    #['exp_company','exp_description','exp_start_time','exp_end_time','exp_user','id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = User.objects.get(username=attrs['username'])

        # Inclua as informações adicionais no token
        data['user_id'] = user.id
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email

        return data

class NewUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id','first_name','last_name','email']
