# coding: utf-8
import json
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from source.models import Project, ProjectCourseFee, Campus, Course, CourseProject
from order.models import Order, UserCourse, ShoppingChart
from utils.serializer_fields import VerboseChoiceField


class CustomCampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time']


class CampusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time', 'network_course']

    def validate(self, attrs):
        if not self.instance:
            if Campus.objects.filter(name=attrs['name']):
                raise serializers.ValidationError('校区名称已存在，不能重复创建')
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('api_key') == 'all_projects':
            projects = instance.project_set.all()
            data['projects'] = ProjectSerializer(projects, many=True).data
        return data


class ProjectCourseFeeSerializer(serializers.ModelSerializer):
    course_info = serializers.CharField(source='get_course_info')

    class Meta:
        model = ProjectCourseFee
        fields = ['id', 'course_number', 'course_fee', 'course_info']


class ProjectSerializer(serializers.ModelSerializer):
    project_course_fee = ProjectCourseFeeSerializer(many=True, read_only=True)
    project_fees = serializers.ListField(write_only=True)

    class Meta:
        model = Project
        fields = ['id', 'campus', 'name', 'start_date', 'end_date', 'address', 'info', 'create_time',
                  'apply_fee', 'course_num', 'project_course_fee', 'project_fees']

    def validate(self, attrs):
        if not self.instance:
            project_fees = attrs['project_fees']
            if not project_fees:
                raise serializers.ValidationError('project_fees不能空')
            project_fees_list = [item['course_number'] for item in project_fees]
            if max(project_fees_list) != len(project_fees):
                raise serializers.ValidationError('project_fees参数传入错误，project_fees最大课程数量与传入要设置课程费用的个数不匹配')
            for item in project_fees:
                if not isinstance(item, dict):
                    raise serializers.ValidationError('project_fees的子项必须为dict')
                if ('course_number' not in item.keys()) or ('course_fee' not in item.keys()):
                    raise serializers.ValidationError('project_fees子项传入错误，必须含有course_number, course_fee字段')
        return attrs

    def create(self, validated_data):
        project_fees = []
        if 'project_fees' in validated_data.keys():
            project_fees = validated_data.pop('project_fees')
        instance = super().create(validated_data)
        if project_fees:
            ProjectCourseFee.objects.filter(project=instance).delete()
            bulk_data = []
            for item in project_fees:
                item['project'] = instance
                bulk_data.append(ProjectCourseFee(**item))
            ProjectCourseFee.objects.bulk_create(bulk_data)
        return instance

    def update(self, instance, validated_data):
        project_fees = []
        if 'project_fees' in validated_data.keys():
            project_fees = validated_data.pop('project_fees')
        instance = super().update(instance, validated_data)
        if project_fees:
            ProjectCourseFee.objects.filter(project=instance).delete()
            bulk_data = []
            for item in project_fees:
                item['project'] = instance
                bulk_data.append(ProjectCourseFee(**item))
            ProjectCourseFee.objects.bulk_create(bulk_data)
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['campus'] = CampusSerializer(instance=instance.campus).data
        if self.context.get('api_key') == 'related_courses':
            data['related_courses'] = CourseProjectSerializer(CourseProject.objects.filter(project=instance,
                                                                                           course__is_active=True,
                                                                                           project__is_active=True),
                                                              context={'api_key': 'related_courses'}, many=True).data
        return data


class UpdateProjectCourseFeeSerializer(serializers.Serializer):
    project_fees = serializers.ListField()

    def validate(self, attrs):
        project_fees = attrs['project_fees']
        if not project_fees:
            raise serializers.ValidationError('project_fees不能空')
        project_fees_list = [item['course_number'] for item in project_fees]
        if max(project_fees_list) != len(project_fees):
            raise serializers.ValidationError('project_fees参数传入错误，project_fees最大课程数量与传入要设置课程费用的个数不匹配')
        for item in project_fees:
            if not isinstance(item, dict):
                raise serializers.ValidationError('project_fees的子项必须为dict')
            if ('course_number' not in item.keys()) or ('course_fee' not in item.keys()):
                raise serializers.ValidationError('project_fees子项传入错误，必须含有course_number, course_fee字段')
        return attrs

    def save_project_course_fee(self, project, validated_data):
        ProjectCourseFee.objects.filter(project=project).delete()
        bulk_data = []
        for item in validated_data:
            item['project'] = project
            bulk_data.append(ProjectCourseFee(**item))
        ProjectCourseFee.objects.bulk_create(bulk_data)
        return


class CourseCreditSwitchSerializer(serializers.ModelSerializer):
    status = VerboseChoiceField(choices=UserCourse.CREDIT_SWITCH_STATUS)

    class Meta:
        model = UserCourse
        fields = ['id', 'status', 'post_datetime', 'post_channel', 'post_number', 'img']


class GetCourseCreditSwitchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['user']
        if UserCourse.objects.filter(user=user, status__isnull=False).exists():
            project_result = CourseProjectSerializer(UserCourse.objects.get(user=user)).data
        else:
            project_result = None
        data['project_result'] = project_result
        return data


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ['id', 'course_code', 'name', 'max_num', 'credit', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('api_key') == 'related_projects':
            data['related_projects'] = CourseProjectSerializer(CourseProject.objects.filter(course=instance,
                                                                                            course__is_active=True,
                                                                                            project__is_active=True),
                                                               context={'api_key': 'related_projects'},
                                                               many=True).data
        return data


class UserCourseSerializer(serializers.ModelSerializer):

    chart_id = serializers.IntegerField(write_only=True)
    course_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = UserCourse
        fields = ['id', 'order', 'chart_id', 'course_ids']

    def validate(self, attrs):

        if attrs['order'].status == 'TO_CONFIRM':
            raise serializers.ValidationError('订单已支付但未确认, 请联系管理员确认订单')

        if attrs['order'].status == 'TO_PAY':
            raise serializers.ValidationError('订单尚未支付')

        for course_id in attrs['course_ids']:
            if not Course.objects.filter(id=course_id).exists():
                raise serializers.ValidationError('课程id：%s 传入有误' % course_id)

        if not ShoppingChart.objects.filter(id=attrs['chart_id']).exists():
            raise serializers.ValidationError('chart_id：%s 传入有误' % attrs['chart_id'])

        chart = ShoppingChart.objects.get(id=attrs['chart_id'])

        current_course_num = UserCourse.objects.filter(user=self.context['request'].user, project=chart.project,
                                                       order=attrs['order']).count()

        if len(attrs['course_ids']) > (chart.course_num - current_course_num):
            raise serializers.ValidationError('当前剩余可选课程为：%d门，传入了%d门课程' %
                                              ((chart.course_num - current_course_num), len(attrs['course_ids']))
                                              )

        if len(attrs['course_ids']) > chart.course_num:
            raise serializers.ValidationError('该项目最大选课书为：%d门, 传入了%d门课程' %
                                              (chart.course_num, len(attrs['course_ids']))
                                              )

        if UserCourse.objects.filter(user=self.context['request'].user, project=chart.project, order=attrs['order'],
                                     course_id__in=attrs['course_ids']).exists():
            raise serializers.ValidationError('该项目已选有当前课程，请重新选择')
        attrs['project'] = chart.project
        return attrs

    def create(self, validated_data):
        user_course = []
        course_switch = []
        for course_id in validated_data['course_ids']:
            user_course.append(UserCourse(user=self.context['request'].user,
                                          order=validated_data['order'],
                                          project=validated_data['project'],
                                          course_id=course_id
                                          )
                               )
        user_courses = UserCourse.objects.bulk_create(user_course)
        return user_courses[0]


class MyScoreSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'score', 'score_grade', 'reporting_time']


class CommonImgUploadSerializer(serializers.ModelSerializer):
    """学生审课"""
    chart_id = serializers.IntegerField()
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.filter(status='CONFIRMED'))
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    # todo
    # confirm_img = Base64ImageField()
    # switch_img = Base64ImageField()
    confirm_img = serializers.ImageField(required=False)
    switch_img = serializers.ImageField(required=False)
    credit_switch_status = VerboseChoiceField(choices=UserCourse.CREDIT_SWITCH_STATUS, required=False)

    class Meta:
        model = UserCourse
        fields = ['id', 'chart_id', 'course', 'order', 'confirm_img', 'switch_img', 'credit_switch_status']

    def validate(self, attrs):
        if self.context.get('api_key') == 'student_confirm_course' and not attrs.get('confirm_img'):
            raise serializers.ValidationError('审课图片为必传参数')
        if self.context.get('api_key') == 'course_credit_switch' and not attrs.get('switch_img'):
            raise serializers.ValidationError('学分转换证明图片为必传参数')
        if self.context.get('api_key') == 'course_credit_switch' and not attrs.get('credit_switch_status'):
            raise serializers.ValidationError('学分转换状态为必填参数')
        order = attrs['order']
        if not attrs['chart_id'] in json.loads(order.chart_ids):
            raise serializers.ValidationError('chart_id: %s 不属于该订单' % attrs['chart_id'])
        if not ShoppingChart.objects.filter(id=attrs['chart_id']).exists():
            raise serializers.ValidationError('无效的chart_id')
        chart = ShoppingChart.objects.get(id=attrs['chart_id'])
        attrs['project'] = chart.project
        return attrs


class ProjectUserCourseSerializer(serializers.ModelSerializer):
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
        data['course_score'] = ProjectUserCourseSerializer(my_course).data if my_course else None
        return data


class ProjectMyScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['course'] = ProjectCourseSerializer(Course.objects.filter(usercourse__project=instance,
                                                                       course__is_active=True,
                                                                       project__is_active=True),
                                                 many=True,
                                                 context={'user': self.context['user']}).data
        return data


class CourseFilterElementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project_set'] = Project.objects.filter(campus=instance).values('id', 'name')
        return data


class CourseProjectSerializer(serializers.ModelSerializer):
    """课程项目关联"""
    class Meta:
        model = CourseProject
        fields = ['id', 'course', 'project', 'create_time', 'professor', 'start_time', 'end_time', 'address']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('api_key') == 'related_projects':
            data['project'] = ProjectSerializer(instance.project).data
        elif self.context.get('api_key') == 'related_courses':
            data['course'] = CourseSerializer(instance.course).data
        return data