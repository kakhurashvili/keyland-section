from django import template
from storeapp.models import SiteConfiguration

register = template.Library()

@register.simple_tag
def get_site_config():
    return SiteConfiguration.objects.first()
