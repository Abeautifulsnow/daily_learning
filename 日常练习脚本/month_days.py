"""
计算每个月天数
"""

import calendar

this_year = int(input("Enter year: "))
this_month = int(input("Enter month: "))
monthRange = calendar.monthrange(this_year, this_month)
print(monthRange)
