import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QTextEdit, QLabel
)
from scheduler import generate_schedule
from ui_editor import TaskEditor
from export_md import export_schedule_to_md
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class SchedulePlanner(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('任务计划安排器')
        self.resize(600, 600)

        layout = QVBoxLayout()

        self.load_btn = QPushButton('加载 tasks.json')
        self.load_btn.clicked.connect(self.load_tasks)
        layout.addWidget(self.load_btn)

        self.edit_btn = QPushButton('编辑任务列表')
        self.edit_btn.clicked.connect(self.open_editor)
        layout.addWidget(self.edit_btn)

        self.run_btn = QPushButton('生成计划')
        self.run_btn.clicked.connect(self.run_schedule)
        layout.addWidget(self.run_btn)

        self.output = QTextEdit()
        layout.addWidget(self.output)

        self.setLayout(layout)

        self.export_btn = QPushButton('导出为 Markdown')
        self.export_btn.clicked.connect(self.export_md)
        layout.addWidget(self.export_btn)

        self.table_preview = QTableWidget()
        layout.addWidget(self.table_preview)

    def load_tasks(self):
        path, _ = QFileDialog.getOpenFileName(self, '打开任务配置', '', 'JSON Files (*.json)')
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.output.setPlainText(f'已加载: {path}\n')

    def run_schedule(self):
        if not hasattr(self, 'data'):
            self.output.append('请先加载 tasks.json')
            return
        tasks = self.data['tasks']
        config = self.data['config']
        result = generate_schedule(tasks, config)
        text = json.dumps(result, ensure_ascii=False, indent=2)
        self.output.append(text)

        # 表格预览
        self.table_preview.clear()
        sorted_days = sorted(result.items())
        self.table_preview.setColumnCount(3)
        self.table_preview.setHorizontalHeaderLabels(["时间", "科目", "标题"])

        flat_tasks = []
        for d, lst in sorted_days:
            flat_tasks.append((d, "", "", ""))  # 日期作为一行
            for t in lst:
                flat_tasks.append(("", t['time'], t['subject'], t['title']))

        self.table_preview.setRowCount(len(flat_tasks))
        for row, (date, time, subject, title) in enumerate(flat_tasks):
            self.table_preview.setItem(row, 0, QTableWidgetItem(date or time))
            self.table_preview.setItem(row, 1, QTableWidgetItem(subject))
            self.table_preview.setItem(row, 2, QTableWidgetItem(title))

    def open_editor(self):
        self.editor = TaskEditor()
        self.editor.show()


    def export_md(self):
        if not hasattr(self, 'data'):
            self.output.append('请先加载 tasks.json')
            return
        from scheduler import generate_schedule
        tasks = self.data['tasks']
        config = self.data['config']
        schedule = generate_schedule(tasks, config)
        path, _ = QFileDialog.getSaveFileName(self, '导出 Markdown 文件', 'schedule.md', 'Markdown 文件 (*.md)')
        if path:
            export_schedule_to_md(schedule, path)
            self.output.append(f'Markdown 导出完成: {path}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    planner = SchedulePlanner()
    planner.show()
    sys.exit(app.exec_())