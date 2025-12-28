from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from apis.serializers import TeacherDetailSerializer, TeacherSerializer
from apis.models import Teacher 
from apis.filters import TeacherFilter

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    filterset_class = TeacherFilter
    
    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "list":
            return TeacherSerializer
        return TeacherDetailSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Teacher deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )