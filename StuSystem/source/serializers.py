# coding: utf-8
import json
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from admin.functions import change_student_status
from authentication.models import UserInfo
from source.models import Project, ProjectCourseFee, Campus, Course, CourseProject
from order.models import Order, UserCourse, ShoppingChart, OrderChartRelation
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
    applyed_number = serializers.IntegerField(source='current_applyed_number', read_only=True)
    payed_number = serializers.IntegerField(source='current_payed_number', read_only=True)
    chose_number = serializers.IntegerField(source='current_choose_number', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'campus', 'name', 'start_date', 'end_date', 'address', 'info', 'create_time', 'chose_number',
                  'apply_fee', 'course_num', 'project_course_fee', 'project_fees', 'applyed_number', 'payed_number']

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
        validated_data['name'] = validated_data['name'].split('-')[1]
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
        data['name'] = data['campus']['name'] + '-' + data['name']
        return data


class StudentAvailableCoursesSerializer(serializers.Serializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())


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
        elif not self.context.get('request'):
            return data
        else:
            project_id = self.context.get('request').query_params.get('project')
            if project_id and project_id != '0':
                data['chose_number'] = UserCourse.objects.filter(course=instance, project_id=project_id).count()
            else:
                data['chose_number'] = UserCourse.objects.filter(course=instance).count()
        return data


class CurrentProjectCoursesSerializer(serializers.ModelSerializer):
    """查询当前项目可选课程"""
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), write_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all(), write_only=True)

    class Meta:
        model = Course
        fields = ['order', 'project']

    def validate(self, attrs):
        order = attrs['order']
        project = attrs['project']
        if not ShoppingChart.objects.filter(orderchartrelation__order=order, project=project):
            raise serializers.ValidationError('订单id : %s 不存在项目id : %s 的项目' % (order.id, project.id))
        return attrs


class UserCourseSerializer(serializers.ModelSerializer):
    chart = serializers.PrimaryKeyRelatedField(queryset=ShoppingChart.objects.all(), write_only=True)
    course_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = UserCourse
        fields = ['id', 'order', 'chart', 'course_ids']

    def validate(self, attrs):

        if not attrs.get('course_ids'):
            raise serializers.ValidationError('课程列表不能为空')

        if attrs['order'].status == 'TO_CONFIRM':
            raise serializers.ValidationError('订单已支付但未确认, 请联系管理员确认订单')

        if attrs['order'].status == 'TO_PAY':
            raise serializers.ValidationError('订单尚未支付')

        for course_id in attrs['course_ids']:
            if not Course.objects.filter(id=course_id).exists():
                raise serializers.ValidationError('课程id：%s 传入有误' % course_id)

        chart = attrs['chart']

        if not OrderChartRelation.objects.filter(chart=chart, order=attrs['order']).exists():
            raise serializers.ValidationError('传入的chart或订单号有误')

        current_course_num = UserCourse.objects.filter(user=self.context['request'].user, project=chart.project,
                                                       order=attrs['order'],
                                                       order__orderchartrelation__chart_id=chart).count()

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
        for course_id in validated_data['course_ids']:
            user_course.append(UserCourse(user=self.context['request'].user,
                                          order=validated_data['order'],
                                          project=validated_data['project'],
                                          course_id=course_id
                                          )
                               )
        user_courses = UserCourse.objects.bulk_create(user_course)
        user_all_course = UserCourse.objects.filter(user=self.context['request'].user).count()
        user_max_course = Order.objects.filter(user=self.context['request'].user, status='CONFIRMED').values_list(
            'orderchartrelation__chart__course_num')
        user_info = UserInfo.objects.filter(user=self.context['request'].user,
                                            student_status__in=['NEW', 'PERSONAL_FILE', 'ADDED_CC', 'SUPPLY_ORDER',
                                                                'PAYMENT_CONFIRM', 'TO_CHOOSE_COURSE']).exists()
        if user_info and user_all_course == sum([number[0] for number in user_max_course]):
            change_student_status(self.context['request'].user.id, 'PICKUP_COURSE')
        return user_courses[0]


class CourseConfirmSerializer(serializers.ModelSerializer):
    credit_switch_status = VerboseChoiceField(UserCourse.CREDIT_SWITCH_STATUS)
    status = VerboseChoiceField(UserCourse.STATUS)

    class Meta:
        model = UserCourse
        fields = ['id', 'course_id', 'credit_switch_status', 'order_id', 'status',
                  'post_datetime', 'post_channel', 'post_number', 'switch_img']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['name'] = instance.course.name
        data['chart'] = ShoppingChart.objects.filter(orderchartrelation__order=instance.order,
                                                     project=instance.project).values('id').first()
        data['course_code'] = instance.course.course_code
        data['project'] = {
            'id': instance.project.id,
            'name': instance.project.name
        }
        return data


class CommonImgUploadSerializer(serializers.ModelSerializer):
    """学生审课"""
    chart = serializers.PrimaryKeyRelatedField(queryset=ShoppingChart.objects.all())
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.filter(status='CONFIRMED'))
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    confirm_img = Base64ImageField(required=False)
    # confirm_img = serializers.ImageField()
    switch_img = Base64ImageField(required=False)

    class Meta:
        model = UserCourse
        fields = ['id', 'chart', 'course', 'order', 'confirm_img', 'confirm_remark', 'switch_img', 'switch_remark']

    def validate(self, attrs):
        if self.context.get('api_key') == 'student_confirm_course' and not attrs.get('confirm_img'):
            raise serializers.ValidationError('审课图片为必传参数')

        if self.context.get('api_key') == 'course_credit_switch' and not attrs.get('switch_img'):
            raise serializers.ValidationError('学分转换证明图片为必传参数')

        chart = attrs['chart']
        attrs['project'] = chart.project
        print(attrs, '\r\n', '*********************审课*******************')
        user_course = UserCourse.objects.filter(user=self.context['request'].user, project=chart.project,
                                                order=attrs['order'], course=attrs['course']).first()
        if not user_course:
            raise serializers.ValidationError('未找到用户所选课程，请检查传入参数')

        if self.context.get('api_key') == 'student_confirm_course':
            if user_course.status == 'PASS':
                raise serializers.ValidationError('审课已通过, 不能再次上传')

        if self.context.get('api_key') == 'course_credit_switch':
            if user_course.status != 'PASS':
                raise serializers.ValidationError('审课尚未完成, 不能上传学分转换图片')

            if user_course.credit_switch_status == 'SWITCHED':
                raise serializers.ValidationError('已上传学分转换图片，状态为: %s' %
                                                  dict(UserCourse.CREDIT_SWITCH_STATUS).get(
                                                      user_course.credit_switch_status))

            if user_course.credit_switch_status == 'PRE_POSTED':
                raise serializers.ValidationError('成绩单尚未寄出')
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
            data['course'] = CourseSerializer(instance.course, context={'api_key': 'related_courses_info'}).data
        return data
