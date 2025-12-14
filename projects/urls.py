'''
urls.py - the address book for the projects app. It maps URL patterns to views.

'''
from django.urls import path
from .views import ProjectList, ProjectDetail, PledgeList, PledgeDetail, PledgeListCreate


urlpatterns = [
    # ============================================================
    # PROJECT URLS
    # ============================================================
    path('', ProjectList.as_view(), name='project-list'),
    # GET  /projects/     → List all projects
    # POST /projects/     → Create new project
    path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    # GET  /projects/1/   → Get project #1
    # PUT  /projects/1/   → Update project #1
    
    # ============================================================
    # PLEDGE URLS
    # ============================================================
    path('<int:project_id>/pledges/', PledgeListCreate.as_view(), name='pledge-list-create'),
    # POST /projects/1/pledges/  → Create pledge for project #1
    # This is the preferred way - project ID is in the URL!
    path('pledges/', PledgeList.as_view(), name='pledge-list'),
    # GET  /projects/pledges/    → List all pledges
    # POST /projects/pledges/    → Create pledge (need project in body)
    path('pledges/<int:pk>/', PledgeDetail.as_view(), name='pledge-detail'),
    # GET  /projects/pledges/1/  → Get pledge #1
    # PUT  /projects/pledges/1/  → Update pledge #1
]
