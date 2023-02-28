from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Avg, Min, Max, Count

from .serializers import JobSerializer, CandidateSerializer

from .models import Job, Candidate

from .filters import JobsFilter
from django.shortcuts import get_object_or_404
from django.utils import timezone


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
@permission_classes([IsAuthenticated])
# create new jobs
def newJob(request):
    request.data['user'] =  request.user
    data = request.data

    job = Job.objects.create(**data)

    serializer = JobSerializer(job, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateJob(request, pk):
    job = get_object_or_404(Job, id=pk)
    
    if job.user != request.user:
        return Response({'message': 'Job Can not be updated'}, status = status.HTTP_403_FORBIDDEN)

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
@permission_classes([IsAuthenticated])
def deleteJob(request, pk):
    
    job = get_object_or_404(Job, id=pk)
    # job by id
    
    if job.user != request.user:
        return Response({'message': 'Job can not be deleted'}, status = status.HTTP_403_FORBIDDEN)
    
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def applyJob(request, pk):
    
    user = request.user
    job = get_object_or_404(Job, id=pk)
    
    if user.userprofile.resume == '':
        return Response({ 'error': 'Resume must be submitted.'},
                         status = status.HTTP_400_BAD_REQUEST)
    
    if job.lastDate < timezone.now():
        return Response({ 'error': 'Deadline Passed.'},
                        status = status.HTTP_400_BAD_REQUEST)
    
    alreadyApplied = job.candidate_set.filter(user=user).exists()
    
    if alreadyApplied == True:
        return Response({ 'error': 'Already Applied.'},
                        status = status.HTTP_400_BAD_REQUEST) 
        
    jobApplied = Candidate.objects.create(
        job = job,
        resume = user.userprofile.resume,
        user = user
    )
    
    return Response({
        'applied' : True,
        'job_id': jobApplied.id
    },
        status = status.HTTP_200_OK
    )    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appliedJobs(request):
    args = {'user_id': request.user.id}
    jobs = Candidate.objects.filter(**args)
    serializer = CandidateSerializer(jobs, many = True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def hasApplied(request, pk):
    user = request.user
    job = get_object_or_404(Job, id=pk)
    applied = job.candidate_set.filter(user=user).exists()
    
    return Response(applied)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_created_jobs(request):
    args = {'user_id': request.user.id}
    jobs = Job.objects.filter(**args)
    serializer = JobSerializer(jobs, many = True)
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def appliedCandidates(request, pk):
    user = request.user
    job = get_object_or_404(Job, id=pk)
    
    if job.user != user:
        return Response({ 'error': 'Unauthorized to access this job.'},
                        status = status.HTTP_403_FORBIDDEN)
    
    candidates = job.candidate_set.all()
    
    serializer = CandidateSerializer(candidates, many = True)
    
    return Response(serializer.data)
