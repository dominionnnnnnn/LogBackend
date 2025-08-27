from rest_framework import serializers
from .models import School, Department

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        
class SchoolLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['logo']
        
    def update(self, instance, validated_data):
        if 'logo' in validated_data:
            instance.logo = validated_data['logo']
            instance.save()
        return instance