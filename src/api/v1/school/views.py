from .models import School, Department
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SchoolSerializer, DepartmentSerializer
from api.v1.users.models import AdminProfile


# Create your views here.
class SchoolListView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    
    def get_queryset(self):
        school_id = self.kwargs['school_id']
        return Department.objects.filter(school_id)

class CreateSchoolView(generics.CreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user


        try:
            admin_profile = user.adminprofile
        except AdminProfile.DoesNotExist:
            return Response({"error": "You are not authorized to create a school."},
                            status=status.HTTP_403_FORBIDDEN)


        if admin_profile.school:
            return Response({"error": "You already have a school assigned."},
                            status=status.HTTP_400_BAD_REQUEST)


        name = request.data.get('name')
        email = request.data.get('email')

        if School.objects.filter(name=name).exists() or School.objects.filter(email=email).exists():
            return Response({"error": "School with this name or email already exists."},
                            status=status.HTTP_400_BAD_REQUEST)

        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        school = serializer.save()

        
        admin_profile.school = school
        admin_profile.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CreateDepartmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

   
        try:
            admin_profile = AdminProfile.objects.get(user=user)
        except AdminProfile.DoesNotExist:
            return Response({'error': 'Only admins can create departments.'}, status=status.HTTP_403_FORBIDDEN)


        if not admin_profile.school:
            return Response({'error': 'Admin must be assigned to a school to create a department.'}, status=status.HTTP_400_BAD_REQUEST)


        data = request.data.copy()
        data['school'] = admin_profile.school.id


        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)