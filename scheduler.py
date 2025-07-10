from datetime import datetime, timedelta
from utils import parse_time_slot, time_to_str, next_day
import random
import collections

def generate_schedule(tasks, config):
    start_date = datetime.strptime(config['start_date'], "%Y-%m-%d").date()
    end_date = datetime.strptime(config['end_date'], "%Y-%m-%d").date()
    slots = config['time_slots']
    weekend_off = config.get('weekend_off', True)
    rest_minutes = config.get('rest_minutes', 10)

    # 展平任务并打乱
    task_instances = []
    for task in tasks:
        for _ in range(task['repeat']):
            task_instances.append(task.copy())
    random.shuffle(task_instances)

    # 生成每日 slot 块
    daily_blocks = collections.OrderedDict()
    current_date = start_date
    while current_date <= end_date:
        if weekend_off and current_date.weekday() >= 5:
            current_date = next_day(current_date)
            continue

        date_str = current_date.strftime("%Y-%m-%d")
        blocks = []
        for slot in slots:
            slot_start, slot_end = parse_time_slot(slot)
            start = datetime.combine(current_date, slot_start)
            end = datetime.combine(current_date, slot_end)
            blocks.append((start, end))
        daily_blocks[date_str] = blocks
        current_date = next_day(current_date)

    # 初始化每个日期的负载记录
    plan = {date: [] for date in daily_blocks}
    load = {date: 0 for date in daily_blocks}

    # 平均调度：将任务分配到当前负载最少的日期中
    for task in task_instances:
        duration = task['duration']
        best_day = min(load, key=load.get)
        assigned = False

        for slot_start, slot_end in daily_blocks[best_day]:
            current_time = slot_start
            while current_time + timedelta(minutes=duration) <= slot_end:
                conflict = any(
                    existing['time'].split('-')[0] == time_to_str(current_time)
                    for existing in plan[best_day]
                )
                if not conflict:
                    plan[best_day].append({
                        "time": f"{time_to_str(current_time)}-{time_to_str(current_time + timedelta(minutes=duration))}",
                        "subject": task['subject'],
                        "title": task['title']
                    })
                    load[best_day] += duration
                    assigned = True
                    break
                current_time += timedelta(minutes=rest_minutes)
            if assigned:
                break
        if not assigned:
            print(f"⚠️ 无法安排任务: {task['title']} {duration}min")

    return plan