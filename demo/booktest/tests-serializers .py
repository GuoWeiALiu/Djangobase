from django.test import TestCase

# Create your tests here.
# 本部分是测试序列化使用的增删改查，需要在cli中执行
# python manage.py shell
'''

1 基本使用
1） 先查询出一个图书对象

from booktest.models import BookInfo

book = BookInfo.objects.get(id=2)
2） 构造序列化器对象

from booktest.serializers import BookInfoSerializer

serializer = BookInfoSerializer(book)
3）获取序列化数据

通过data属性可以获取序列化后的数据

serializer.data
# {'id': 2, 'btitle': '天龙八部', 'bpub_date': '1986-07-24', 'bread': 36, 'bcomment': 40, 'image': None}
4）如果要被序列化的是包含多条数据的查询集QuerySet，可以通过添加many=True参数补充说明

book_qs = BookInfo.objects.all()
serializer = BookInfoSerializer(book_qs, many=True)
serializer.data
# [OrderedDict([('id', 2), ('btitle', '天龙八部'), ('bpub_date', '1986-07-24'), ('bread', 36), ('bcomment', 40), ('image', N]), OrderedDict([('id', 3), ('btitle', '笑傲江湖'), ('bpub_date', '1995-12-24'), ('bread', 20), ('bcomment', 80), ('image'ne)]), OrderedDict([('id', 4), ('btitle', '雪山飞狐'), ('bpub_date', '1987-11-11'), ('bread', 58), ('bcomment', 24), ('ima None)]), OrderedDict([('id', 5), ('btitle', '西游记'), ('bpub_date', '1988-01-01'), ('bread', 10), ('bcomment', 10), ('im', 'booktest/xiyouji.png')])]
2 关联对象嵌套序列化
如果需要序列化的数据中包含有其他关联对象，则对关联对象数据的序列化需要指明。

例如，在定义英雄数据的序列化器时，外键hbook（即所属的图书）字段如何序列化？

我们先定义HeroInfoSerialzier除外键字段外的其他部分

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
对于关联字段，可以采用以下几种方式：

1） PrimaryKeyRelatedField
此字段将被序列化为关联对象的主键。

hbook = serializers.PrimaryKeyRelatedField(label='图书', read_only=True)
或
hbook = serializers.PrimaryKeyRelatedField(label='图书', queryset=BookInfo.objects.all())
指明字段时需要包含read_only=True或者queryset参数：

包含read_only=True参数时，该字段将不能用作反序列化使用
包含queryset参数时，将被用作反序列化时参数校验使用
使用效果：

from booktest.serializers import HeroInfoSerializer
from booktest.models import HeroInfo
hero = HeroInfo.objects.get(id=6)
serializer = HeroInfoSerializer(hero)
serializer.data
# {'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': 2}
2) StringRelatedField
此字段将被序列化为关联对象的字符串表示方式（即__str__方法的返回值）

hbook = serializers.StringRelatedField(label='图书')
使用效果

{'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': '天龙八部'}
3）HyperlinkedRelatedField
此字段将被序列化为获取关联对象数据的接口链接

hbook = serializers.HyperlinkedRelatedField(label='图书', read_only=True, view_name='books-detail')
必须指明view_name参数，以便DRF根据视图名称寻找路由，进而拼接成完整URL。

使用效果

{'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': 'http://127.0.0.1:8000/books/2/'}
我们暂时还没有定义视图，此方式不再演示。

4）SlugRelatedField
此字段将被序列化为关联对象的指定字段数据

hbook = serializers.SlugRelatedField(label='图书', read_only=True, slug_field='bpub_date')
slug_field指明使用关联对象的哪个字段

使用效果

{'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': datetime.date(1986, 7, 24)}
5）使用关联对象的序列化器
hbook = BookInfoSerializer()
使用效果

{'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': OrderedDict([('id', 2), ('btitle', '天龙八部')te', '1986-07-24'), ('bread', 36), ('bcomment', 40), ('image', None)])}
6） 重写to_representation方法
序列化器的每个字段实际都是由该字段类型的to_representation方法决定格式的，可以通过重写该方法来决定格式。

注意，to_representations方法不仅局限在控制关联对象格式上，适用于各个序列化器字段类型。

自定义一个新的关联字段：

class BookRelateField(serializers.RelatedField):
    """自定义用于处理图书的字段"""
    def to_representation(self, value):
        return 'Book: %d %s' % (value.id, value.btitle)
指明hbook为BookRelateField类型

hbook = BookRelateField(read_only=True)
使用效果

{'id': 6, 'hname': '乔峰', 'hgender': 1, 'hcomment': '降龙十八掌', 'hbook': 'Book: 2 天龙八部'}
many参数
如果关联的对象数据不是只有一个，而是包含多个数据，如想序列化图书BookInfo数据，每个BookInfo对象关联的英雄HeroInfo对象可能有多个，此时关联字段类型的指明仍可使用上述几种方式，只是在声明关联字段时，多补充一个many=True参数即可。

此处仅拿PrimaryKeyRelatedField类型来举例，其他相同。

在BookInfoSerializer中添加关联字段：

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
    heroinfo_set = serializers.PrimaryKeyRelatedField(read_only=True, many=True)  # 新增
使用效果：

from booktest.serializers import BookInfoSerializer
from booktest.models import BookInfo
book = BookInfo.objects.get(id=2)
serializer = BookInfoSerializer(book)
serializer.data
# {'id': 2, 'btitle': '天龙八部', 'bpub_date': '1986-07-24', 'bread': 36, 'bcomment

如我们前面定义过的BookInfoSerializer

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20)
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
通过构造序列化器对象，并将要反序列化的数据传递给data构造参数，进而进行验证

from booktest.serializers import BookInfoSerializer
data = {'bpub_date': 123}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # 返回False
serializer.errors
# {'btitle': [ErrorDetail(string='This field is required.', code='required')], 'bpub_date': [ErrorDetail(string='Date has wrong format. Use one of these formats instead: YYYY[-MM[-DD]].', code='invalid')]}
serializer.validated_data  # {}

data = {'btitle': 'python'}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # True
serializer.errors  # {}
serializer.validated_data  #  OrderedDict([('btitle', 'python')])
is_valid()方法还可以在验证失败时抛出异常serializers.ValidationError，可以通过传递raise_exception=True参数开启，REST framework接收到此异常，会向前端返回HTTP 400 Bad Request响应。

# Return a 400 response if the data was invalid.
serializer.is_valid(raise_exception=True)
如果觉得这些还不够，需要再补充定义验证行为，可以使用以下三种方法：

1）validate_<field_name>
对<field_name>字段进行验证，如

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    ...

    def validate_btitle(self, value):
        if 'django' not in value.lower():
            raise serializers.ValidationError("图书不是关于Django的")
        return value
测试

from booktest.serializers import BookInfoSerializer
data = {'btitle': 'python'}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # False
serializer.errors
#  {'btitle': [ErrorDetail(string='图书不是关于Django的', code='invalid')]}
2）validate
在序列化器中需要同时对多个字段进行比较验证时，可以定义validate方法来验证，如

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    ...

    def validate(self, attrs):
        bread = attrs['bread']
        bcomment = attrs['bcomment']
        if bread < bcomment:
            raise serializers.ValidationError('阅读量小于评论量')
        return attrs
测试

from booktest.serializers import BookInfoSerializer
data = {'btitle': 'about django', 'bread': 10, 'bcomment': 20}
s = BookInfoSerializer(data=data)
s.is_valid()  # False
s.errors
#  {'non_field_errors': [ErrorDetail(string='阅读量小于评论量', code='invalid')]}
3）validators
在字段中添加validators选项参数，也可以补充验证行为，如


def about_django(value):
    if 'django' not in value.lower():
        raise serializers.ValidationError("图书不是关于Django的")

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    id = serializers.IntegerField(label='ID', read_only=True)
    btitle = serializers.CharField(label='名称', max_length=20, validators=[about_django])
    bpub_date = serializers.DateField(label='发布日期', required=False)
    bread = serializers.IntegerField(label='阅读量', required=False)
    bcomment = serializers.IntegerField(label='评论量', required=False)
    image = serializers.ImageField(label='图片', required=False)
测试：

from booktest.serializers import BookInfoSerializer
data = {'btitle': 'python'}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # False
serializer.errors
#  {'btitle': [ErrorDetail(string='图书不是关于Django的', code='invalid')]}
REST framework提供的validators:

UniqueValidator

单字段唯一，如

from rest_framework.validators import UniqueValidator

slug = SlugField(
    max_length=100,
    validators=[UniqueValidator(queryset=BlogPost.objects.all())]
)
UniqueTogetherValidation

联合唯一，如

from rest_framework.validators import UniqueTogetherValidator

class ExampleSerializer(serializers.Serializer):
    # ...
    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=ToDoItem.objects.all(),
                fields=('list', 'position')
            )
        ]
2. 保存
如果在验证成功后，想要基于validated_data完成数据对象的创建，可以通过实现create()和update()两个方法来实现。

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    ...

    def create(self, validated_data):
        """新建"""
        return BookInfo(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        return instance
如果需要在返回数据对象的时候，也将数据保存到数据库中，则可以进行如下修改

class BookInfoSerializer(serializers.Serializer):
    """图书数据序列化器"""
    ...

    def create(self, validated_data):
        """新建"""
        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """更新，instance为要更新的对象实例"""
        instance.btitle = validated_data.get('btitle', instance.btitle)
        instance.bpub_date = validated_data.get('bpub_date', instance.bpub_date)
        instance.bread = validated_data.get('bread', instance.bread)
        instance.bcomment = validated_data.get('bcomment', instance.bcomment)
        instance.save()
        return instance
实现了上述两个方法后，在反序列化数据的时候，就可以通过save()方法返回一个数据对象实例了

book = serializer.save()
如果创建序列化器对象的时候，没有传递instance实例，则调用save()方法的时候，create()被调用，相反，如果传递了instance实例，则调用save()方法的时候，update()被调用。

from db.serializers import BookInfoSerializer
data = {'btitle': '封神演义'}
serializer = BookInfoSerializer(data=data)
serializer.is_valid()  # True
serializer.save()  # <BookInfo: 封神演义>

from db.models import BookInfo
book = BookInfo.objects.get(id=2)
data = {'btitle': '倚天剑'}
serializer = BookInfoSerializer(book, data=data)
serializer.is_valid()  # True
serializer.save()  # <BookInfo: 倚天剑>
book.btitle  # '倚天剑'
两点说明：
1） 在对序列化器进行save()保存时，可以额外传递数据，这些数据可以在create()和update()中的validated_data参数获取到

serializer.save(owner=request.user)
2）默认序列化器必须传递所有required的字段，否则会抛出验证异常。但是我们可以使用partial参数来允许部分字段更新

# Update `comment` with partial data
serializer = CommentSerializer(comment, data={'content': u'foo bar'}, partial=True)

'''