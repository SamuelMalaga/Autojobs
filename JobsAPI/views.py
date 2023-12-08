import subprocess
from django.http import JsonResponse
from .models import Job, Application, Certification, Education,Language,WorkExperience,UserProfile
from .serializers import JobSerializer, ApplicationSerializer, CertificationSerializer, EducationSerializer, LanguageSerializer, WorkExperienceSerializer, UserProfileSerializer,CustomTokenObtainPairSerializer, NewUserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import IntegrityError
# Auth Views
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, logout
import json



# ---------------------------------------------------------------
# <---                  Job Related Views                    --->
# ---------------------------------------------------------------
@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def job_list(request):
    # Configurar a paginação
    paginator = PageNumberPagination()
    paginator.page_size = 25  # Defina o número de itens por página

    jobs = Job.objects.all()

    # Paginar os resultados
    result_page = paginator.paginate_queryset(jobs, request)
    serializer = JobSerializer(result_page, many=True)

    # Retornar a resposta paginada
    return paginator.get_paginated_response(serializer.data)

    # jobs = Job.objects.all()
    # serializer = JobSerializer(jobs, many=True)
    # return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def execute_FULLpublicJscraper(request):
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
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def execute_LinkPublicScraper(request):
    # Substitua 'seu_script.js' pelo caminho para o seu script JavaScript.
    script_path = 'C:/Users/SamuelMendesMalaga/Documents/Autojobs/JParser/LinkPublicScraper.js'

    request_body = request.body.decode('utf-8')

    JSON_data = json.loads(request_body)

    job_link = JSON_data.get('job_link', None)

    print(job_link)

    try:
        # Execute o script JavaScript.
        result = subprocess.run(
            ['node', script_path, '--job_link', job_link],
            capture_output=True,
            text=True,
            encoding='utf-8',  # Set the encoding explicitly
            errors='replace',  # Replace or ignore characters that cannot be decoded
        )

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
# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
def application_list(request,user_id):
  if request.method =='GET':
    applications = Application.objects.filter(appl_user=user_id)
    serializer = ApplicationSerializer(applications, many=True)
    status_options = dict(Application.APPL_STATUSES)
    response_data = {
            'applications': serializer.data,
            'status_options': status_options,
        }
    return Response(response_data)
  if request.method == 'POST':
    serializer = ApplicationSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_application_detail(request, user_id, appl_id):
    try:
        application = Application.objects.get(appl_user=user_id, pk=appl_id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ApplicationSerializer(application)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_application_statuses(request, user_id, appl_id):
    try:
        application = Application.objects.get(appl_user=user_id, pk=appl_id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ApplicationSerializer(application)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_application(request, user_id, appl_id):
    try:
        application = Application.objects.get(appl_user=user_id, pk=appl_id)
    except Application.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    application.delete()
    return Response({'detail': 'application deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user_application(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        serializer = ApplicationSerializer(data=request.data, context={'request': request})

        # print('user_id',user.id)

        if serializer.is_valid():
            serializer.validated_data['appl_user'] = user
            instance = serializer.save()
            data = ApplicationSerializer(instance).data
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ---------------------------------------------------------------
# <---              Certification Related Views              --->
# ---------------------------------------------------------------
@api_view(['GET','POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_certification_detail(request, user_id, cert_id):
    try:
        certification = Certification.objects.get(cert_user=user_id, pk=cert_id)
    except Certification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CertificationSerializer(certification)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_certification(request, user_id, cert_id):
    try:
        certification = Certification.objects.get(cert_user=user_id, pk=cert_id)
    except Certification.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    certification.delete()
    return Response({'detail': 'certification deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_education_detail(request, user_id, edu_id):
    try:
        education = Education.objects.get(edu_user=user_id, pk=edu_id)
    except Education.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = EducationSerializer(education)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_education(request, user_id, edu_id):
    try:
        education = Education.objects.get(edu_user=user_id, pk=edu_id)
    except Education.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    education.delete()
    return Response({'detail': 'education deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_language_detail(request, user_id, lng_id):
    try:
        language = Language.objects.get(lng_user=user_id, pk=lng_id)
    except Language.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = LanguageSerializer(language)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_language(request, user_id, lng_id):
    try:
        language = Language.objects.get(lng_user=user_id, pk=lng_id)
    except Language.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    language.delete()
    return Response({'detail': 'Language deleted successfully'},status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])  # Adicione o TokenAuthentication aqui
@permission_classes([IsAuthenticated]) # Adicione IsAuthenticated aqui
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_work_experience(request, user_id, exp_id):
    try:
        work_experience = WorkExperience.objects.get(exp_user=user_id, pk=exp_id)
    except WorkExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = WorkExperienceSerializer(work_experience)
    return Response(serializer.data)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_work_experience(request, user_id, exp_id):
    try:
        work_experience = WorkExperience.objects.get(exp_user=user_id, pk=exp_id)
    except WorkExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    work_experience.delete()
    return Response({'detail': 'Work experience deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
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
            # Use o serializer personalizado para incluir informações adicionais no token
            serializer = CustomTokenObtainPairSerializer(data={"username": username, "password": password})
            serializer.is_valid(raise_exception=True)
            refresh = RefreshToken.for_user(user)

            # Inclua as informações adicionais no JSON de resposta
            response_data = {
                'access_token': str(refresh.access_token),
                'user_id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
            print(response_data)

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def logoutTeste(request):
   logout(request)
   return Response(status=status.HTTP_200_OK)
class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
    # Obtenha o token do cabeçalho da solicitação
        token = request.auth

        # Verifique se o token existe e é válido
        if token:
            # Decodifique o token para obter informações adicionais, se necessário
            user = Token.objects.get(key=token).user
            # Realize a lógica de logout
            token.delete()  # Exclua o token do banco de dados
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)
    # def post(self, request):
    #     token = request.auth
    #     print(token)
    #     request.auth.delete()
    #     return Response(status=status.HTTP_200_OK)

# ---------------------------------------------------------------
# <---                UserInfo Related Views                 --->
# ---------------------------------------------------------------
@api_view(['GET'])
def get_user_info(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user=user_id)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user_profile)
    return Response(serializer.data)

@api_view(['POST'])
def login_test(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"not found"},status=status.HTTP_404_NOT_FOUND)

    token,created = Token.objects.get_or_create(user=user)
    serializer = NewUserSerializer(instance=user)
    return Response({"token":token.key, "user":serializer.data})

@api_view(['GET'])
def signup_test(request):
    return Response({})

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def response_test(request):
    return Response({"passed for {}".format(request.user.email)})

@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_test(request):
    # Obtenha o token do cabeçalho da solicitação
    token = request.auth

    if token:
        # Exclua o token associado ao usuário
        token.delete()

        # Responda ao cliente indicando que o logout foi bem-sucedido
        return Response({"detail": "Logout bem-sucedido"}, status=status.HTTP_200_OK)
    else:
        # Se não houver token no cabeçalho, retorne uma resposta de erro
        return Response({"detail": "Token não fornecido"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user_profile(request, user_id):
    try:
        user_profile = UserProfile.objects.get(user=user_id)
    except WorkExperience.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserProfileSerializer(user_profile, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
