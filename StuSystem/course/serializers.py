# coding: utf-8
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from course.models import Project, ProjectCourseFee, Campus, CampusCountry, CampusCountryRelation, \
    CampusType, Course, ProjectResult
from order.models import Order, UserCourse
from utils.serializer_fields import VerboseChoiceField


class CampusTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CampusType
        fields = ['id', 'title', 'create_time']


class CustomCampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time']


class CampusCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = CampusCountry
        fields = ['id', 'name', 'campus_type', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        campus_set = Campus.objects.filter(campuscountryrelation__campus_country=instance)
        campus_set_data = CustomCampusSerializer(campus_set, many=True).data
        data['campus_set'] = campus_set_data
        data['campus_type'] = CampusTypeSerializer(instance=instance.campus_type).data
        return data


class CustomCampusTypeSerializer(serializers.ModelSerializer):
    campuscountry_set = CampusCountrySerializer(many=True)

    class Meta:
        model = CampusType
        fields = ['id', 'title', 'create_time', 'campuscountry_set']


class CampusSerializer(serializers.ModelSerializer):
    campus_country = serializers.ListField(write_only=True)

    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time', 'campus_country']

    def validate(self, attrs):
        if not self.instance:
            if Campus.objects.filter(name=attrs['name']):
                raise serializers.ValidationError('校区名称已存在，不能重复创建')
        if 'campus_country' in attrs.keys():
            campus_country = attrs['campus_country']
            campus_country_instance = []
            for item in campus_country:
                if not CampusCountry.objects.filter(id=item).exists():
                    raise serializers.ValidationError('无效的campus_country id值：%s' % item)
                campus_country_instance.append(CampusCountry.objects.get(id=item))
            attrs['campus_country'] = campus_country_instance
        return attrs

    def create(self, validated_data):
        campus_countries = validated_data.pop('campus_country')
        instance = super().create(validated_data)
        campus_country_relation_instance = []
        for campus_country in campus_countries:
            campus_country_relation_instance.append(CampusCountryRelation(campus=instance, campus_country=campus_country))
        CampusCountryRelation.objects.bulk_create(campus_country_relation_instance)
        return instance

    def update(self, instance, validated_data):
        if 'campus_country' in validated_data.keys():
            campus_countries = validated_data.pop('campus_country')
            CampusCountryRelation.objects.filter(campus=instance).delete()
            campus_country_relation_instance = []
            for campus_country in campus_countries:
                campus_country_relation_instance.append(CampusCountryRelation(campus=instance, campus_country=campus_country))
            CampusCountryRelation.objects.bulk_create(campus_country_relation_instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        campus_countries = CampusCountry.objects.filter(campuscountryrelation__campus=instance)
        campus_countries_data = CampusCountrySerializer(campus_countries, many=True).data
        data['campus_country'] = campus_countries_data
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
                  'apply_fee', 'course_num', 'project_course_fee', 'project_fees', 'campus_country']

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
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        serializer = CampusSerializer(instance=instance.campus)
        data['campus'] = serializer.data
        data['campus_country'] = CampusCountrySerializer(instance=instance.campus_country).data \
            if instance.campus_country else None
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


class MyProjectsSerializer(ProjectSerializer):
    def to_representation(self, instance):
        user = self.context['user']
        data = super().to_representation(instance)
        order_info = instance.order_set.filter(user=user, project=instance).first()
        data['order_status'] = {'key': order_info.status, 'verbose': dict(Order.STATUS).get(order_info.status)}
        data['order_remark'] = order_info.remark
        current_course_num = UserCourse.objects.filter(user=self.context['user'], order__project=instance).count()
        data['current_course_num'] = current_course_num
        my_courses = Course.objects.filter(usercourse__order__project=instance, usercourse__user=user)
        data['my_courses'] = CourseSerializer(my_courses, many=True).data
        return data


class ProjectResultSerializer(serializers.ModelSerializer):
    status = VerboseChoiceField(choices=ProjectResult.STATUS)

    class Meta:
        model = ProjectResult
        fields = ['id', 'status', 'post_datetime', 'post_channel', 'post_number', 'img']


class GetProjectResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['user']
        if ProjectResult.objects.filter(user=user, status__isnull=False).exists():
            project_result = ProjectResultSerializer(ProjectResult.objects.get(user=user)).data
        else:
            project_result = None
        data['project_result'] = project_result
        return data


class CourseSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    class Meta:
        model = Course
        fields = ['id', 'project', 'course_code', 'name', 'max_num', 'credit', 'professor', 'start_time', 'end_time',
                  'create_time', 'address', 'syllabus']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['current_course_num'] = UserCourse.objects.filter(course=instance).count()
        return data


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
        ProjectResult.objects.get_or_create(user=validated_data['user'])
        return super().create(validated_data)


class MyCourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['id', 'name']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        courses = Course.objects.filter(usercourse__order__project=instance)
        current_course_num = UserCourse.objects.filter(user=self.context['user'], order__project=instance).count()
        my_courses = CourseSerializer(courses, many=True).data
        data['course_num'] = instance.course_num
        data['current_course_num'] = current_course_num
        data['my_courses'] = my_courses
        return data


class MyScoreSerializer(serializers.ModelSerializer):
    course = CourseSerializer()

    class Meta:
        model = UserCourse
        fields = ['id', 'course', 'score', 'score_grade', 'reporting_time']


class ConfirmPhotoSerializer(serializers.Serializer):
    confirm_photo = Base64ImageField()


class UpdateImgSerializer(serializers.Serializer):
    img = Base64ImageField()

    def validate_project_result(self, project, user):
        if not ProjectResult.objects.filter(user=user, status='SUCCESS').exists():
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


class CourseFilterElementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campus
        fields = ['id', 'name', 'info', 'create_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project_set'] = Project.objects.filter(campus=instance).values('id', 'name')
        return data