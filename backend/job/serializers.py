from rest_framework import serializers
from .models import Job, Candidate

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields ='__all__'
        
class CandidateSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    
    class Meta:
        model = Candidate
        fields = ('user', 'appliedDate', 'job', 'resume')