"""
A small static resume generator
"""

from static_resume import base_processors

__name__ = 'static_resume'
__version__ = '0.1'
__author__ = 'Pierre Beaujean'
__maintainer__ = 'Pierre Beaujean'
__email__ = 'pierreb24@gmail.com'
__status__ = 'Development'


CONFIG_FILE = 'conf.py'

DEFAULT_CONFIG = {
    'OUTPUT_DIR': 'output/',
    'OUTPUT_FILE': 'index.html',

    'INTERNAL_PROCESSORS': {}
}

BASE_TEMPLATE = """
{% block doc -%}
<!DOCTYPE html>
<html{% block html_attribs %}{% endblock html_attribs %}>
{%- block html %}
  <head>
    {%- block head %}
    <title>{% block title %}{% if owner %}{{ owner }}{% else %}Default template{% endif %}{% endblock title %}</title>

    {%- block metas %}
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {%- endblock metas %}

    {%- block styles %}
    {%- endblock styles %}
    {%- endblock head %}
  </head>
  <body{% block body_attribs %}{% endblock body_attribs %}>
    {% block body -%}
    {% block navbar %}
    {%- endblock navbar %}
    {% block content -%}
    {%- endblock content %}
    {% block footer %}
    {%- endblock footer %}

    {% block scripts %}
    {%- endblock scripts %}
    {%- endblock body %}
  </body>
{%- endblock html %}
</html>
{% endblock doc -%}
"""
