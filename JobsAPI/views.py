import subprocess
from django.http import JsonResponse
from .models import Job, Application, Certification, Education,Language,WorkExperience
from .serializers import JobSerializer, ApplicationSerializer, CertificationSerializer, EducationSerializer, LanguageSerializer, WorkExperienceSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Auth Views
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
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
def application_list(request):
  if request.method =='GET':
    applications = Application.objects.all()
    serializer = ApplicationSerializer(applications, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def application_detail(request,id):
  try:
    application = Application.objects.get(pk=id)
  except Application.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method =='GET':
    serializer = ApplicationSerializer(application)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = ApplicationSerializer(application, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    application.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------
# <---              Certification Related Views              --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def certification_list(request):
  if request.method =='GET':
    certifications = Certification.objects.all()
    serializer = CertificationSerializer(certifications, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = CertificationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def certification_detail(request,id):
  try:
    certification = Certification.objects.get(pk=id)
  except Certification.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method =='GET':
    serializer = CertificationSerializer(certification)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = CertificationSerializer(certification, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    certification.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------
# <---               Education Related Views                 --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def education_list(request):
  if request.method =='GET':
    educations = Education.objects.all()
    serializer = EducationSerializer(educations, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = EducationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def education_detail(request,id):
  try:
    education = Education.objects.get(pk=id)
  except Education.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method =='GET':
    serializer = EducationSerializer(education)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = EducationSerializer(education, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    education.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------
# <---                Language Related Views                 --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def language_list(request):
  if request.method =='GET':
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = LanguageSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def language_detail(request,id):
  try:
    language = Language.objects.get(pk=id)
  except Language.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method =='GET':
    serializer = LanguageSerializer(language)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = LanguageSerializer(language, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    language.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------
# <---                WorkExperience Related Views           --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
def work_experience_list(request):
  if request.method =='GET':
    work_experiences = WorkExperience.objects.all()
    serializer = WorkExperienceSerializer(work_experiences, many=True)
    return Response(serializer.data)
  if request.method == 'POST':
    serializer = WorkExperienceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def work_experience_detail(request,id):
  try:
    work_experience = WorkExperience.objects.get(pk=id)
  except Language.DoesNotExist:
    return Response(status=status.HTTP_404_NOT_FOUND)
  if request.method =='GET':
    serializer = WorkExperienceSerializer(work_experience)
    return Response(serializer.data)
  elif request.method == 'PUT':
    serializer = WorkExperienceSerializer(work_experience, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'DELETE':
    work_experience.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------
# <---                  Auth Related Views                   --->
# ---------------------------------------------------------------
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
