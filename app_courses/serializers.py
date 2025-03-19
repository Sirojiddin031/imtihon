from rest_framework import serializers
from app_courses.models import (
    Group, Subject, Course, Table, TableType,
    Homework, HomeworkSubmission, HomeworkReview
)

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GetGroupByIdsSerializer(serializers.Serializer):
    group_ids = serializers.ListField(child=serializers.IntegerField())


class SubjectSerializer(serializers.ModelSerializer): # serializer for fan model
    class Meta:
        model = Subject
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer): # serializer for  course model
    class Meta:
        model = Course
        fields = '__all__'


class TableSerializer(serializers.ModelSerializer): # serializer for ttable model
    class Meta:
        model = Table
        fields = '__all__'


class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = '__all__'


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'
        extra_kwargs = {'teacher': {'read_only': True}}


class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkSubmission
        fields = '__all__'
        extra_kwargs = {
            'student': {'read_only': True},
            'is_checked': {'read_only': True} 
        }


class HomeworkReviewSerializer(serializers.ModelSerializer): # serializer for homework qoshimcha model
    class Meta:
        model = HomeworkReview
        fields = '__all__'
        extra_kwargs = {
            'teacher': {'read_only': True}  
        }


class RemoveStudentFromGroupSerializer(serializers.Serializer): 
    student_id = serializers.IntegerField()


class RemoveTeacherFromGroupSerializer(serializers.Serializer): 
    teacher_id = serializers.IntegerField()


class GroupAddStudent(serializers.Serializer): 
    student_id = serializers.IntegerField()


class GroupAddTeacher(serializers.Serializer): 
    teacher_id = serializers.IntegerField()
