from django import template
from datetime import date

register = template.Library()


@register.filter(name="calculate_age")
def calculate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age
