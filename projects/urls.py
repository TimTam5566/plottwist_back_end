from django.urls import path
from .views import ProjectList, ProjectDetail, PledgeList, PledgeDetail, PledgeListCreate


urlpatterns = [
    path('', ProjectList.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetail.as_view(), name='project-detail'),
    path('<int:project_id>/pledges/', PledgeListCreate.as_view(), name='pledge-list-create'),
    path('pledges/', PledgeList.as_view(), name='pledge-list'),
    path('pledges/<int:pk>/', PledgeDetail.as_view(), name='pledge-detail'),
]
