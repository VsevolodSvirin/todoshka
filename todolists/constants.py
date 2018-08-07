from django.utils.translation import gettext_lazy as _

# Email constants
ASSIGNED_TO_SUBJECT = _('Assigned to {assignee}')
ASSIGNED_TO_BODY = _('Behold! {author} needs you to do {task}.')

DEADLINE_CHANGED_SUBJECT = _('Deadline for {task}')
DEADLINE_CHANGED_BODY = \
    _('I hope you\'ve had your coffee already! The deadline for task {task} is changed to {deadline}!')

DEADLINE_NOTIFICATION_SUBJECT = _('Notification about {task} deadline')
DEADLINE_NOTIFICATION_BODY = _('Hurry up! The deadline of task {task} is in 1 hour!')
