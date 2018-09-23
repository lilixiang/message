# -*- encoding:utf8 -*-

__author__ = 'luke'

from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

from message.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='用户名', required=True,
                               widget=forms.TextInput(attrs={'placeholder': '用户名'}),
                               error_messages={'required': '用户名不能为空!'})
    password = forms.CharField(max_length=30, label='密码', required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
                               error_messages={'required': '密码不能为空!'}
                               )
    remember = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def auth_user(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            msg = '用户名或密码错误!'
            self._errors["username"] = self.error_class([msg])
            return self
        else:
            return self


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=30, label='用户名', required=True,
                               widget=forms.TextInput(attrs={'placeholder': '用户名'}),
                               error_messages={'required': '用户名不能为空！'}
                               )
    password = forms.CharField(max_length=30, label='密码', required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
                               error_messages={'required': '密码不能为空！'}
                               )
    password_confirm = forms.CharField(max_length=30, label='密码确认', required=True,
                                       widget=forms.PasswordInput(attrs={'placeholder': '密码确认'}),
                                       error_messages={'required': '密码确认不能为空！'})

    email = forms.EmailField(max_length=30, label='邮箱', required=True,
                             widget=forms.TextInput(attrs={'placeholder': '邮箱'}),
                             error_messages={'required': '邮箱不能为空！', 'invalid': '请输入正确的邮箱！'})

    def auth_user(self):
        username = self.cleaned_data.get('username')
        is_exist = User.objects.filter(username=username)

        if is_exist:
            msg = '用户名已存在'
            self._errors["username"] = self.error_class([msg])
            return self
        else:
            return self

    def auth_email(self):
        email = self.cleaned_data.get('email')
        is_exist = User.objects.filter(email=email)

        if is_exist:
            msg = '邮箱已被注册'
            self._errors["email"] = self.error_class([msg])
            return self
        else:
            return self


class SendMessageForm(forms.Form):
    receiver_id = forms.IntegerField(label='接受人id', required=True,
                                     widget=forms.NumberInput(attrs={'placeholder': '接受人编号'}),
                                     error_messages={'required': '接受人编号不能为空！'}
                                     )

    content = forms.CharField(max_length=512, label='发送内容', required=True,
                              widget=forms.TextInput(attrs={'placeholder': '发送内容'}),
                              error_messages={'required': '发送内容不能为空！', 'invalid': '发送内容不能为空'})


class InboxSendMessageForm(forms.Form):

    content = forms.CharField(max_length=512, label='发送内容', required=True,
                              widget=forms.TextInput(attrs={'placeholder': '发送内容'}),
                              error_messages={'required': '发送内容不能为空！', 'invalid': '发送内容不能为空'})


class DeleteContactForm(forms.Form):
    contact_id = forms.IntegerField(label='联系人编号', required=True,
                                    widget=forms.NumberInput(attrs={'placeholder': '联系人编号'}),
                                    error_messages={'required': '联系人编号不能为空！'}
                                    )


class DeleteMessageForm(forms.Form):
    message_id = forms.IntegerField(label='消息编号', required=True,
                                    widget=forms.NumberInput(attrs={'placeholder': '联系人编号'}),
                                    error_messages={'required': '消息编号不能为空！'}
                                    )
