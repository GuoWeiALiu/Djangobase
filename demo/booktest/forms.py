from django import forms
from .models import BookInfo

# 创建一个Form类来描述这个表单
# class BookInfoForm(forms.Form):
#     btitle = forms.CharField(label='图书名称', required=True, max_length=20)
#     bpub_date = forms.DateField(label='发型日期', required=True)

# 模型类表单
class BookInfoForm(forms.ModelForm):
    class Meta:
        model = BookInfo
        fields = ('btitle', 'bpub_date')



