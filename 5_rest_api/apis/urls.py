from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apis.views.v1.school import SchoolViewSet, ClassroomViewSet
from apis.views.v1.student import StudentViewSet
from apis.views.v1.teacher import TeacherViewSet


router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')

api_v1_urls = (router.urls, 'v1')

urlpatterns = [
    path('v1/', include(api_v1_urls))
]
