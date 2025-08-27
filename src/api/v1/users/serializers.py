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
        fields = ['school', 'department', 'matric_number', 'organisation_name', 'internship_location', 'internship_start', 'internship_end']

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

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'photo', 'school', 'department', 'matric_number',
            'organisation_name', 'internship_location',
            'internship_start', 'internship_end'
        ]

class SupervisorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorProfile
        fields = ['photo', 'school', 'department', 'office', 'phone_number']

class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = ['photo', 'school', 'position', 'phone_number']
        
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        if instance.role == "student" and hasattr(instance, 'student_profile'):
            data['profile'] = StudentProfileSerializer(instance.student_profile).data
            data['supervisor_name'] = (
                instance.student_profile.supervisor.full_name
                if instance.student_profile.supervisor else None
            )
            data['student_id'] = (
                instance.student_profile.id
                if instance.student_profile else None
            )
            data['school_name'] = (
                instance.student_profile.school.name
                if instance.student_profile.school else None
            )
            data['department'] = (
                instance.student_profile.department.name
                if instance.student_profile.department else None
            )
        elif instance.role == "supervisor" and hasattr(instance, 'supervisor_profile'):
            data['profile'] = SupervisorProfileSerializer(instance.supervisor_profile).data
            data['school_name'] = (
                instance.supervisor_profile.school.name
                if instance.supervisor_profile.school else None
            )
            data['department'] = (
                instance.supervisor_profile.department.name
                if instance.supervisor_profile.department else None
            )
        elif instance.role == "admin" and hasattr(instance, 'admin_profile'):
            data['profile'] = AdminProfileSerializer(instance.admin_profile).data
            
            data['school_name'] = (
                instance.admin_profile.school.name
                if instance.admin_profile.school else None
            )

        return data


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