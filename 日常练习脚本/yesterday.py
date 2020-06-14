import datetime


def get_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


# 输出
print(get_yesterday())
