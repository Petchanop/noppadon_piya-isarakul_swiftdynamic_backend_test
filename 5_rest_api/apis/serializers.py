from rest_framework import serializers
from apis.models import (
    GradeLevel,
    School,
    Address,
    SubDistrict,
    District,
    Province,
    Classroom,
    Gender,
    Student,
    Teacher,
)
# code here


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = District
        fields = "__all__"


class SubDistrictSerializer(serializers.ModelSerializer):
    district = DistrictSerializer()

    class Meta:
        model = SubDistrict
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    province = serializers.SlugRelatedField(
        slug_field="name", queryset=Province.objects.all()
    )
    district = serializers.SlugRelatedField(
        slug_field="name", queryset=District.objects.all()
    )
    sub_district = serializers.SlugRelatedField(
        slug_field="name", queryset=SubDistrict.objects.all()
    )

    class Meta:
        model = Address
        fields = "__all__"

    def to_internal_value(self, data):
        prov_name = data.get("province")
        dist_name = data.get("district")
        sub_name = data.get("sub_district")

        if prov_name and dist_name and sub_name:
            province_obj, _ = Province.objects.get_or_create(name=prov_name)
            district_obj, _ = District.objects.get_or_create(
                name=dist_name, province=province_obj
            )
            sub_district_obj, _ = SubDistrict.objects.get_or_create(
                name=sub_name, district=district_obj
            )
            data["province"] = province_obj
            data["district"] = district_obj
            data["sub_district"] = sub_district_obj

        return super().to_internal_value(data)


class SchoolSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = School
        fields = "__all__"

    def create(self, validated_data):
        address_data = validated_data.pop("address")

        province_name = address_data.pop("province")
        district_name = address_data.pop("district")
        sub_dist_name = address_data.pop("sub_district")
        province_obj, _ = Province.objects.get_or_create(name=province_name)

        district_obj, _ = District.objects.get_or_create(
            name=district_name, province=province_obj
        )

        sub_district_obj, _ = SubDistrict.objects.get_or_create(
            name=sub_dist_name, district=district_obj
        )

        address = Address.objects.create(
            province=province_obj,
            district=district_obj,
            sub_district=sub_district_obj,
            **address_data,
        )
        school = School.objects.create(address=address, **validated_data)
        return school

    def update(self, instance, validated_data):
        address_data = validated_data.pop("address", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if address_data:
            address = instance.address
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        return instance


class SchoolFilterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)


class ClassroomSerializer(serializers.ModelSerializer):
    grade = serializers.SlugRelatedField(
        slug_field="name",
        queryset=GradeLevel.objects.all()
    )
    room = serializers.IntegerField()
    school = serializers.SlugRelatedField(
        slug_field="name",
        queryset=School.objects.all()
    )
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = ["id", "grade", "room", "display_name", "school"]
        validators = []

    def get_display_name(self, obj):
        return f"{obj.grade}/{obj.room}"

    def to_internal_value(self, data):
        grade_name = data.get("grade")
        room = data.get("room")
        grade_obj, _ = GradeLevel.objects.get_or_create(name=grade_name)
        data["grade"] = grade_obj
        data["room"] = room
        return super().to_internal_value(data)

    def create(self, validated_data):
        school = validated_data["school"]
        grade = validated_data.pop("grade")
        room_data = validated_data.pop("room")
        classroom, _ = Classroom.objects.get_or_create(
            grade=grade,
            room=room_data,
            school=school,
        )

        return classroom
    
class ClassroomNestedSerializer(serializers.ModelSerializer):
    grade = serializers.CharField()
    display_name = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = ["id", "grade", "room", "display_name"]

    def get_display_name(self, obj):
        return f"{obj.grade}/{obj.room}"



class ChoiceField(serializers.ChoiceField):

    def to_representation(self, value):
        if value == "" and self.allow_blank:
            return value
        return self._choices[value]

    def to_internal_value(self, data):
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class StudentSerializer(serializers.ModelSerializer):
    gender = ChoiceField(choices=Gender.choices)
    classroom = ClassroomNestedSerializer()
    school = serializers.SlugRelatedField(
        slug_field="name", queryset=School.objects.all()
    )

    class Meta:
        model = Student
        fields = "__all__"
    
    def create(self, validated_data):
        classroom_data = validated_data.pop("classroom")
        school = validated_data["school"]

        grade_name = classroom_data["grade"]
        room = classroom_data["room"]

        grade, _ = GradeLevel.objects.get_or_create(name=grade_name)
        classroom, _ = Classroom.objects.get_or_create(
            grade=grade,
            room=room,
            school=school
        )

        student = Student.objects.create(classroom=classroom, **validated_data)
        return student

    def update(self, instance, validated_data):
        classroom_data = validated_data.pop("classroom", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if classroom_data is not None:
            grade_name = classroom_data["grade"]
            room = classroom_data["room"]
            school = instance.school
            grade, _ = GradeLevel.objects.get_or_create(name=grade_name)
            classroom, _ = Classroom.objects.get_or_create(
                grade=grade,
                room=room,
                school=school
            )

            instance.classroom = classroom
            instance.save()

        return instance
    
class StudentDetailSerializer(StudentSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        classroom = instance.classroom
        if classroom:
            data["classroom"] = {
                "grade": classroom.grade.name,
                "room": classroom.room,
            }
        else:
            data["classroom"] = None

        return data
    
class TeacherSerializer(serializers.ModelSerializer):
    gender = ChoiceField(choices=Gender.choices)
    classrooms = ClassroomNestedSerializer(many=True)
    school = serializers.SlugRelatedField(
        slug_field="name", queryset=School.objects.all()
    )

    class Meta:
        model = Teacher
        fields = "__all__"

    def create(self, validated_data):
        classrooms_data = validated_data.pop("classrooms")

        teacher = Teacher.objects.create(**validated_data)

        classroom_objs = []
        for classroom_data in classrooms_data:
            grade_name = classroom_data["grade"]
            room = classroom_data["room"]
            school = validated_data["school"]
            
            grade, _ = GradeLevel.objects.get_or_create(name=grade_name)
            
            classroom, _ = Classroom.objects.get_or_create(
                grade=grade,
                room=room,
                school=school
            )
            classroom_objs.append(classroom)

        teacher.classrooms.set(classroom_objs)
        return teacher

    def update(self, instance, validated_data):

        classrooms_data = validated_data.pop("classrooms", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if classrooms_data is not None:
            classroom_objs = []
            for classroom_data in classrooms_data:
                grade_name = classroom_data["grade"]
                room = classroom_data["room"]
                school = instance.school
                
                grade, _ = GradeLevel.objects.get_or_create(name=grade_name)
                classroom, _ = Classroom.objects.get_or_create(grade=grade, room=room, school=school)
                classroom_objs.append(classroom)

            instance.classrooms.set(classroom_objs)

        return instance
    
class TeacherDetailSerializer(TeacherSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        classrooms = instance.classrooms.all()

        data["classrooms"] = [
            {
                "grade": classroom.grade.name,
                "room": classroom.room,
            }
            for classroom in classrooms
        ]

        return data
    
class SchoolDetailSerializer(SchoolSerializer):
    classrooms = ClassroomNestedSerializer(many=True, read_only=True)
    teachers = TeacherSerializer(
        many=True, read_only=True, source="teacher"
    )
    students = StudentSerializer(
        many=True, read_only=True, source="student"
    )
    classrooms_count = serializers.IntegerField(read_only=True)
    teachers_count = serializers.IntegerField(read_only=True)
    students_count = serializers.IntegerField(read_only=True)

class ClassroomDetailSerializer(ClassroomSerializer):
    teachers = TeacherSerializer(
        many=True, read_only=True, source="teacher"
    )
    students = StudentSerializer(
        many=True, read_only=True, source="student"
    )
    
    class Meta(ClassroomSerializer.Meta):
        fields = ClassroomSerializer.Meta.fields + [
            "teachers",
            "students",
        ]