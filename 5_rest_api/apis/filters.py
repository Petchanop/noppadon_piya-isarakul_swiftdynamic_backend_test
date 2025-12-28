from django_filters import FilterSet, filters
from apis.models import Gender, School, Classroom, Student, Teacher


# code here
class SchoolFilter(FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = School
        fields = "__all__"


class ClassroomFilter(FilterSet):
    school = filters.CharFilter(field_name="school__name", lookup_expr="icontains")

    class Meta:
        model = Classroom
        fields = "__all__"

class GenderFilterMixin:
    def filter_gender(self, queryset, name, value):
        value = value.strip().lower()

        gender_map = {
            # codes
            "m": Gender.MALE,
            "f": Gender.FEMALE,
            "u": Gender.UNSPECIFIC,

            # display names
            "male": Gender.MALE,
            "female": Gender.FEMALE,
            "unspecified": Gender.UNSPECIFIC,
        }

        gender_code = gender_map.get(value)

        if gender_code is None:
            return queryset.none()

        return queryset.filter(gender=gender_code)

class TeacherFilter(GenderFilterMixin,FilterSet):
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains"
    )
    gender = filters.CharFilter(method="filter_gender")

    # school filters
    school_id = filters.NumberFilter(field_name="school_id")
    school = filters.CharFilter(
        field_name="school__name",
        lookup_expr="icontains"
    )

    classroom = filters.CharFilter(method="filter_classroom")

    # atomic filters (recommended to keep)
    grade = filters.CharFilter(
        field_name="classrooms__grade__name",
        lookup_expr="iexact"
    )
    room = filters.NumberFilter(
        field_name="classrooms__room"
    )

    def filter_classroom(self, queryset, name, value):
        try:
            grade, room = value.replace(" ", "").split("/")
            room = int(room)
        except ValueError:
            return queryset.none()

        return queryset.filter(
            classrooms__grade__name=grade,
            classrooms__room=room
        )

    class Meta:
        model = Teacher
        fields = "__all__"
        
class StudentFilter(GenderFilterMixin, FilterSet):
    # basic fields
    first_name = filters.CharFilter(
        field_name="first_name",
        lookup_expr="icontains"
    )
    last_name = filters.CharFilter(
        field_name="last_name",
        lookup_expr="icontains"
    )
    gender = filters.CharFilter(method="filter_gender")

    # school filters
    school_id = filters.NumberFilter(field_name="school_id")
    school = filters.CharFilter(
        field_name="school__name",
        lookup_expr="icontains"
    )

    classroom =filters.CharFilter(method="filter_classroom")

    grade =filters.CharFilter(
        field_name="classroom__grade__name",
        lookup_expr="iexact"
    )
    room =filters.NumberFilter(
        field_name="classroom__room"
    )

    def filter_classroom(self, queryset, name, value):
        try:
            grade, room = value.replace(" ", "").split("/")
            return queryset.filter(
                classroom__grade__name=grade,
                classroom__room=int(room)
            )
        except Exception:
            return queryset.none()


    class Meta:
        model = Student
        fields =  "__all__"
