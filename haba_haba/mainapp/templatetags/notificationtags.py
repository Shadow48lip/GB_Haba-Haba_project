from django import template
from mainapp.models import UserComplaints

register = template.Library()


@register.simple_tag(name='get_new_complaint_count')
def get_new_complaint_count():
    return UserComplaints.get_new_complaints()
