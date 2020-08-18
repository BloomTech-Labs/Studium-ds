import pandas as pd
import datetime
from datetime import timedelta

pd.set_option('mode.chained_assignment', None)


def get_session_length(row):
    """ Calculate length of session in seconds"""
    time_delta = row['session_end'] - row['session_start']
    session_length = time_delta.total_seconds()
    return session_length


def get_cards_per_min(row):
    """Calculate cards viewed per minute"""
    row['session_length'] = get_session_length(row)
    cards_per_min = (row['total_looked_at'] / row['session_length']) * 60
    return cards_per_min


def convert_to_datetime(df):
    """Convert milliseconds since epoch timestamp to pandas datetime object"""
    df['session_start'] = pd.to_datetime(df['session_start'], unit='s')
    df['session_end'] = pd.to_datetime(df['session_end'], unit='s')
    return df


def daily_cards_min_comparison(df):
    """Function to compare today's avg cards per minute to yesterday's. Returns a dictionary of daily cards per minute,
    percentage difference, unicode for the up/down/equal sign, and a color code"""
    df = convert_to_datetime(df)
    today = datetime.date.today()
    yesterday = today - timedelta(days=1)
    todays_per_min = []
    yesterday_per_min = []
    # this iterates over each row in the dataframe, applying the logic and adding the cards_per_min value to the
    # appropriate list
    for index, row in df.iterrows():
        if row['session_start'].date() == today:
            per_min = get_cards_per_min(row)
            todays_per_min.append(per_min)
        if row['session_start'].date() == yesterday:
            per_min = get_cards_per_min(row)
            yesterday_per_min.append(per_min)
    today_average = 0
    yesterday_average = 0
    if len(todays_per_min) > 0 and len(yesterday_per_min) > 0:
        # if both days have data, then calculate the average of the list
        today_average = sum(todays_per_min) / len(todays_per_min)
        yesterday_average = sum(yesterday_per_min) / len(yesterday_per_min)
    elif len(todays_per_min) == 0:
        # if no cards viewed today, cards per min average is 0
        today_average = 0
    elif len(yesterday_per_min) == 0:
        yesterday_average = 0
    try:
        difference = abs((today_average - yesterday_average) / yesterday_average) * 100
    except ZeroDivisionError:
        # if no cards viewed yesterday, cards per min up 100% today
        # if both averages are zero, this will display '0 100% =' in black
        difference = 100
    if today_average > yesterday_average:
        color_code = "09B109"
        # hex color code for green
        arrow = "\u2191"
        # unicode for upward arrow
    elif today_average < yesterday_average:
        color_code = "CE2929"
        # hex color code for red
        arrow = "\u2193"
        # unicode for downward arrow
    else:
        color_code = "000000"
        # hex color code for black
        arrow = "\u003D"
        # unicode for equal sign
    result = make_results_dict(today_average, difference, color_code, arrow)
    result['daily_cards_min'] = result.pop('metric')
    return result


def weekly_per_min_comparison(df):
    """Function to compare this week's avg cards per minute to last week's. Returns a dictionary of weekly cards per
    minute, percentage difference, unicode for the up/down/equal sign, and a color code """
    df = convert_to_datetime(df)
    today = datetime.date.today()
    this_week_start = today - timedelta(days=7)
    last_week_start = today - timedelta(days=14)
    week_per_min = []
    lastweek_per_min = []
    for index, row in df.iterrows():
        if row['session_start'].date() >= this_week_start:
            per_min = get_cards_per_min(row)
            week_per_min.append(per_min)
        if last_week_start <= row['session_start'].date() < this_week_start:
            per_min = get_cards_per_min(row)
            lastweek_per_min.append(per_min)
    week_average = 0
    lastweek_average = 0
    if len(week_per_min) > 0 and len(lastweek_per_min) > 0:
        week_average = sum(week_per_min) / len(week_per_min)
        lastweek_average = sum(lastweek_per_min) / len(lastweek_per_min)
    elif len(week_per_min) == 0:
        week_average = 0
    elif len(lastweek_per_min) == 0:
        lastweek_average = 0
    if week_average > lastweek_average:
        color_code = "09B109"
        arrow = "\u2191"
    elif week_average < lastweek_average:
        color_code = "CE2929"
        arrow = "\u2193"
    else:
        color_code = "000000"
        arrow = "\u003D"
    try:
        difference = abs((week_average - lastweek_average) / lastweek_average) * 100
    except ZeroDivisionError:
        difference = 100
        # if no sessions last week, difference is up 100%
        # if both averages are zero, this will display '0 100% =' in black
    result = make_results_dict(week_average, difference, color_code, arrow)
    result['weekly_cards_min'] = result.pop('metric')
    return result


def monthly_per_min_comparison(df):
    """Function to compare today's stats to yesterday's. Returns a dictionary of monthly cards per minute,
    percentage difference, unicode for the up/down/equal sign, and a color code"""
    df = convert_to_datetime(df)
    today = datetime.date.today()
    this_month_start = today - timedelta(days=30)
    last_month_start = today - timedelta(days=60)
    month_per_min = []
    lastmonth_per_min = []
    for index, row in df.iterrows():
        if row['session_start'].date() >= this_month_start:
            per_min = get_cards_per_min(row)
            month_per_min.append(per_min)
        if last_month_start <= row['session_start'].date() < this_month_start:
            per_min = get_cards_per_min(row)
            lastmonth_per_min.append(per_min)
    month_average = 0
    lastmonth_average = 0
    if len(month_per_min) > 0 and len(lastmonth_per_min) > 0:
        month_average = sum(month_per_min) / len(month_per_min)
        lastmonth_average = sum(lastmonth_per_min) / len(lastmonth_per_min)
    elif len(month_per_min) == 0:
        month_average = 0
    elif len(lastmonth_per_min) == 0:
        lastmonth_average = 0
    if month_average > lastmonth_average:
        color_code = "09B109"
        arrow = "\u2191"
    elif month_average < lastmonth_average:
        color_code = "CE2929"
        arrow = "\u2193"
    else:
        color_code = "000000"
        arrow = "\u003D"
    try:
        difference = abs((month_average - lastmonth_average) / lastmonth_average) * 100
    except ZeroDivisionError:
        difference = 100
        # if no sessions last month, difference is up 100%
        # if both averages are zero, this will display '0 100% =' in black
    result = make_results_dict(month_average, difference, color_code, arrow)
    result['monthly_cards_min'] = result.pop('metric')
    return result


def best_session_length(df):
    """Takes in dataframe of user session data and returns best session length in minutes (best session being session
    with highest cards per minute """
    if len(df) == 0:
        best_length = 0
        # if no data in dataframe, return 0
    else:
        df = convert_to_datetime(df)
        df = df.reindex(columns=df.columns.tolist() + ['cards_per_min', 'session_length'])
        # adds necessary columns to dataframe
        for index, row in df.iterrows():
            df['session_length'].loc[index] = get_session_length(row)
            df['cards_per_min'].loc[index] = get_cards_per_min(row)
        df = df.sort_values(by=['cards_per_min'], ascending=False)
        # sorts dataframe and puts highest cards per minute at the top
        best_length = (df['session_length'].iloc[0] / 60)
        # converts session length in seconds to minutes
    return best_length


def best_session_daily(df):
    """Function to determine the best session length in minutes for today and yesterday. Takes in a
    user session dataframe and returns a dictionary of daily best session,
    percentage difference, unicode for the up/down/equal sign, and a color code"""
    df = convert_to_datetime(df)
    today = datetime.date.today()
    yesterday = today - timedelta(days=1)
    today_card_ids = []
    yesterday_card_ids = []
    for index, row in df.iterrows():
        try:
            if row['session_start'].date() == today:
                today_card_ids.append(row['id'])
            elif row['session_start'].date() == yesterday:
                yesterday_card_ids.append(row['id'])
        except IndexError:
            today_card_ids = []
            yesterday_card_ids = []
    today = df[df['id'].isin(today_card_ids)]
    yesterday = df[df['id'].isin(yesterday_card_ids)]
    today_best_session = best_session_length(today)
    yesterday_best_session = best_session_length(yesterday)
    if today_best_session > yesterday_best_session:
        color_code = "09B109"
        arrow = "\u2191"
    elif today_best_session < yesterday_best_session:
        color_code = "CE2929"
        arrow = "\u2193"
    else:
        color_code = "000000"
        arrow = "\u003D"
    try:
        difference = abs((today_best_session - yesterday_best_session) / yesterday_best_session) * 100
    except ZeroDivisionError:
        # if no sessions yesterday, best session is up 100%
        # if both best_sessions are zero, this will display '0 100% =' in black
        difference = 100
    result = make_results_dict(today_best_session, difference, color_code, arrow)
    result['best_session_daily'] = result.pop('metric')
    return result


def best_session_weekly(df):
    """Function to determine the best session length in minutes for this week and last week. Takes in a
    user session dataframe and returns a dictionary of weekly best session,
    percentage difference, unicode for the up/down/equal sign, and a color code"""
    df = convert_to_datetime(df)
    today = datetime.date.today()
    this_week_start = today - timedelta(days=7)
    last_week_start = today - timedelta(days=14)
    this_week_card_ids = []
    lastweek_card_ids = []
    for index, row in df.iterrows():
        try:
            if row['session_start'].date() >= this_week_start:
                this_week_card_ids.append(row[id])
            elif last_week_start <= row['session_start'].date() < this_week_start:
                lastweek_card_ids.append(row[id])
        except IndexError:
            this_week_card_ids = []
            lastweek_card_ids = []
    thisweek = df[df['id'].isin(this_week_card_ids)]
    lastweek = df[df['id'].isin(lastweek_card_ids)]
    thisweek_best_session = best_session_length(thisweek)
    lastweek_best_session = best_session_length(lastweek)
    if thisweek_best_session > lastweek_best_session:
        color_code = "09B109"
        arrow = "\u2191"
    elif thisweek_best_session < lastweek_best_session:
        color_code = "CE2929"
        arrow = "\u2193"
    else:
        color_code = "000000"
        arrow = "\u003D"
    try:
        difference = abs((thisweek_best_session - lastweek_best_session) / lastweek_best_session) * 100
    except ZeroDivisionError:
        # if no sessions last week, best session is up 100%
        # if both best_sessions are zero, this will display '0 100% =' in black
        difference = 100
    result = make_results_dict(thisweek_best_session, difference, color_code, arrow)
    result['best_session_weekly'] = result.pop('metric')
    return result


def best_session_monthly(df):
    """Function to determine the best session length in minutes for this month and last month. Takes in a
    user session dataframe and returns a dictionary of monthly best session,
    percentage difference, unicode for the up/down/equal sign, and a color code"""
    df = convert_to_datetime(df)
    today = datetime.date.today()
    this_month_start = today - timedelta(days=30)
    last_month_start = today - timedelta(days=60)
    this_month_card_ids = []
    lastmonth_card_ids = []
    for index, row in df.iterrows():
        try:
            if row['session_start'].date() >= this_month_start:
                this_month_card_ids.append(row[id])
            elif last_month_start <= row['session_start'].date() < this_month_start:
                lastmonth_card_ids.append(row[id])
        except IndexError:
            this_month_card_ids = []
            lastmonth_card_ids = []
    thismonth = df[df['id'].isin(this_month_card_ids)]
    lastmonth = df[df['id'].isin(lastmonth_card_ids)]
    thismonth_best_session = best_session_length(thismonth)
    lastmonth_best_session = best_session_length(lastmonth)
    if thismonth_best_session > lastmonth_best_session:
        color_code = "09B109"
        arrow = "\u2191"
    elif thismonth_best_session < lastmonth_best_session:
        color_code = "CE2929"
        arrow = "\u2193"
    else:
        color_code = "000000"
        arrow = "\u003D"
    try:
        difference = abs((thismonth_best_session - lastmonth_best_session) / lastmonth_best_session) * 100
    except ZeroDivisionError:
        # if last month has no sessions, the difference is up 100%
        # if both best_sessions are zero, this will display '0 100% =' in black
        difference = 100
    result = make_results_dict(thismonth_best_session, difference, color_code, arrow)
    result['best_session_monthly'] = result.pop('metric')
    return result


def make_results_dict(metric, difference, color, unicode):
    results_dict = {'metric': metric, 'difference': difference, 'color_code': color, 'unicode': unicode}
    return results_dict
