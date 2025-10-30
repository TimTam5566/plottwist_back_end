from rest_framework import serializers
from django.apps import apps

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    image = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'

    def validate(self, data):
        if not data.get('starting_content'):
            raise serializers.ValidationError({"starting_content": "This field is required."})
        if not data.get('title'):
            raise serializers.ValidationError("Title is required")
        if not data.get('description'):
            raise serializers.ValidationError("Description is required")
        if not data.get('genre'):
            raise serializers.ValidationError("Genre is required")
        return data

    def create(self, validated_data):
        # Ensure one content type is null based on what's provided
        if validated_data.get('poemstart'):
            validated_data['storystart'] = None
        else:
            validated_data['poemstart'] = None

        # Handle optional image field
        if 'image' not in validated_data:
            validated_data['image'] = ""

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