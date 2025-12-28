from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, related_name="districts"
    )

    def __str__(self):
        return self.name


class SubDistrict(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="sub_districts"
    )

    def __str__(self):
        return self.name


class Address(models.Model):
    house_no = models.CharField(max_length=50)
    village_number = models.CharField(max_length=20, blank=True, null=True)
    alley = models.CharField(max_length=20, blank=True, null=True)
    junstion = models.CharField(max_length=20, blank=True, null=True)
    road = models.CharField(max_length=100, blank=True, null=True)
    province = models.ForeignKey(
        Province,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    district = models.ForeignKey(
        District,
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
    )
    sub_district = models.ForeignKey(
        SubDistrict, null=True, blank=False, on_delete=models.SET_NULL
    )
    postal_code = models.CharField(max_length=5)


class School(models.Model):
    name = models.CharField(max_length=50)
    name_abbreviation = models.CharField(max_length=5)
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name="school"
    )


class GradeLevel(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Classroom(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="classrooms"
    )
    grade = models.ForeignKey(
        GradeLevel, on_delete=models.CASCADE, related_name="Classroom"
    )
    room = models.IntegerField()

    class Meta:
        unique_together = ("grade", "room", "school")


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    UNSPECIFIC = "U", "Unspecified"


class Teacher(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIC
    )
    classrooms = models.ManyToManyField(Classroom, related_name="teacher")
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="teacher"
    )


class Student(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    gender = models.CharField(
        max_length=1, choices=Gender.choices, default=Gender.UNSPECIFIC
    )
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name="student"
    )
    school = models.ForeignKey(
        School, on_delete=models.CASCADE, related_name="student"
    )
