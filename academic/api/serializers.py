from rest_framework import serializers

from academic.models import Course, Department, Stream


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
    department = serializers.StringRelatedField()


class BaseStreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        exclude = ["created_at", "updated_at"]


class StreamSerializer(BaseStreamSerializer):
    pass


class StreamListSerializer(BaseStreamSerializer):
    course = serializers.StringRelatedField()
