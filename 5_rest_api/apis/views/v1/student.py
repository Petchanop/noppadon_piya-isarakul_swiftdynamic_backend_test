from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from apis.serializers import StudentDetailSerializer, StudentSerializer
from apis.models import Student
from apis.filters import StudentFilter

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    filterset_class = StudentFilter
    
    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "list":
            return StudentSerializer
        return StudentDetailSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Student deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )