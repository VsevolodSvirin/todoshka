import datetime

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.utils import timezone
from pytz import UTC

from todolists.serializers import TodoListSerializer
from todolists.tasks import email_notify
from todoshka.celery import app as celery_app

User = get_user_model()


class SendNotificationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='Cool Guy',
                                        email='cool_guy@smedialink.com',
                                        password='123')
        self.user_2 = User.objects.create(username='Another Cool Guy',
                                          email='another_cool_guy@smedialink.com',
                                          password='123')

        todo_attrs = {
            'name': 'This is a List',
            'author': self.user,
            'assignee': self.user_2,
            'deadline': timezone.now() + datetime.timedelta(hours=1, minutes=1)
        }

        celery_app.conf.task_always_eager = True

        self.todo = TodoListSerializer().create(validated_data=todo_attrs)

    def tearDown(self):
        self.user.delete()
        self.user_2.delete()
        self.todo.delete()

        celery_app.conf.task_always_eager = False

    def test_task_assigned_notification(self):
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Assigned to This is a List')
        self.assertEqual(mail.outbox[0].from_email, 'its@me.mario')
        self.assertEqual(mail.outbox[0].to, ['another_cool_guy@smedialink.com'])
        self.assertEqual(mail.outbox[0].body, 'Behold! Cool Guy needs you to do This is a List.')

    def test_deadline_changed_notification(self):
        old_outbox = len(mail.outbox)

        self.todo = TodoListSerializer().update(
            self.todo,
            validated_data={'deadline': datetime.datetime(2020, 1, 1, 1, 1, 1, 1, tzinfo=UTC)})

        self.assertEqual(len(mail.outbox), old_outbox + 1)
        self.assertEqual(mail.outbox[-1].subject, 'Deadline for This is a List')
        self.assertEqual(mail.outbox[-1].from_email, 'its@me.mario')
        self.assertEqual(mail.outbox[-1].to, ['another_cool_guy@smedialink.com'])
        self.assertEqual(mail.outbox[-1].body,
                         'I hope you\'ve had your coffee already! '
                         'The deadline for task This is a List is changed to {}!'.format(self.todo.deadline))

    def test_notification(self):
        mail.outbox.clear()

        email_notify.delay()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Notification about This is a List deadline')
        self.assertEqual(mail.outbox[0].from_email, 'its@me.mario')
        self.assertEqual(mail.outbox[0].to, ['cool_guy@smedialink.com', 'another_cool_guy@smedialink.com'])
        self.assertEqual(mail.outbox[0].body, 'Hurry up! The deadline of task This is a List is in 1 hour!')
