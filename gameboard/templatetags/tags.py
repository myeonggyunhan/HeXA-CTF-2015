from django import template

register = template.Library()

@register.simple_tag
def active(request, view_name):
    if not request:
        return ""

    if request.path[1:] == view_name:
    	return "active"

    return ""
