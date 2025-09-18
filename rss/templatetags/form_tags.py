from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """폼 필드에 CSS 클래스를 추가하는 필터"""
    return field.as_widget(attrs={'class': css_class})