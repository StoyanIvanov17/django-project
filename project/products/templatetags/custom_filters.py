from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return []
    return dictionary.get(key, [])


@register.filter
def split(value, delimiter=','):
    if not value:
        return []
    return value.split(delimiter)


@register.filter
def trim(value):
    if isinstance(value, str):
        return value.strip()
    return value
