import subprocess
from django.http import JsonResponse
from .models import Job, Application, Certification, Education,Language,WorkExperience
from .serializers import JobSerializer, ApplicationSerializer, CertificationSerializer, EducationSerializer, LanguageSerializer, WorkExperienceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
# Auth Views
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



# ---------------------------------------------------------------
# <---                  Job Related Views                    --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def job_list(request):
  if request.method =='GET':
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def job_detail(request,id):
  try:
    job = Job.objects.get(pk=id)
  except Job.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method =='GET':
    serializer = JobSerializer(job)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = JobSerializer(job, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    job.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------
# <---                Scraper Related Views                  --->
# ---------------------------------------------------------------
@api_view(['POST'])
def execute_scraper(request):
    # Substitua 'seu_script.js' pelo caminho para o seu script JavaScript.
    script_path = 'C:/Users/SamuelMendesMalaga/Documents/Autojobs/JParser/FULLpublicJscraper.js'
    job_name = request.GET.get('job_name')
    job_location = request.GET.get('job_location')
    job_type = request.GET.get('job_type')

    job_name_str = str(job_name) if job_name is not None else ''
    job_location_str = str(job_location) if job_location is not None else ''
    job_type_str = str(job_type) if job_type is not None else ''
    print('job_name:',job_name,'job_location:',job_location,'job_type:',job_type)

    try:
        # Execute o script JavaScript.
        result = subprocess.run(['node', script_path, '--job-name', job_name_str,'--job-location', job_location_str,'--job-type', job_type_str], capture_output=True, text=True)

        # Verifique a saída do processo.
        if result.returncode == 0:
            return JsonResponse({'message': 'Script executado com sucesso', 'output': result.stdout})
        else:
            return JsonResponse({'message': 'Erro na execução do script', 'error_output': result.stderr}, status=500)
    except Exception as e:
        return JsonResponse({'message': 'Erro na execução do script', 'error_message': str(e)}, status=500)

# ---------------------------------------------------------------
# <---              Application Related Views                --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def application_list(request,user_id):
  if request.method =='GET':
    applications = Application.objects.filter(appl_user=user_id)
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_application_detail(request, user_id, appl_id):
    try:
        application = Application.objects.get(appl_user=user_id, pk=appl_id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ApplicationSerializer(application)
    return Response(serializer.data)

@api_view(['PUT'])
def update_application(request, user_id, appl_id):
    try:
        application = Application.objects.get(appl_user=user_id, pk=appl_id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ApplicationSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_application(request, user_id, appl_id):
    try:
        application = Application.objects.get(appl_user=user_id, pk=appl_id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    application.delete()
    return Response({'detail': 'application deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_user_application(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Certifique-se de passar o contexto para o serializer
        serializer = ApplicationSerializer(data=request.data, context={'request': request})

        # print('user_id',user.id)

        if serializer.is_valid():
            # Adicione o usuário à instância do serializer
            serializer.validated_data['appl_user'] = user
            print('serializer Data',serializer.validated_data)
            instance = serializer.save()
            data = ApplicationSerializer(instance).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------
# <---              Certification Related Views              --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def certification_list(request,user_id):
  if request.method =='GET':
    certifications = Certification.objects.filter(cert_user=user_id)
    serializer = CertificationSerializer(certifications, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = CertificationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_certification_detail(request, user_id, cert_id):
    try:
        certification = Certification.objects.get(cert_user=user_id, pk=cert_id)
    except Certification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CertificationSerializer(certification)
    return Response(serializer.data)

@api_view(['PUT'])
def update_certification(request, user_id, cert_id):
    try:
        certification = Certification.objects.get(cert_user=user_id, pk=cert_id)
    except Certification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CertificationSerializer(certification, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_certification(request, user_id, cert_id):
    try:
        certification = Certification.objects.get(cert_user=user_id, pk=cert_id)
    except Certification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    certification.delete()
    return Response({'detail': 'certification deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_user_certification(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Certifique-se de passar o contexto para o serializer
        serializer = CertificationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Adicione o usuário à instância do serializer
            serializer.validated_data['cert_user'] = user
            instance = serializer.save()

            data = CertificationSerializer(instance).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------
# <---               Education Related Views                 --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def education_list(request,user_id):
  if request.method =='GET':
    educations = Education.objects.filter(edu_user=user_id)
    serializer = EducationSerializer(educations, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = EducationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_education_detail(request, user_id, edu_id):
    try:
        education = Education.objects.get(edu_user=user_id, pk=edu_id)
    except Education.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EducationSerializer(education)
    return Response(serializer.data)

@api_view(['PUT'])
def update_education(request, user_id, edu_id):
    try:
        education = Education.objects.get(edu_user=user_id, pk=edu_id)
    except Education.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EducationSerializer(education, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_education(request, user_id, edu_id):
    try:
        education = Education.objects.get(edu_user=user_id, pk=edu_id)
    except Education.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    education.delete()
    return Response({'detail': 'education deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_user_education(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Certifique-se de passar o contexto para o serializer
        serializer = EducationSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Adicione o usuário à instância do serializer
            serializer.validated_data['edu_user'] = user
            instance = serializer.save()

            data = EducationSerializer(instance).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------
# <---                Language Related Views                 --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def language_list(request,user_id):
  if request.method =='GET':
    languages = Language.objects.filter(lng_user=user_id)
    serializer = LanguageSerializer(languages, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = LanguageSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_language_detail(request, user_id, lng_id):
    try:
        language = Language.objects.get(lng_user=user_id, pk=lng_id)
    except Language.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LanguageSerializer(language)
    return Response(serializer.data)

@api_view(['PUT'])
def update_language(request, user_id, lng_id):
    try:
        language = Language.objects.get(lng_user=user_id, pk=lng_id)
    except Language.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LanguageSerializer(language, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_language(request, user_id, lng_id):
    try:
        language = Language.objects.get(lng_user=user_id, pk=lng_id)
    except Language.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    language.delete()
    return Response({'detail': 'Language deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_user_language(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Certifique-se de passar o contexto para o serializer
        serializer = LanguageSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Adicione o usuário à instância do serializer
            serializer.validated_data['lng_user'] = user
            instance = serializer.save()

            data = LanguageSerializer(instance).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------
# <---                WorkExperience Related Views           --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def work_experience_list(request,user_id):
  if request.method =='GET':
    work_experiences = WorkExperience.objects.filter(exp_user=user_id)
    serializer = WorkExperienceSerializer(work_experiences, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = WorkExperienceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_work_experience(request, user_id, exp_id):
    try:
        work_experience = WorkExperience.objects.get(exp_user=user_id, pk=exp_id)
    except WorkExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WorkExperienceSerializer(work_experience)
    return Response(serializer.data)

@api_view(['PUT'])
def update_work_experience(request, user_id, exp_id):
    try:
        work_experience = WorkExperience.objects.get(exp_user=user_id, pk=exp_id)
    except WorkExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WorkExperienceSerializer(work_experience, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_work_experience(request, user_id, exp_id):
    try:
        work_experience = WorkExperience.objects.get(exp_user=user_id, pk=exp_id)
    except WorkExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    work_experience.delete()
    return Response({'detail': 'Work experience deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def create_user_work_experience(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        # Certifique-se de passar o contexto para o serializer
        serializer = WorkExperienceSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # Adicione o usuário à instância do serializer
            serializer.validated_data['exp_user'] = user
            instance = serializer.save()

            data = WorkExperienceSerializer(instance).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------
# <---                  Auth Related Views                   --->
# ---------------------------------------------------------------
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
