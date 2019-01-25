from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def nickname(context, user):
    requesting_user = context["user"]
    return user.nickname_for(requesting_user)
