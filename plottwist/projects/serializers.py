from rest_framework import serializers
from django.apps import apps

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')  
    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'

    def validate(self, data):
        
        """
        Custom validation to ensure either poemstart or storystart is provided, not both
        """

        poemstart = data.get('poemstart')
        storystart = data.get('storystart')

        # Check that at least one content type is provided
        if not poemstart and not storystart:
            raise serializers.ValidationError(
                "Either poemstart or storystart must be provided"
            )

        # Check that both aren't provided
        if poemstart and storystart:
            raise serializers.ValidationError(
                "Cannot provide both poemstart and storystart"
            )

        # Validate required fields
        if not data.get('title'):
            raise serializers.ValidationError("Title is required")
        
        if not data.get('description'):
            raise serializers.ValidationError("Description is required")
        
        if not data.get('genre'):
            raise serializers.ValidationError("Genre is required")

        return data

    def create(self, validated_data):
        """
        Custom create method to handle null fields
        """
        # Ensure one content type is null based on what's provided
        if validated_data.get('poemstart'):
            validated_data['storystart'] = None
        else:
            validated_data['poemstart'] = None

        # Handle optional image field
        if 'image' not in validated_data:
            validated_data['image'] = None

        return super().create(validated_data)

class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = apps.get_model('projects.Pledge')
        fields = '__all__'

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    
    def update(self, instance, validated_data):
        # Update only editable fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.poemstart = validated_data.get('poemstart', instance.poemstart)
        instance.storystart = validated_data.get('storystart', instance.storystart)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        # date_created and owner are read-only and shouldn't be updated
        instance.save()
        return instance


class PledgeDetailSerializer(PledgeSerializer):
    def update(self, instance, validated_data):
        # Update only editable fields
        instance.amount = validated_data.get('amount', instance.amount)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.poemline = validated_data.get('poemline', instance.poemline)
        instance.storyverse = validated_data.get('storyverse', instance.storyverse)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.project = validated_data.get('project', instance.project)
        # date_created and supporter are read-only and shouldn't be updated
        instance.save()
        return instance