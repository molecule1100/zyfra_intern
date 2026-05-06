from django import template

register = template.Library()


@register.filter
def in_group(user, group_names):
    if user.is_superuser:
        return True
    names = [n.strip() for n in group_names.split(',')]
    return user.groups.filter(name__in=names).exists()
