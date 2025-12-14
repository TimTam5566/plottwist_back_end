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
    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'

# ============================================================
# PLEDGE SERIALIZER - Basic pledge data
# ============================================================
class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='owner.id') # check for bugs may need to be supporter.id
    
    """
    ReadOnlyField = This field is OUTPUT only, never INPUT
    
    Converts Pledge model ↔ JSON
    
    This might cause issues - worth checking!
    """

    class Meta:
        model = apps.get_model('projects.Pledge')
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
    """
    NESTED SERIALIZER:
    This includes all pledges for this project inside the response!
    
    many=True = there can be multiple pledges
    read_only=True = you can't create pledges through this serializer
    
    EXAMPLE OUTPUT:
    {
        "id": 1,
        "title": "Haunted Lighthouse",
        "description": "A spooky tale...",
        "pledges": [
            {"id": 1, "amount": 2, "add_content": "The door creaked..."},
            {"id": 2, "amount": 1, "add_content": "A ghost appeared..."}
        ]
    }
    
    This works because of related_name='pledges' in the Pledge model!
    """

    def update(self, instance, validated_data):
        """
        CUSTOM UPDATE METHOD:
        Controls exactly which fields can be updated.
        
        instance = the existing project in the database
        validated_data = the new data from the request
        
        .get('field', default) means:
        "Get 'field' from new data, or keep the existing value if not provided"
        
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.starting_content = validated_data.get('starting_content', instance.starting_content)
        instance.current_content = validated_data.get('current_content', instance.current_content)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        # date_created and owner are read-only and shouldn't be updated they are set when project is created and are permaanent.
        instance.save()
        return instance

# ============================================================
# PLEDGE DETAIL SERIALIZER
# ============================================================
class PledgeDetailSerializer(PledgeSerializer):
    """
    Extended pledge serializer with custom update logic.
    
    NOTE: References instance.anonymous but that field doesn't exist in the model!
    This might be leftover from an earlier version or a planned feature.
    """
    def update(self, instance, validated_data):
        # Update only editable fields
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.add_content = validated_data.get('add_content', instance.add_content)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.project = validated_data.get('project', instance.project)
        # date_created and supporter are read-only and shouldn't be updated
        instance.save()
        return instance