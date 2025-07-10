import json

def export_schedule_to_md(schedule: dict, path: str):
    """将任务安排导出为 Markdown 文件"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write("# 学习任务计划表\n\n")
        for date, items in sorted(schedule.items()):
            f.write(f"## {date}\n\n")
            for task in items:
                time = task['time']
                subject = task['subject']
                title = task['title']
                f.write(f"- **{time}** | {subject}：{title}\n")
            f.write("\n")