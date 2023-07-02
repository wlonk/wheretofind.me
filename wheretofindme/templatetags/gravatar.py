from hashlib import md5

from django import template

register = template.Library()


@register.simple_tag()
def gravatar(user):
    user_hash = md5(user.email.lower().encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{user_hash}"
