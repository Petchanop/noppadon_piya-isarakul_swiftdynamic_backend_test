from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from django.db.models import Count
from apis.serializers import (
    ClassroomDetailSerializer,
    ClassroomSerializer,
    SchoolDetailSerializer,
    SchoolSerializer,
)
from apis.models import School, Classroom
from apis.filters import ClassroomFilter, SchoolFilter


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = ( 
        School.objects
            .annotate(
            classrooms_count=Count("classrooms", distinct=True),
            teachers_count=Count("teacher", distinct=True),
            students_count=Count("student", distinct=True),
            ).prefetch_related(
                "classrooms",
                "classrooms__grade",
                "teacher",
                "student",
                )
            )
    # serializer_class = SchoolSerializer
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SchoolDetailSerializer
        return SchoolSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "School deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.prefetch_related(
        "teacher",
        "student",
    )
    # serializer_class = ClassroomSerializer
    filterset_class = ClassroomFilter
    
    def get_serializer_class(self) -> type[Serializer]:
        if self.action == "retrieve":
            return ClassroomDetailSerializer
        return ClassroomSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Classroom deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
