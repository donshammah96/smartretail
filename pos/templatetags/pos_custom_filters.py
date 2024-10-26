from django import template

register = template.Library()

@register.filter
def get_attr(obj, attr):
    """
    Custom template filter to get an attribute of an object.
    """
    return getattr(obj, attr, None)

@register.filter
def get_field_value(obj, field_name):
    """
    Custom template filter to get the value of a field of an object.
    """
    return getattr(obj, field_name, None)

@register.filter
def add(value, arg):
    """
    Custom template filter to add a value to an argument.
    """
    return value + arg

@register.filter
def get_meta_fields(obj):
    """
    Custom template filter to return the meta fields of an object.
    """
    return [field for field in obj._meta.fields]
