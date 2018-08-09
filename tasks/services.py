from tasks.tasks import email_task_assigned, email_deadline_changed


def deliver_email_on_create(instance, validated_data):
    if 'assignee' in validated_data.keys():
        email_task_assigned.delay(instance.id)


def deliver_email_on_update(instance, validated_data):
    if 'assignee' in validated_data.keys():
        email_task_assigned.delay(instance.id)

    if 'deadline' in validated_data.keys() and instance.assignee:
        email_deadline_changed.delay(instance.id)
