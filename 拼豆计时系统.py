import sys
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QPushButton, QLabel,
                             QDialog, QComboBox, QLineEdit, QTextEdit, QMessageBox,
                             QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('拼豆店数据.db')
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS 计时记录 (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                座位号 INTEGER,
                套餐类型 TEXT,
                开始时间 TEXT,
                结束时间 TEXT,
                使用时长 TEXT,
                顾客信息 TEXT,
                日期 TEXT
            )
        ''')
        self.conn.commit()

    def save_record(self, 座位号, 套餐类型, 开始时间, 结束时间, 使用时长, 顾客信息):
        cursor = self.conn.cursor()
        日期 = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO 计时记录 (座位号, 套餐类型, 开始时间, 结束时间, 使用时长, 顾客信息, 日期)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (座位号, 套餐类型, 开始时间, 结束时间, 使用时长, 顾客信息, 日期))
        self.conn.commit()

    def get_all_records(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM 计时记录 ORDER BY id DESC')
        return cursor.fetchall()

class SeatButton(QPushButton):
    def __init__(self, seat_number, parent=None):
        super().__init__(str(seat_number), parent)
        self.seat_number = seat_number
        self.is_occupied = False
        self.start_time = None
        self.package_type = None
        self.customer_info = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.setMinimumSize(80, 60)
        self.setStyleSheet(self.get_style('空闲'))

    def get_style(self, status):
        styles = {
            '空闲': 'background-color: #90EE90; font-size: 14px; font-weight: bold;',
            '使用中': 'background-color: #FFB6C1; font-size: 12px;',
        }
        return styles.get(status, styles['空闲'])

    def start_timing(self, package_type, customer_info):
        self.is_occupied = True
        self.package_type = package_type
        self.customer_info = customer_info
        self.start_time = datetime.now()
        self.timer.start(1000)
        self.setStyleSheet(self.get_style('使用中'))
        self.update_display()

    def update_display(self):
        if self.is_occupied and self.start_time:
            elapsed = datetime.now() - self.start_time
            hours = int(elapsed.total_seconds() // 3600)
            minutes = int((elapsed.total_seconds() % 3600) // 60)
            seconds = int(elapsed.total_seconds() % 60)

            display_text = f"{self.seat_number}号\n{self.package_type}\n{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.setText(display_text)

    def stop_timing(self):
        self.timer.stop()
        end_time = datetime.now()
        elapsed = end_time - self.start_time

        self.is_occupied = False
        self.setText(str(self.seat_number))
        self.setStyleSheet(self.get_style('空闲'))

        return {
            '开始时间': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            '结束时间': end_time.strftime('%Y-%m-%d %H:%M:%S'),
            '使用时长': str(timedelta(seconds=int(elapsed.total_seconds())))
        }

class StartDialog(QDialog):
    def __init__(self, seat_number, parent=None):
        super().__init__(parent)
        self.seat_number = seat_number
        self.setWindowTitle(f'{seat_number}号座位 - 开始计时')
        self.setMinimumWidth(400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 套餐选择
        package_layout = QHBoxLayout()
        package_layout.addWidget(QLabel('套餐类型：'))
        self.package_combo = QComboBox()
        self.package_combo.addItems(['3小时套餐', '日落场套餐', '小板套餐', '单人套餐', '双人套餐'])
        package_layout.addWidget(self.package_combo)
        layout.addLayout(package_layout)

        # 顾客信息（可选）
        layout.addWidget(QLabel('顾客信息（可选）：'))
        self.customer_info = QTextEdit()
        self.customer_info.setPlaceholderText('可填写顾客姓名、电话、备注等信息...')
        self.customer_info.setMaximumHeight(100)
        layout.addWidget(self.customer_info)

        # 按钮
        button_layout = QHBoxLayout()
        start_btn = QPushButton('开始计时')
        start_btn.clicked.connect(self.accept)
        start_btn.setStyleSheet('background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;')
        cancel_btn = QPushButton('取消')
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet('background-color: #f44336; color: white; padding: 10px; font-size: 14px;')
        button_layout.addWidget(start_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_data(self):
        return {
            '套餐类型': self.package_combo.currentText(),
            '顾客信息': self.customer_info.toPlainText()
        }

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setWindowTitle('拼豆店计时管理系统')
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 标题
        title = QLabel('拼豆店计时管理系统')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet('font-size: 24px; font-weight: bold; padding: 10px;')
        main_layout.addWidget(title)

        # 选项卡
        tabs = QTabWidget()
        tabs.addTab(self.create_seat_panel(), '座位管理')
        tabs.addTab(self.create_record_panel(), '历史记录')
        main_layout.addLayout(QVBoxLayout())
        main_layout.addWidget(tabs)

    def create_seat_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 一号大厅
        hall1_label = QLabel('一号大厅 (1-31号)')
        hall1_label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(hall1_label)

        hall1_grid = QGridLayout()
        self.seats = {}
        for i in range(1, 32):
            row = (i - 1) // 8
            col = (i - 1) % 8
            seat_btn = SeatButton(i)
            seat_btn.clicked.connect(lambda checked, s=seat_btn: self.seat_clicked(s))
            hall1_grid.addWidget(seat_btn, row, col)
            self.seats[i] = seat_btn
        layout.addLayout(hall1_grid)

        # 二号大厅
        hall2_label = QLabel('二号大厅 (32-49号)')
        hall2_label.setStyleSheet('font-size: 18px; font-weight: bold; padding: 10px;')
        layout.addWidget(hall2_label)

        hall2_grid = QGridLayout()
        for i in range(32, 50):
            row = (i - 32) // 6
            col = (i - 32) % 6
            seat_btn = SeatButton(i)
            seat_btn.clicked.connect(lambda checked, s=seat_btn: self.seat_clicked(s))
            hall2_grid.addWidget(seat_btn, row, col)
            self.seats[i] = seat_btn
        layout.addLayout(hall2_grid)

        layout.addStretch()
        return widget

    def create_record_panel(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 刷新按钮
        refresh_btn = QPushButton('刷新记录')
        refresh_btn.clicked.connect(self.load_records)
        refresh_btn.setStyleSheet('padding: 5px; font-size: 14px;')
        layout.addWidget(refresh_btn)

        # 记录表格
        self.record_table = QTableWidget()
        self.record_table.setColumnCount(8)
        self.record_table.setHorizontalHeaderLabels(['ID', '座位号', '套餐类型', '开始时间', '结束时间', '使用时长', '顾客信息', '日期'])
        self.record_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.record_table)

        self.load_records()
        return widget

    def load_records(self):
        records = self.db.get_all_records()
        self.record_table.setRowCount(len(records))
        for i, record in enumerate(records):
            for j, value in enumerate(record):
                self.record_table.setItem(i, j, QTableWidgetItem(str(value)))

    def seat_clicked(self, seat_btn):
        if not seat_btn.is_occupied:
            # 开始计时
            dialog = StartDialog(seat_btn.seat_number, self)
            if dialog.exec_() == QDialog.Accepted:
                data = dialog.get_data()
                seat_btn.start_timing(data['套餐类型'], data['顾客信息'])
        else:
            # 结束计时
            reply = QMessageBox.question(self, '确认',
                                        f'{seat_btn.seat_number}号座位正在使用中，是否结束计时？',
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                timing_data = seat_btn.stop_timing()
                self.db.save_record(
                    seat_btn.seat_number,
                    seat_btn.package_type,
                    timing_data['开始时间'],
                    timing_data['结束时间'],
                    timing_data['使用时长'],
                    seat_btn.customer_info or ''
                )
                QMessageBox.information(self, '完成',
                    f'{seat_btn.seat_number}号座位计时已结束\n使用时长：{timing_data["使用时长"]}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
