# templatetags/custom_filters.py
import os
from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='image_exists')
def image_exists(image_name):
    if not image_name:
        return False
    image_path = os.path.join(settings.BASE_DIR, 'rentacar', 'static', 'images', image_name)
    return os.path.isfile(image_path)
