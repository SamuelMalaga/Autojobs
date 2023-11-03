from django.http import JsonResponse
from .models import Job
from .serializers import JobSerializer

def job_list(request):
  jobs = Job.objects.all()
  serializer = JobSerializer(jobs, many=True)
  return JsonResponse({'jobs':serializer.data})
