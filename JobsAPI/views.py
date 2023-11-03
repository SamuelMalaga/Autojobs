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
    return JsonResponse({'jobs':serializer.data})
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
  elif request.method == 'POST':
    pass
  elif request.method == 'DELETE':
    pass
