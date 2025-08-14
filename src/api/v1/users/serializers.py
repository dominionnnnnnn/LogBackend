from rest_framework import serializers
from .models import  StudentProfile, SupervisorProfile, User , AdminProfile
from api.v1.school.models import School, Department

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            **validated_data,
            is_active=False 
        )
        user.set_password(password)
        user.save()
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'full_name']

# profile serializers
class StudentProfileSetupSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all()
    )
    
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )
    
    class Meta:
        model = StudentProfile
        fields = ['school', 'department', 'matric_number', 'internship_start', 'internship_end']

    def create(self, validated_data):
        return StudentProfile.objects.create(user=self.context['request'].user, **validated_data)

class SupervisorProfileSetupSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(
        queryset=School.objects.all()
    )
    
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all()
    )
    
    class Meta:
        model = SupervisorProfile
        fields = ['school', 'department', 'office', 'phone_number']

    def create(self, validated_data):
        return SupervisorProfile.objects.create(user=self.context['request'].user, **validated_data)
    
class AdminProfileSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = [ 'position', 'phone_number']

    def create(self, validated_data):
        return AdminProfile.objects.create(user=self.context['request'].user, **validated_data)

# photo serializers
class SupervisorPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorProfile
        fields = ['photo']
        
    def update(self, instance, validated_data):
        if 'photo' in validated_data:
            instance.photo = validated_data['photo']
            instance.save()
        return instance
    
class AdminPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['photo']
        
    def update(self, instance, validated_data):
        if 'photo' in validated_data:
            instance.photo = validated_data['photo']
            instance.save()
        return instance
    
class StudentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['photo']
        
    def update(self, instance, validated_data):
        if 'photo' in validated_data:
            instance.photo = validated_data['photo']
            instance.save()
        return instance