from datetime import datetime, timedelta

def parse_time_slot(slot_str):
    """
    将时间段字符串如 "08:30-11:00" 转换为 (start_time, end_time) 的 time 对象
    """
    start_s, end_s = slot_str.split('-')
    start = datetime.strptime(start_s, "%H:%M").time()
    end = datetime.strptime(end_s, "%H:%M").time()
    return start, end

def time_to_str(dt):
    return dt.strftime("%H:%M")

def next_day(date_obj):
    return date_obj + timedelta(days=1)

def is_weekend(date_obj):
    return date_obj.weekday() >= 5