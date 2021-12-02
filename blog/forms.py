
from django import forms
from django.forms.fields import ImageField
from django.forms.forms import DeclarativeFieldsMetaclass

class bp_0(forms.Form):
    desc = forms.CharField(widget=forms.Textarea())
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class bp_2(forms.Form):
    changes = forms.CharField(widget=forms.Textarea())
    Action = forms.ChoiceField(choices=(('u', 'Update requirements and request changes'),('a', 'Accept current image as final')))

class sp_1(forms.Form):
    Accept = forms.ChoiceField(choices=(('y', 'YES'),('n', 'NO')))

class sp_12(forms.Form):
    image = forms.ImageField()
