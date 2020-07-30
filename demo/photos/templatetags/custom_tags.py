from django import template
from django.template.loader import get_template
from django.utils.html import escape

register = template.Library()

@register.simple_tag()
def verbatim_include(name):
    """
    Example: {% verbatim_include "weblog/post.html" %}
    """
    template = get_template(name)
    return escape(template.render())


@register.simple_tag()
def verbatim_include_py(name):
    """
    Renders the contents of a python file to html-compatible text
    Example: {% verbatim_include_py "demo/urls.py" %}
    """
    template = ''
    with open(name, 'r') as f:
        for line in f:
            template += line

    return escape(template)