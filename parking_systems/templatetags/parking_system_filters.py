from django import template

register = template.Library()


@register.filter()
def timedelta_filter(timedeltaobj):
    secs = timedeltaobj.total_seconds()
    timetot = ""
    if secs >= 86400:
        days = secs // 86400
        timetot += "{} д.".format(int(days))
        secs = secs - days*86400

    if secs >= 3600:
        hrs = secs // 3600
        timetot += " {} ч.".format(int(hrs))
        secs = secs - hrs*3600

    if secs >= 60:
        mins = secs // 60
        timetot += " {} мин.".format(int(mins))

    return timetot
