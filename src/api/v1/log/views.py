from .serializers import LogSerializer, LogUpdateStatusSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Log
from rest_framework.views import APIView
from rest_framework.response import Response
from api.v1.users.models import User
from rest_framework import status

class LogCreateView(generics.CreateAPIView):
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "student":
            raise PermissionDenied("Only students can create logs.")
        serializer.save(user=self.request.user)
        
class LogUpdateStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not hasattr(request.user, 'role') or request.user.role != 'supervisor':
            return Response(
                {'detail': 'Only supervisors can approve or reject logs.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            log = Log.objects.get(pk=pk)
        except Log.DoesNotExist:
            return Response({'detail': 'Log not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = LogUpdateStatusSerializer(log, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogListView(APIView):
    permission_classed = [IsAuthenticated]
    
    def get(self, request):
        user = request.user

        if user.role == 'student':
            logs = Log.objects.filter(user=user).order_by('-date')
            serializer = LogSerializer(logs, many=True)
            return Response(serializer.data)
        elif user.role == 'supervisor':
            user_id = request.query_params.get('user_id')
            if not user_id:
                return Response({"error": "Please provide a student user_id in query params."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                student = User.objects.get(id=user_id, role='student')
            except User.DoesNotExist:
                return Response({"error": "Student not found."}, status=status.HTTP_404_NOT_FOUND)

            logs = Log.objects.filter(user=student).order_by('-date')
            serializer = LogSerializer(logs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error": "You are not authorized to view logs."}, status=status.HTTP_403_FORBIDDEN)

