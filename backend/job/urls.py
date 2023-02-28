from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.getAllJobs, name='jobs'),
    path('jobs/new/', views.newJob, name='new_job'),
    path('jobs/<str:pk>/', views.getJob, name='job'),
    # job enpoint by id
    # using the GET function written in views.py
    path('jobs/<str:pk>/update/', views.updateJob, name='update_job'),
    path('jobs/<str:pk>/delete/', views.deleteJob, name='delete_job'),
    path('jobs/<str:pk>/apply/', views.applyJob, name='apply_job'),
    path('jobs/<str:pk>/applied/', views.hasApplied, name='has_applied'),
    path('jobs/<str:pk>/candidates/', views.appliedCandidates, name='applied_candidates'),
    path('me/jobs/applied/', views.appliedJobs, name='applied_jobs'),
    path('me/jobs/created', views.user_created_jobs, name='user_created_jobs'),
    path('stats/<str:topic>/', views.getTopicStats, name='get_topic_stats')
]