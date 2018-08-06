from datetime import timedelta

from celery.utils.log import get_task_logger
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone

from todoshka.celery import app

logger = get_task_logger(__name__)
User = get_user_model()


def send_assignment_email(task):
    recipient_list = []
    if task.assignee:
        recipient_list.append(task.assignee.email)

        send_mail(
            subject='Assigned to {}'.format(task.name),
            from_email='its@me.mario',
            recipient_list=recipient_list,
            fail_silently=False,
            message='Behold! {} needs you to do {}.'.format(task.author, task.name)
        )


def send_deadline_changed_email(task):
    recipient_list = []
    if task.assignee:
        recipient_list.append(task.assignee.email)

        send_mail(
            subject='Deadline for {}'.format(task.name),
            from_email='its@me.mario',
            recipient_list=recipient_list,
            fail_silently=False,
            message='I hope you\'ve had your coffee already! '
                    'The deadline for task {} is changed to {}!'.format(task.name, task.deadline)
        )


def send_notification_email(task):
    recipient_list = [task.author.email]
    if task.assignee:
        recipient_list.append(task.assignee.email)

    send_mail(
        subject='Notification about {} deadline'.format(task.name),
        from_email='its@me.mario',
        recipient_list=recipient_list,
        fail_silently=False,
        message='Hurry up! The deadline of task {} is in 1 hour!'.format(task.name)
    )


@app.task()
def email_task_assigned(task):
    try:
        send_assignment_email(task)
    except Exception as exc:
        logger.error('Task Assignment Email Sending: {}'.format(exc))


@app.task()
def email_deadline_changed(task):
    try:
        send_deadline_changed_email(task)
    except Exception as exc:
        logger.error('Deadline Changed Email Sending: {}'.format(exc))


@app.task()
def email_notify(*args):
    from todolists.models import TodoList

    deadline_early = timezone.now() + timedelta(hours=1)
    deadline_late = deadline_early + timedelta(minutes=1)

    upcoming_tasks = TodoList.objects.filter(deadline__range=[deadline_early, deadline_late])
    for task in upcoming_tasks:
        try:
            send_notification_email(task)
        except Exception as exc:
            logger.error('Periodic Email Sending: {}'.format(exc))
