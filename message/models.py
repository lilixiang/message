# -*- encoding:utf8 -*-
from enum import IntEnum

from django.contrib.auth.models import AbstractUser
from django.db import models

__author__ = 'luke'


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True, help_text='用户编号')
    email = models.EmailField(help_text='电子邮件', max_length=128, default='', null=False, db_index=True)
    password = models.CharField(help_text='密码', max_length=128, default='')
    nickname = models.CharField(help_text='昵称', max_length=50, default='')
    gender = models.PositiveSmallIntegerField(help_text='性别', default=0)

    class Meta(AbstractUser.Meta):
        db_table = 'user'


class Contact(models.Model):
    # 用户联系人表

    class DelType(IntEnum):
        no = 0
        yes = 1

    DEL_TYPE_CHOICE = (
        ('no', 0),
        ('yes', 1),
    )

    id = models.BigAutoField(primary_key=True, help_text='用户编号')
    user_id = models.BigIntegerField(help_text='用户编号')
    contact_id = models.BigIntegerField(help_text='联系人编号')

    unread_cnt = models.BigIntegerField(help_text='未读消息数', default=0)

    is_del = models.PositiveSmallIntegerField(help_text='是否删除', default=0, choices=DEL_TYPE_CHOICE)

    # todo 改用timestamp
    last_msg_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'user_contacts'


class Inbox(models.Model):
    # 用户会话表

    id = models.BigAutoField(primary_key=True, help_text='用户编号')
    sender_id = models.BigIntegerField(help_text='用户编号')
    receiver_id = models.BigIntegerField(help_text='联系人编号')

    class Meta:
        db_table = 'user_inbox'


class Message(models.Model):
    # 用户消息表
    class DelType(IntEnum):
        no = 0
        yes = 1

    DEL_TYPE_CHOICE = (
        ('no', 0),
        ('yes', 1),
    )

    id = models.BigAutoField(primary_key=True, help_text='用户编号')
    inbox_id = models.BigIntegerField(help_text='会话编号', default=0, )
    sender_id = models.BigIntegerField(help_text='发送人编号')
    receiver_id = models.BigIntegerField(help_text='接受人编号')

    content = models.CharField(help_text='消息', max_length=1024, default='')

    is_del = models.PositiveSmallIntegerField(help_text='是否删除', default=0, choices=DEL_TYPE_CHOICE)

    class Meta:
        db_table = 'user_messages'
