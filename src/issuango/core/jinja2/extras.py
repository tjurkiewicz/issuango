import django.utils.timezone


def strftime(fmt, date=None):
    if not date:
        date = django.utils.timezone.now()
    return date.strftime(fmt.encode('utf-8')).decode('utf-8')


def field_type(field):
    return field.field.widget.__class__.__name__
