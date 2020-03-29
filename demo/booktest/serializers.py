from rest_framework import serializers

from .models import BookInfo, HeroInfo
# 1初试drf
# class BookInfoSerializer(serializers.ModelSerializer):
#     """图书数据序列化器"""
#     class Meta:
#         model = BookInfo
#         fields = '__all__'
# 使用fields来明确字段，__all__表名包含所有字段，也可以写明具体哪些字段，如
# 使用exclude可以明确排除掉哪些字段

class BookInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        # fields = '__all__'
        fields = ['id', 'btitle', 'bpub_date']
        exclude = ('image',)

class HeroInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroInfo
        fields = ['id', 'hname', 'hbook']
        depth = 1
#


class BookInfoSerializer(serializers.Serializer):
    # 在字段中添加validators选项参数，也可以补充验证行为
    # def about_django(value):
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("图书不是关于Django的")
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True,)
    btitle = serializers.CharField(label='名称', max_length=20)
    # btitle = serializers.CharField(label='名称', max_length=20, validators=[about_django])
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    logo = serializers.ImageField(label='图片', required=False)
    heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # validate_ < field_name >对<field_name>字段进行验证
    # def validate_btitle(self, value):
    #     if 'django' not in value.lower():
    #         raise serializers.ValidationError("图书不是关于Django的")
    #     return value
#validate
# 在序列化器中需要同时对多个字段进行比较验证时，可以定义validate方法来验证
#     def validate(self, attrs):
#         bread = attrs['bread']
#         bcomment = attrs['bcomment']
#         if bread < bcomment:
#             raise serializers.ValidationError('阅读量小于评论量')
#         return attrs
#
    def create(self, validated_data):
        """新建"""
        return BookInfo.objects.create(**validated_data)
#
    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.save()
        return instance
#
#
class BookRelateField(serializers.RelatedField):
    """自定义用于处理图书的字段"""
    def to_representation(self, value):
        return 'Book: %d %s' % (value.id, value.btitle)
#
#

class HeroInfoSerializer(serializers.Serializer):
    """英雄数据序列化器"""
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    id = serializers.IntegerField(label='ID', read_only=True)
    hname = serializers.CharField(label='名字', max_length=20)
    hgender = serializers.ChoiceField(choices=GENDER_CHOICES, label='性别', required=False)
    hcomment = serializers.CharField(label='描述信息', max_length=200, required=False, allow_null=True)
    hbook = serializers.PrimaryKeyRelatedField(read_only=True)
    hbook = BookInfoSerializer()
    hbook = BookRelateField(read_only=True)
#
#
#
# class BookReadSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BookInfo
#         fields = ('bread', )
# 添加额外参数
#         extra_kwargs = {
#             'bread': {
#                 'required': True,
#                 'min_value': 0,
#             }
#         }
#
#     def update(self, instance, validated_data):
#         instance.bread = validated_data['bread']
#         instance.save()
#         return instance
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
