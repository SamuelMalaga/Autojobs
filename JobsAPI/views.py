import subprocess
from django.http import JsonResponse
from .models import Job
from .serializers import JobSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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
