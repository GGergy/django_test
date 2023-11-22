from django import template


register = template.Library()


@register.filter(name="glow")
def glowing(value):
    try:
        if isinstance(value, str):
            if value.isdigit():
                value = float(value)
            else:
                return ""
        value = str(round(value))
        return {
            "1": "border-danger",
            "2": "border-danger",
            "3": "border-warning",
            "4": "border-primary",
            "5": "border-success",
        }.get(value, "")
    except Exception:
        return ""


__all__ = []
