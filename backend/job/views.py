from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Avg, Min, Max, Count

from .serializers import JobSerializer
from .models import Job

from .filters import JobsFilter
from django.shortcuts import get_object_or_404


# Create your views here.

@api_view(['GET'])
def getAllJobs(request):


    filterset = JobsFilter(request.GET, queryset=Job.objects.all().order_by('id'))
    count = filterset.qs.count()
    # count the filter number

    # Pagignation
    resPerPage = 3
    paginator = PageNumberPagination()
    paginator.page_size = resPerPage
    # results per page
    
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = JobSerializer(queryset, many=True)
    return Response({'Jobs' : serializer.data,
                    'count': count,
                    'resPerPage': resPerPage
                    })


@api_view(['GET'])
# method 
def getJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    # get the id of the job using primary key
    # if object does not exist, through 404

    serializer = JobSerializer(job, many=False)

    return Response(serializer.data)


@api_view(['POST'])
# create new jobs
def newJob(request):
    data = request.data

    job = Job.objects.create(**data)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateJob(request, pk):
    job = get_object_or_404(Job, id=pk)

    job.title = request.data['title']
    job.description = request.data['description']
    job.email = request.data['email']
    job.address = request.data['address']
    job.jobType = request.data['jobType']
    job.education = request.data['education']
    job.industry = request.data['industry']
    job.experience = request.data['experience']
    job.salary = request.data['salary']
    job.positions = request.data['positions']
    job.company = request.data['company']

    job.save()

    serializer = JobSerializer(job, many=False)

    return Response(serializer.data)


@api_view(['DELETE'])
def deleteJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    # job by id

    job.delete()

    return Response({ 'message': 'Job is Deleted.' }, status=status.HTTP_200_OK)


@api_view(['GET'])
def getTopicStats(request, topic):

    args = { 'title__icontains': topic }
    jobs = Job.objects.filter(**args)
    # filters, and gets all jobs that are contains the topic word
    # Data filtering

    if len(jobs) == 0:
        return Response({ 'message': 'Not stats found for {topic}'.format(topic=topic) })
    # if lens == 0 - > no jobs with such topics found

    
    stats = jobs.aggregate(
        total_jobs = Count('title'),
        avg_positions = Avg('positions'),
        avg_salary = Avg('salary'),
        min_salary = Min('salary'),
        max_salary = Max('salary')
    )

    return Response(stats)