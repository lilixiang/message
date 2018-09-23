# -*- encoding:utf8 -*-
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from message import services
from message.forms.user_forms import SendMessageForm, DeleteContactForm, DeleteMessageForm, InboxSendMessageForm
from .forms import RegisterForm, LoginForm
from .models import User, Contact, Message, Inbox

__author__ = 'luke'


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user_contact_list'))
    if request.method == 'POST':
        form = LoginForm(request.POST.copy())
        content = {'form': form, 'title': '登录', }
        if not form.is_valid():
            return render(request, 'login.html', {'content': content})

        form = form.auth_user()
        if form.errors:
            content['form'] = form
            return render(request, 'login.html', {'content': content}, )

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        request.session['username'] = username
        return HttpResponseRedirect(reverse('user_contact_list'))

    elif request.method == 'GET':
        form = LoginForm()
        content = {'form': form, 'title': '登录', }
        return render(request, 'login.html', {'content': content})


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
        content = {'form': form}
        return render(request, 'register.html', {'content': content})

    if request.method == 'POST':
        content = {}

        form = RegisterForm(request.POST.copy())
        content['form'] = form

        if not form.is_valid():
            return render(request, 'register.html', {'content': content})

        form = form.auth_user()
        form = form.auth_email()
        if form.errors:
            return render(request, 'register.html', {'content': content}, )

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        password_confirm = form.cleaned_data.get('password_confirm')
        if password != password_confirm:
            form.errors["password"] = form.error_class(['两次密码不一致！'])
            return render(request, 'register.html', {'content': content}, )

        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username=username,
                                        password=password,
                                        email=email
                                        )
        user.save()
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)

        return HttpResponseRedirect(reverse('user_contact_list'))


@login_required()
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


@login_required()
def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('user_contact_list'))
    else:
        return HttpResponseRedirect(reverse('login'))


@login_required()
def user_contact_list(request):
    user = request.user
    contacts = Contact.objects.filter(user_id=user.id, is_del=Contact.DelType.no).all()

    content = {'contacts': contacts}
    return render(request, 'contact.html', {'content': content})


@login_required()
def user_inbox(request, contact_id):
    user = request.user
    inbox = Inbox.objects.filter(sender_id=user.id, receiver_id=contact_id).first()

    if inbox:
        messages = Message.objects.filter(inbox_id=inbox.id, is_del=Message.DelType.no).all()
        contact = Contact.objects.filter(user_id=user.id, contact_id=contact_id).first()
        unread_cnt = contact.unread_cnt

        if unread_cnt > 0:
            contact.unread_cnt -= unread_cnt
            contact.save()

    else:
        messages = []

    form = InboxSendMessageForm()

    content = {'messages': messages, 'form': form, 'contact_id': contact_id, 'user': user}
    return render(request, 'inbox.html', {'content': content})


@login_required()
@transaction.atomic
def send_message(request):
    user = request.user

    if request.method == 'GET':
        form = SendMessageForm()
        content = {'form': form}
        return render(request, 'send_message.html', {'content': content})

    if request.method == 'POST':
        form = SendMessageForm(request.POST.copy())
        content = {'form': form}
        if form.is_valid():
            if form.errors:
                content['form'] = form
                return render(request, 'send_message.html', {'content': content}, )
            receiver_id = form.cleaned_data.get('receiver_id')

            if receiver_id == user.id:
                form.errors["receiver_id"] = form.error_class(['不能给自己发送消息'])
                return render(request, 'send_message.html', {'content': content}, )
            try:
                receiver = User.objects.get(pk=receiver_id)

            except User.DoesNotExist:
                form.errors["receiver_id"] = form.error_class(['用户不存在'])
                return render(request, 'send_message.html', {'content': content}, )

            receiver_id = form.cleaned_data.get('receiver_id')
            msg = form.cleaned_data.get('content')

            sender_inbox = services.get_or_create_inbox(user.id, receiver_id)
            send_msg = Message(sender_id=user.id, receiver_id=receiver_id,
                               inbox_id=sender_inbox.id, content=msg)

            send_msg.save()
            receiver_inbox = services.get_or_create_inbox(receiver_id, user.id)
            receiver_msg = Message(sender_id=user.id, receiver_id=receiver_id,
                                   inbox_id=receiver_inbox.id,
                                   content=msg)
            receiver_msg.save()

            sender_contact = services.get_or_create_contact(user.id, receiver_id)
            sender_contact.unread_cnt += 1
            sender_contact.is_del = Contact.DelType.no

            receiver_contact = services.get_or_create_contact(receiver_id, user.id)
            receiver_contact.unread_cnt += 1
            receiver_contact.is_del = Contact.DelType.no

            sender_contact.save()
            receiver_contact.save()

            messages = Message.objects.filter(inbox_id=sender_inbox.id, is_del=Message.DelType.no).all()

            content['messages'] = messages
            content['form'] = SendMessageForm()

            return redirect('/inbox/{}/'.format(receiver_id))


@login_required()
@transaction.atomic
def delete_message(request):
    user = request.user

    if request.method == 'POST':
        form = DeleteMessageForm(request.POST.copy())
        content = {'form': form}
        if form.is_valid():
            if form.errors:
                content['form'] = form
                return render(request, 'login.html', {'content': content}, )
            else:
                message_id = form.cleaned_data.get('message_id')

                message = Message.objects.get(pk=message_id)

                if message.sender_id == user.id:
                    message.is_del = Contact.DelType.yes

                    message.save()

                return JsonResponse({'status': True})


@login_required()
@transaction.atomic
@csrf_exempt
def delete_contact(request):
    user = request.user

    if request.method == 'POST':
        form = DeleteContactForm(request.POST.copy())
        content = {'form': form}
        if form.is_valid():
            if form.errors:
                content['form'] = form
                return render(request, 'login.html', {'content': content}, )
            else:
                contact_id = form.cleaned_data.get('contact_id')

                contact = Contact.objects.filter(
                    user_id=user.id, contact_id=contact_id, is_del=Contact.DelType.no).first()

                contact.unread_cnt = 0
                contact.is_del = Contact.DelType.yes

                contact.save()

                return JsonResponse({'status': True})
