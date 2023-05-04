#
# Module with helper functions for the VSTOXX index calculation
#
# (c) The Python Quants GmbH
# For illustration purposes only.
# August 2014
#

TYEAR = 365 * 24 * 60 * 60.  # seconds of a standard year

import datetime as dt


def third_friday(date):
    ''' Returns the third friday of the month given by the datetime object date
    This is the day options expiry on.

    date: datetime object
        date of month for which third Friday is to be found
    '''
    
    number_days = date.day
    first_day = date - dt.timedelta(number_days - 1)
    week_day = first_day.weekday()
    day_delta = 4 - week_day  # distance to the next Friday 
    if day_delta < 0:
        day_delta += 7
    return first_day + dt.timedelta(day_delta + 14)


def first_settlement_day(date):
    ''' Returns the next settlement date (third Friday of a month) following
    the date date.

    date: datetime object
        date for which following third Friday is to be found
    '''

    settlement_day_in_month = third_friday(date)
    delta = (settlement_day_in_month - date).days
    if delta > 1:
        return settlement_day_in_month
    next_month = settlement_day_in_month + dt.timedelta(20)
    return third_friday(next_month)


def second_settlement_day(date):
    ''' Returns the second settlement date (third Friday of a month) following
    the date date.

    date: datetime object
        date for which second third Friday is to be found
    '''

    settlement_day_in_month = first_settlement_day(date)
      # settlement date in the given month
    next_month = settlement_day_in_month + dt.timedelta(20)
      # shift date to the next month
    return third_friday(next_month)  # settlement date of that month


def not_a_day_before_expiry(date):
    ''' Returns True if the date is NOT one day before or equal the third
    Friday in month

    date: datetime object
        date for which second third Friday is to be found
    '''

    settlement_day_in_month = third_friday(date)
    delta = (settlement_day_in_month - date).days
    return delta not in [1, 0]

        
def compute_delta(date, settlement_day):
    ''' Computes the time (in seconds) from date 0:00 to the first settlement
    date 8:30 AM

    date: datetime object
        starting date
    settlement_day: datetime object
        relevant settlement day
    '''
   
    dummy_time_1 = dt.timedelta(seconds=43200)
    dummy_time_2 = dt.timedelta(seconds=23400)
    settlement_date = settlement_day + dummy_time_1 + dummy_time_2
    delta_T_dummy = settlement_date - date
    return (
        (delta_T_dummy.days - 1) * 24 * 60 * 60 + delta_T_dummy.seconds
    ) / TYEAR

                    
