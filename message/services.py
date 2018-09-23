# -*- encoding:utf8 -*-
from message.models import Inbox, Contact

__author__ = 'luke'


def get_or_create_inbox(sender_id, receiver_id):
    """

    :param sender_id:
    :param receiver_id:
    :return:
    """
    inbox = Inbox.objects.filter(sender_id=sender_id, receiver_id=receiver_id).first()

    if not inbox:
        inbox = Inbox(
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        inbox.save()

    return inbox


def get_or_create_contact(sender_id, receiver_id):
    """

    :param sender_id:
    :param receiver_id:
    :return:
    """
    contact = Contact.objects.filter(user_id=sender_id, contact_id=receiver_id).first()

    if not contact:
        contact = Contact(
            user_id=sender_id,
            contact_id=receiver_id,
        )
        contact.save()

    return contact

