'''
Serializers are The Translator's of Django REST Framework. 
They convert complex data types, like Django models,
into native Python datatypes that can then be easily rendered into JSON, XML or other content types.
They also provide deserialization, allowing parsed data to be converted back into complex types, 
after first validating the incoming data.   
'''

from rest_framework import serializers
from django.apps import apps

# ============================================================
# PLEDGE SERIALIZER - Basic pledge data
# ============================================================
class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='supporter.id')
    supporter_username = serializers.ReadOnlyField(source='supporter.username')
    # ^^^ ADD THIS: Returns the username for display on frontend
    
    class Meta:
        model = apps.get_model('projects.Pledge')
        fields = '__all__'
    
    def create(self, validated_data):
        """
        When a pledge is created, append its content to the project's current_content
        with proper paragraph spacing (\n\n)
        """
        # Create the pledge first
        pledge = super().create(validated_data)
        
        # Get the project and append the new content with spacing
        project = pledge.project
        
        if project.current_content and project.current_content.strip():
            # Add double newline for paragraph spacing
            project.current_content = project.current_content.strip() + "\n\n" + pledge.add_content.strip()
        else:
            # If no current content yet, start with starting_content + new content
            if project.starting_content and project.starting_content.strip():
                project.current_content = project.starting_content.strip() + "\n\n" + pledge.add_content.strip()
            else:
                project.current_content = pledge.add_content.strip()
        
        project.save()
        return pledge


# ============================================================
# PROJECT SERIALIZER - Basic project data
# ============================================================
class ProjectSerializer(serializers.ModelSerializer):
    """
    Converts Project model ↔ JSON
    
    USED FOR: List views (showing many projects)
    
    fields = '__all__' means include everything:
    id, title, description, goal, image, genre, content_type,
    owner, starting_content, current_content, is_open, date_created 
    """
    owner_username = serializers.ReadOnlyField(source='owner.username')
    # ^^^ ADD THIS: Returns owner's username for display
    
    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'


# ============================================================
# PROJECT DETAIL SERIALIZER - Project with nested pledges
# ============================================================
class ProjectDetailSerializer(ProjectSerializer):
    """
    An EXTENDED version of ProjectSerializer that includes pledges.
    
    INHERITANCE: This inherits from ProjectSerializer
    So it has everything ProjectSerializer has, PLUS pledges.
    
    USED FOR: Detail view (viewing one specific project)
    """
    pledges = PledgeSerializer(many=True, read_only=True)
    owner_username = serializers.ReadOnlyField(source='owner.username')
    """
    NESTED SERIALIZER:
    This includes all pledges for this project inside the response!
    
    many=True = there can be multiple pledges
    read_only=True = you can't create pledges through this serializer
    
    EXAMPLE OUTPUT:
    {
        "id": 1,
        "title": "Haunted Lighthouse",
        "owner_username": "alice",
        "pledges": [
            {
                "id": 1, 
                "amount": 2, 
                "add_content": "The door creaked...",
                "supporter": 5,
                "supporter_username": "bob",
                "anonymous": false
            }
        ]
    }
    """

    def update(self, instance, validated_data):
        """
        CUSTOM UPDATE METHOD:
        Controls exactly which fields can be updated.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.starting_content = validated_data.get('starting_content', instance.starting_content)
        instance.current_content = validated_data.get('current_content', instance.current_content)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.save()
        return instance


# ============================================================
# PLEDGE DETAIL SERIALIZER
# ============================================================
class PledgeDetailSerializer(PledgeSerializer):
    """
    Extended pledge serializer with custom update logic.
    """
    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.add_content = validated_data.get('add_content', instance.add_content)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.project = validated_data.get('project', instance.project)
        instance.save()
        return instance