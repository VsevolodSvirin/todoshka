from datetime import timedelta

from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from tasks import constants
from tasks.models import Task
from todoshka.celery import app
from todoshka import settings

logger = get_task_logger(__name__)
User = get_user_model()


def send_assignment_email(task):
    recipient_list = []
    if task.assignee:
        recipient_list.append(task.assignee.email)

        send_mail(
            subject=constants.ASSIGNED_TO_SUBJECT.format(assignee=task.name),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
            message=constants.ASSIGNED_TO_BODY.format(author=task.author, task=task.name)
        )


def send_deadline_changed_email(task):
    recipient_list = []
    if task.assignee:
        recipient_list.append(task.assignee.email)

        send_mail(
            subject=constants.DEADLINE_CHANGED_SUBJECT.format(task=task.name),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
            message=constants.DEADLINE_CHANGED_BODY.format(task=task.name, deadline=task.deadline)
        )


def send_notification_email(task):
    recipient_list = [task.author.email]
    if task.assignee:
        recipient_list.append(task.assignee.email)

    send_mail(
        subject=constants.DEADLINE_NOTIFICATION_SUBJECT.format(task=task.name),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
        message=constants.DEADLINE_NOTIFICATION_BODY.format(task=task.name)
    )


@app.task()
def email_task_assigned(task_id):
    try:
        task = Task.objects.get(pk=task_id)
        send_assignment_email(task)
    except Exception as exc:
        logger.error('Task Assignment Email Sending: {}'.format(exc))


@app.task()
def email_deadline_changed(task_id):
    try:
        task = Task.objects.get(pk=task_id)
        send_deadline_changed_email(task)
    except Exception as exc:
        logger.error('Deadline Changed Email Sending: {}'.format(exc))


@app.task()
def email_notify(*args):
    deadline_early = timezone.now() + timedelta(hours=1)
    deadline_late = deadline_early + timedelta(minutes=1)

    upcoming_tasks = Task.objects.filter(deadline__range=[deadline_early, deadline_late])
    for task in upcoming_tasks:
        try:
            send_notification_email(task)
        except Exception as exc:
            logger.error('Periodic Email Sending: {}'.format(exc))
