from rest_framework import serializers

from academic.models import Course, Department, Stream, Subject


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ["created_at", "updated_at"]


class BaseCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ["created_at", "updated_at"]


class CourseSerializer(BaseCourseSerializer):
    pass


class CourseListSerializer(BaseCourseSerializer):
    department = DepartmentSerializer(read_only=True)


class CourseShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title"]


class BaseStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        exclude = ["created_at", "updated_at"]


class StreamSerializer(BaseStreamSerializer):
    pass


class StreamListSerializer(BaseStreamSerializer):
    course = CourseShortInfoSerializer(read_only=True)


class StreamShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ["id", "title"]


class BaseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = ["created_at", "updated_at", "is_active"]


class SubjectSerializer(BaseSubjectSerializer):
    pass


class SubjectListSerializer(BaseSubjectSerializer):
    course = CourseShortInfoSerializer(read_only=True)
    stream = StreamShortInfoSerializer(read_only=True)
