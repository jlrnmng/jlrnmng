import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton
import mysql.connector
from mysql.connector import Error, errorcode
from tabulate import tabulate
import configparser

class DBManagementApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Management System")
        self.init_ui()

        self.connection = None
        self.connect_to_db()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Top Frame
        top_frame_layout = QHBoxLayout()
        top_frame_layout.addWidget(QLabel("Table Name:"))
        self.table_name_entry = QLineEdit()
        top_frame_layout.addWidget(self.table_name_entry)
        main_layout.addLayout(top_frame_layout)

        # Middle Frame
        middle_frame_layout = QVBoxLayout()
        fields_layout = QHBoxLayout()
        fields_layout.addWidget(QLabel("Fields:"))
        self.fields_entry = QLineEdit()
        fields_layout.addWidget(self.fields_entry)
        middle_frame_layout.addLayout(fields_layout)

        values_layout = QHBoxLayout()
        values_layout.addWidget(QLabel("Values:"))
        self.values_entry = QLineEdit()
        values_layout.addWidget(self.values_entry)
        middle_frame_layout.addLayout(values_layout)

        update_layout = QHBoxLayout()
        update_layout.addWidget(QLabel("Update Fields:"))
        self.update_fields_entry = QLineEdit()
        update_layout.addWidget(self.update_fields_entry)
        middle_frame_layout.addLayout(update_layout)

        update_values_layout = QHBoxLayout()
        update_values_layout.addWidget(QLabel("Update Values:"))
        self.update_values_entry = QLineEdit()
        update_values_layout.addWidget(self.update_values_entry)
        middle_frame_layout.addLayout(update_values_layout)

        condition_layout = QHBoxLayout()
        condition_layout.addWidget(QLabel("Condition Field:"))
        self.condition_field_entry = QLineEdit()
        condition_layout.addWidget(self.condition_field_entry)
        middle_frame_layout.addLayout(condition_layout)

        condition_value_layout = QHBoxLayout()
        condition_value_layout.addWidget(QLabel("Condition Value:"))
        self.condition_value_entry = QLineEdit()
        condition_value_layout.addWidget(self.condition_value_entry)
        middle_frame_layout.addLayout(condition_value_layout)

        main_layout.addLayout(middle_frame_layout)

        # Result Text
        self.result_text = QTextEdit()
        main_layout.addWidget(self.result_text)

        # Buttons
        button_layout = QHBoxLayout()
        view_btn = QPushButton("View Data")
        view_btn.clicked.connect(self.view_data)
        button_layout.addWidget(view_btn)

        add_btn = QPushButton("Add Record")
        add_btn.clicked.connect(self.add_record)
        button_layout.addWidget(add_btn)

        update_btn = QPushButton("Update Record")
        update_btn.clicked.connect(self.update_record)
        button_layout.addWidget(update_btn)

        delete_btn = QPushButton("Delete Record")
        delete_btn.clicked.connect(self.delete_record)
        button_layout.addWidget(delete_btn)

        exit_btn = QPushButton("Exit")
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def connect_to_db(self):
        try:
            db_config = self.read_db_config()
            self.connection = mysql.connector.connect(**db_config)
            if self.connection.is_connected():
                print('Connected to MySQL Database')
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Error, Access Denied. Please check your username and password.')
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print('Error, Database does not Exist.')
            else:
                print(e)

    def read_db_config(self, filename='config.ini', section='mysql'):
        parser = configparser.ConfigParser()
        parser.read(filename)
        db = {}
        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception(f'{section} not found in the {filename} file.')

        return db

    def view_data(self):
        table_name = self.table_name_entry.text()
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            if data:
                headers = [desc[0] for desc in cursor.description]
                self.result_text.setText(tabulate(data, headers=headers, tablefmt='grid'))
            else:
                self.result_text.setText("No data found in the table")
        except Error as e:
            self.result_text.setText("Error fetching data: " + str(e))

    def add_record(self):
        table_name = self.table_name_entry.text()
        fields = self.fields_entry.text().split(',')
        values = self.values_entry.text().split(',')
        try:
            cursor = self.connection.cursor()
            query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(['%s']*len(values))})"
            cursor.execute(query, values)
            self.connection.commit()
            self.result_text.setText("Record added successfully")
        except Error as e:
            self.result_text.setText("Error adding record: " + str(e))

    def update_record(self):
        table_name = self.table_name_entry.text()
        update_fields = self.update_fields_entry.text().split(',')
        update_values = self.update_values_entry.text().split(',')
        condition_field = self.condition_field_entry.text()
        condition_value = self.condition_value_entry.text()
        try:
            cursor = self.connection.cursor()
            set_values = ', '.join([f"{field} = %s" for field in update_fields])
            query = f"UPDATE {table_name} SET {set_values} WHERE {condition_field} = %s"
            cursor.execute(query, (*update_values, condition_value))
            self.connection.commit()
            self.result_text.setText("Record updated successfully")
        except Error as e:
            self.result_text.setText("Error updating record: " + str(e))

    def delete_record(self):
        table_name = self.table_name_entry.text()
        condition_field = self.condition_field_entry.text()
        condition_value = self.condition_value_entry.text()
        try:
            cursor = self.connection.cursor()
            query = f"DELETE FROM {table_name} WHERE {condition_field} = %s"
            cursor.execute(query, (condition_value,))
            self.connection.commit()
            self.result_text.setText("Record deleted successfully")
        except Error as e:
            self.result_text.setText("Error deleting record: " + str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    db_app = DBManagementApp()
    db_app.show()
    sys.exit(app.exec_())
