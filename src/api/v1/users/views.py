from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework import status, permissions
from .models import User, StudentProfile, SupervisorProfile, AdminProfile
from .serializers import UserRegistrationSerializer, StudentProfileSetupSerializer, AdminProfileSetupSerializer, SupervisorProfileSetupSerializer, SupervisorPhotoSerializer, StudentPhotoSerializer, AdminPhotoSerializer ,UserDetailSerializer
from rest_framework.permissions import IsAuthenticated 
from rest_framework.parsers import MultiPartParser, FormParser
from .tasks import send_verification_email
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            code = user.generate_verification_code()
            email = user.email
            send_verification_email(email, code)
            return Response({"message": "Email sent"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResendVerificationCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)

        code = user.generate_verification_code()

        send_verification_email(user.email, code)

        return Response({"message": "Verification code resent"}, status=status.HTTP_200_OK)
    
class VerifyCodeView(APIView):
     def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        if user.verification_code != code:
            return Response({"error": "Invalid verification code."}, status=400)

        if timezone.now() > user.code_expiry:
            return Response({"error": "Verification code expired."}, status=400)

        user.is_active = True
        user.verification_code = None
        user.code_expiry = None
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Email verified successfully.",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=200)

class UserProfileSetupView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if request.user.role == 'student':
            serializer = StudentProfileSetupSerializer(data=request.data, context={'request': request})
        elif request.user.role == 'supervisor':
            serializer = SupervisorProfileSetupSerializer(data=request.data, context={'request': request})
        elif request.user.role == 'admin':
            serializer = AdminProfileSetupSerializer(data=request.data, context={'request': request})
        else:
            return Response({"error": "Invalid user role"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile setup successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfilePhotoUpdateView(APIView):

    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        user = request.user

        if user.role == 'student':
            profile = getattr(user, 'student_profile', None)
            serializer = StudentPhotoSerializer(profile, data=request.data, partial=True)
        elif user.role == 'supervisor':
            profile = getattr(user, 'supervisor_profile', None)
            serializer = SupervisorPhotoSerializer(profile, data=request.data, partial=True)
        elif user.role == 'admin':
            profile = getattr(user, 'admin_profile', None)
            serializer = AdminPhotoSerializer(profile, data=request.data, partial=True)
        else:
            return Response({"error": "Invalid user role"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not profile:
            return Response({"error": "Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile photo updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListStudentView(APIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        base_qs = User.objects.filter(role="student")  # Only students
        
        if user.role == 'student':
            raise PermissionDenied("Students cannot access this view.")
        
        elif user.role == 'admin':
            qs = base_qs.filter(
                student_profile__school_id=user.admin_profile.school.id
            )
        
        elif user.role == "supervisor":
            sp = user.supervisor_profile
            qs = base_qs.filter(
                student_profile__department_id=sp.department.id
            )
        
        else:
            qs = User.objects.none()
        
        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

class ListSupervisorView(APIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Only admins can access this
        if user.role != 'admin':
            raise PermissionDenied("Only admins can access this view.")

        # Filter supervisors by the same school as the admin
        qs = User.objects.filter(
            role="supervisor",
            supervisor_profile__school_id=user.admin_profile.school.id
        )

        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)
        
class IsSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'supervisor'

class AssignSupervisorView(APIView):
    permission_classes = [IsSupervisor]

    def post(self, request, student_id):
        # Fetch student with related fields in one query
        student = get_object_or_404(
            StudentProfile.objects.select_related('school', 'department', 'supervisor'),
            pk=student_id
        )

        if student.supervisor_id:
            return Response(
                {'detail': 'This student already has a supervisor.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        supervisor_profile = request.user.supervisor_profile 

        
        if student.school_id != supervisor_profile.school_id:
            return Response(
                {'detail': 'You cannot assign yourself to a student from another school.'},
                status=status.HTTP_403_FORBIDDEN
            )

        
        if hasattr(supervisor_profile, 'department_id') and student.department_id != supervisor_profile.department_id:
            return Response(
                {'detail': 'You cannot assign yourself to a student from another department.'},
                status=status.HTTP_403_FORBIDDEN
            )

        
        student.supervisor = request.user
        student.save(update_fields=['supervisor'])

        return Response(
            {'detail': 'Supervisor assigned successfully.'},
            status=status.HTTP_200_OK
        )
        
class ListAssignedStudentsView(APIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role != "supervisor":
            raise PermissionDenied("Only supervisors can access this view.")

        qs = User.objects.filter(
            role="student",
            student_profile__supervisor=user
        )

        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)
