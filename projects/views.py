'''
views.py is the main file where we define the API endpoints for our projects and pledges. 
It uses Django REST Framework's APIView to create class-based views for listing, creating, 
retrieving, and updating projects and pledges. The file also includes custom permissions to 
ensure that only authorized users can modify certain resources.
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .permissions import IsOwnerOrReadOnly, IsSupporterOrReadOnly
from django.http import Http404
from .models import Project, Pledge
from .serializers import ProjectSerializer, PledgeSerializer, ProjectDetailSerializer

# ============================================================
# API ROOT - The "homepage" of your API
# ============================================================

@api_view(['GET'])
def api_root(request, format=None):

    """
    
    A helpful landing page that shows all available API endpoints.
    
    WHEN YOU VISIT: /api/ or your base API URL
    
    RETURNS:
    {
        'projects': 'http://plottwist.com/projects/',
        'pledges': 'http://plottwist.com/projects/pledges/',
        'auth': 'http://plottwist.com/api-token-auth/'
    }
    
    """
    return Response({
        'projects': reverse('project-list', request=request, format=format),
        'pledges': reverse('pledge-list', request=request, format=format),
        'auth': reverse('api_token_auth', request=request, format=format),
    })

# ============================================================
# PROJECT LIST - Handle /projects/
# ============================================================

class ProjectList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    """
    PERMISSION EXPLAINED:
    IsAuthenticatedOrReadOnly means:
    - Anyone can READ (GET) - even without logging in
    - Only logged-in users can CREATE (POST)
    
    This makes sense! People accessing the site can browse projects,
    but only registered users can create new ones.
    """
    def get(self, request):
        """
        GET /projects/
        
        Returns ALL projects
        
        USED BY: Homepage, project listing page
        
        RETURNS: List of all projects as JSON
        [
            {"id": 1, "title": "Haunted Lighthouse", ...},
            {"id": 2, "title": "Space Adventure", ...}
        ]
        """
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True) # many=True for lists
        return Response(serializer.data)

    def post(self, request):
        """
        POST /projects/
        
        Creates a NEW project
        
        USED BY: "Create Project" form in React
        
        IMPORTANT: serializer.save(owner=request.user)
        This automatically sets the owner to whoever is logged in!
        The frontend doesn't need to send owner - it's set from the auth token.
        """
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user) # Auto-assign owner!
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )
    
# ============================================================
# PROJECT DETAIL - Handle /projects/1/
# ============================================================
class ProjectDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    """
    TWO PERMISSIONS STACKED:
    1. IsAuthenticatedOrReadOnly - must be logged in to edit
    2. IsOwnerOrReadOnly - must be the OWNER to edit
    
    So to edit a project, you must be:
    - Logged in AND
    - The owner of that specific project
    """

    def get_object(self, pk):
        """
        Find a project by ID (pk = primary key)
        
        Also runs permission checks!
        self.check_object_permissions() verifies the user can access this specific project.
        """
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        GET /projects/1/
        
        Returns ONE specific project with full details
        
        NOTE: Uses ProjectDetailSerializer (not ProjectSerializer)
        This includes the pledges nested inside!
        """
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        PUT /projects/1/
        
        Updates a project
        
        USED BY: "Edit Project" page in React
        
        IMPORTANT: partial=True allows updating just SOME fields
        Without it, you'd have to send ALL fields every time.
        """
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            instance=project, # The existing project to update
            data=request.data, # The new data from the request
            partial=True # Allow partial updates
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )
    
# ============================================================
# PLEDGE LIST - Handle /projects/pledges/
# ============================================================    
class PledgeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        '''
        GET /projects/pledges/
            
        WHAT IT DOES: Returns ALL pledges across all projects
        USED BY admin dashboards or analytics.
        '''
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST /projects/pledges/
        
        WHAT IT DOES: Creates a new pledge (contribution)
        
        Like projects, the supporter is auto-assigned from the logged-in user.
        Used by the pledge form on project detail pages.
        """
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user) # Auto-assign supporter!
            return Response(
                serializer.data, 
                status=status.HTTP_201_CREATED
                )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
            )
# ============================================================
# PLEDGE DETAIL - Handle /projects/pledges/1/
# ============================================================   
class PledgeDetail(APIView):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsSupporterOrReadOnly # Only the person who made the pledge can edit it
    ]

    def get_object(self, pk):
        try:
            pledge = Pledge.objects.get(pk=pk)
            self.check_object_permissions(self.request, pledge)
            return pledge
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """GET /projects/pledges/1/ - Get one specific pledge"""
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """PUT /projects/pledges/1/ - Update a pledge"""
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(
            instance=pledge,
            data=request.data,
            partial=True
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )
# ============================================================
# PLEDGE LIST CREATE - Handle /projects/1/pledges/
# ============================================================
class PledgeListCreate(APIView):
    """
    
    A special endpoint for creating pledges FOR A SPECIFIC PROJECT.
    
    Instead of: POST /projects/pledges/ with project_id in the body
    You can do: POST /projects/1/pledges/ (project ID is in the URL!)
    
    This is cleaner and more RESTful.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def post(self, request, project_id):
        # Check if user is logged in
        if not request.user.is_authenticated:
            return Response(
                {"error": "The gates remain sealed — no credentials, no quest. Try again or forge a new identity."},
                # ^^^ Fun themed error message! Very on-brand for a storytelling app 📚
                status=status.HTTP_401_UNAUTHORIZED
            )
        # Find the project by ID
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return Response({"error": "Project not found."}, status=status.HTTP_404_NOT_FOUND)
        # Add project_id to the data before serialization
        data = request.data.copy()
        data['project'] = project_id
        serializer = PledgeSerializer(data=data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

