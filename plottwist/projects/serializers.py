from rest_framework import serializers
from django.apps import apps

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')  
    class Meta:
        model = apps.get_model('projects.Project')
        fields = '__all__'

class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = apps.get_model('projects.Pledge')
        fields = '__all__'

class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    
    def update(self, instance, validated_data):
        # Prevent updating the owner field
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.goal = validated_data.get('goal', instance.goal)
        instance.image = validated_data.get('image', instance.image)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.poemstart = validated_data.get('poemstart', instance.poemstart)
        instance.storystart = validated_data.get('storystart', instance.storystart)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
'''  
class pledgeDetailSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        # Prevent updating the supporter field
        instance.amount = validated_data.get('amount', instance.amount)
        
        instance.comment = validated_data.get('comment', instance.comment)
        instance.poemline = validated_data.get('poemline', instance.poemline)
        instance.storyverse = validated_data.get('storyverse', instance.storyverse)
        instance.anonymous = validated_data.get('anonymous', instance.anonymous)
        instance.supporter = validated_data.get('supporter', instance.supporter)
        instance.project = validated_data.get('project', instance.project)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.supporter = validated_data.get('supporter', instance.supporter)
        instance.save()
        return instance

        '''