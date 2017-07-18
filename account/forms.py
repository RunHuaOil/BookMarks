from django import forms
from django.forms import TextInput
from django.contrib.auth.models import User
from .models import Profile
import logging

logger = logging.getLogger(__name__)


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(widget=forms.PasswordInput, label='密  码')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='请再输入密码', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        # logger.debug(User.objects.all())
        # logger.debug(type(User.objects.all()))
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('两次密码输入不一致')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email'] == '':
            raise forms.ValidationError('邮箱不能为空')
        for each_user in User.objects.all():
            if cd['email'] == each_user.email:
                raise forms.ValidationError('该邮箱已经注册过')
        return cd['email']

    def clean_first_name(self):
        cd = self.cleaned_data
        if cd['first_name'] == '':
            raise forms.ValidationError('名字不能为空')
        for each_user in User.objects.all():
            if cd['first_name'] == each_user.first_name:
                raise forms.ValidationError('这个名字已经有人用啦')
        return cd['first_name']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']
        widgets = {
            'date_of_birth': TextInput(attrs={'type': 'date'}),
        }


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(disabled=True, label='邮箱地址')
    first_name = forms.CharField(disabled=True, label='名字')

    class Meta:
        model = User
        fields = ['first_name', 'email']


