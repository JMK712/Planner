import json
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QFileDialog, QLabel,
    QLineEdit, QMessageBox, QCheckBox
)

class TaskEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("任务与配置编辑器")
        self.resize(800, 600)

        self.layout = QVBoxLayout()

        # --- 任务编辑区 ---
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["科目", "标题", "耗时（分钟）", "重复次数"])
        self.layout.addWidget(QLabel("任务列表"))
        self.layout.addWidget(self.table)

        button_layout = QHBoxLayout()
        add_btn = QPushButton("添加任务")
        add_btn.clicked.connect(self.add_task)
        del_btn = QPushButton("删除所选")
        del_btn.clicked.connect(self.delete_task)
        button_layout.addWidget(add_btn)
        button_layout.addWidget(del_btn)
        self.layout.addLayout(button_layout)

        # --- 配置编辑区 ---
        self.layout.addWidget(QLabel("计划配置"))

        self.start_input = QLineEdit()
        self.end_input = QLineEdit()
        self.slots_input = QLineEdit()
        self.rest_input = QLineEdit()
        self.weekend_box = QCheckBox("双休日不安排任务")

        self.layout.addWidget(QLabel("开始日期 (YYYY-MM-DD)"))
        self.layout.addWidget(self.start_input)
        self.layout.addWidget(QLabel("结束日期 (YYYY-MM-DD)"))
        self.layout.addWidget(self.end_input)
        self.layout.addWidget(QLabel("每天时间段 (逗号分隔，如 09:00-12:00,14:00-17:00)"))
        self.layout.addWidget(self.slots_input)
        self.layout.addWidget(QLabel("任务间休息时间（分钟）"))
        self.layout.addWidget(self.rest_input)
        self.layout.addWidget(self.weekend_box)

        # 保存按钮
        save_btn = QPushButton("保存为 tasks.json")
        save_btn.clicked.connect(self.save_all)
        self.layout.addWidget(save_btn)

        self.setLayout(self.layout)

    def add_task(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col in range(4):
            self.table.setItem(row, col, QTableWidgetItem(""))

    def delete_task(self):
        for row in sorted(set(index.row() for index in self.table.selectedIndexes()), reverse=True):
            self.table.removeRow(row)

    def save_all(self):
        # 收集任务
        tasks = []
        for row in range(self.table.rowCount()):
            try:
                subject = self.table.item(row, 0).text()
                title = self.table.item(row, 1).text()
                duration = int(self.table.item(row, 2).text())
                repeat = int(self.table.item(row, 3).text())
                tasks.append({"subject": subject, "title": title, "duration": duration, "repeat": repeat})
            except Exception:
                QMessageBox.warning(self, "格式错误", f"第 {row+1} 行任务数据无效，已跳过。")

        # 收集配置
        try:
            config = {
                "start_date": self.start_input.text(),
                "end_date": self.end_input.text(),
                "time_slots": [s.strip() for s in self.slots_input.text().split(',') if s.strip()],
                "weekend_off": self.weekend_box.isChecked(),
                "rest_minutes": int(self.rest_input.text())
            }
        except Exception:
            QMessageBox.critical(self, "配置错误", "计划配置格式错误，请检查！")
            return

        # 保存为 JSON
        if tasks and config:
            path, _ = QFileDialog.getSaveFileName(self, '保存任务配置', 'tasks.json', 'JSON Files (*.json)')
            if path:
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({"tasks": tasks, "config": config}, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "保存成功", f"保存至 {path}")