# coding: utf-8
import random, string
from rest_framework import serializers
from course.models import Project, ProjectCourseFee, Campus, CampusType, Course, ProjectResult
from order.models import UserCourse
from drf_extra_fields.fields import Base64ImageField
from utils.serializer_fields import VerboseChoiceField
from order.models import Order


class CampusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusType
        fields = ['id', 'title', 'create_time']


class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'campus_type', 'info', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['campus_type'] = CampusTypeSerializer(instance.campus_type).data
        return data


class ProjectCourseFeeSerializer(serializers.ModelSerializer):
    course_info = serializers.CharField(source='get_course_info')

    class Meta:
        model = ProjectCourseFee
        fields = ['id', 'course_number', 'course_fee', 'course_info']


class ProjectSerializer(serializers.ModelSerializer):
    project_course_fee = ProjectCourseFeeSerializer(many=True)

    class Meta:
        model = Project
        fields = ['id', 'campus', 'name', 'start_date', 'end_date', 'address', 'info', 'create_time',
                  'apply_fee', 'course_num', 'project_course_fee']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        serializer = CampusSerializer(instance=instance.campus)
        data['campus'] = serializer.data
        return data


class MyProjectsSerializer(ProjectSerializer):
    def to_representation(self, instance):
        user = self.context['user']
        data = super().to_representation(instance)
        order_info = instance.order_set.filter(user=user, project=instance).first()
        data['order_status'] = {'key': order_info.status, 'verbose': dict(Order.STATUS).get(order_info.status)}
        data['order_remark'] = order_info.remark
        current_course_num = UserCourse.objects.filter(user=self.context['user'], project_id=instance).count()
        data['current_course_num'] = current_course_num
        my_courses = Course.objects.filter(usercourse__project=instance, usercourse__user=user)
        data['my_courses'] = CourseSerializer(my_courses, many=True).data
        return data


class ProjectResultSerializer(serializers.ModelSerializer):
    status = VerboseChoiceField(choices=ProjectResult.STATUS)

    class Meta:
        model = ProjectResult
        fields = ['id', 'status', 'post_date', 'post_channel', 'post_number', 'img']


class GetProjectResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['user']
        if ProjectResult.objects.filter(user=user, project=instance, status__isnull=False).exists():
            project_result = ProjectResultSerializer(ProjectResult.objects.get(user=user, project=instance)).data
        else:
            project_result = None
        data['project_result'] = project_result
        return data


class CourseSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    course_code = serializers.CharField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'project', 'course_code', 'name', 'max_num', 'credit', 'professor', 'start_time', 'end_time',
                  'create_time', 'address', 'syllabus']

    def create(self, validated_data):
        validated_data['course_code'] = ''.join(random.sample(string.digits + string.ascii_uppercase, 10))
        return super().create(validated_data)


class CurrentCourseProjectSerializer(serializers.Serializer):
    project = serializers.IntegerField()
    user = serializers.IntegerField()

    def validate(self, attrs):
        if not Project.objects.filter(id=attrs['project']).exists():
            raise serializers.ValidationError('项目不存在')

        if not Order.objects.filter(user_id=attrs['user'], project_id=attrs['project'],
                                    ).exists():
            raise serializers.ValidationError('订单不存在')

        if not Order.objects.filter(user_id=attrs['user'], project_id=attrs['project'],
                                    status='TO_PAY').exists():
            raise serializers.ValidationError('订单未支付')
        return attrs


class CreateUserCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'order', 'user']

    def validate(self, attrs):
        if not Order.objects.filter(user=attrs['user'], project=attrs['order'].project,
                                    ).exists():
            raise serializers.ValidationError('订单不存在')

        if attrs['order'] == 'TO_CONFIRM':
            raise serializers.ValidationError('订单已支付但未确认, 请联系管理员确认订单')

        if attrs['order'] == 'TO_PAY':
            raise serializers.ValidationError('订单尚未支付')

        if UserCourse.objects.filter(order=attrs['order']).count() >= int(attrs['order'].course_num):
            raise serializers.ValidationError('订单已达到最大选课数，不能再继续选课')

        if UserCourse.objects.filter(user=attrs['user'], order=attrs['order'],
                                     course=attrs['course']).exists():
            raise serializers.ValidationError('已选该课程，不能重复选择')
        return attrs

    def create(self, validated_data):
        ProjectResult.objects.get_or_create(user=validated_data['user'], project=validated_data['order'].project)
        return super().create(validated_data)


class MyCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        courses = Course.objects.filter(usercourse__project=instance)
        current_course_num = UserCourse.objects.filter(user=self.context['user'], project_id=instance).count()
        my_courses = CourseSerializer(courses, many=True).data
        data['course_num'] = instance.course_num
        data['current_course_num'] = current_course_num
        data['my_courses'] = my_courses
        return data


class MyScoreSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'score', 'score_grade']


class ConfirmPhotoSerializer(serializers.Serializer):
    confirm_photo = Base64ImageField()


class UpdateImgSerializer(serializers.Serializer):
    img = Base64ImageField()

    def validate_project_result(self, project, user):
        if not ProjectResult.objects.filter(project=project, user=user, status='SUCCESS').exists():
            raise serializers.ValidationError('学分转换未完成，不能上传图片')
        return


class UserCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCourse
        fields = ['score', 'score_grade', 'reporting_time']


class ProjectCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_code', 'name', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        my_course = UserCourse.objects.filter(user=self.context['user'], course=instance).first()
        data['course_score'] = UserCourseSerializer(my_course).data if my_course else None
        return data


class ProjectMyScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course'] = ProjectCourseSerializer(Course.objects.filter(usercourse__project=instance), many=True,
                                                 context={'user': self.context['user']}).data
        return data