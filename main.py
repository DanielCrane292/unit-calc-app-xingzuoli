# main.py
# Student Name: Xingzuo Li
# Student Number: 2295275
# GitHub Username: DanielCrane292

import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QDialog,
    QPushButton, QLabel, QLineEdit, QComboBox,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QMenuBar, QMenu, QMessageBox, QListWidget
)

# ===================== Unit Converter Dialog =====================
class UnitConverterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unit Converter")

        # Input label and field
        self.input_label = QLabel("Enter value:")
        self.input_field = QLineEdit()

        # From unit
        self.from_label = QLabel("From:")
        self.from_combo = QComboBox()
        self.from_combo.addItems(["Meters", "Feet", "Celsius", "Fahrenheit"])

        # To unit
        self.to_label = QLabel("To:")
        self.to_combo = QComboBox()
        self.to_combo.addItems(["Meters", "Feet", "Celsius", "Fahrenheit"])

        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_units)

        # Result display
        self.result_label = QLabel("Result: ")
        self.result_value = QLabel("")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.from_label)
        layout.addWidget(self.from_combo)
        layout.addWidget(self.to_label)
        layout.addWidget(self.to_combo)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_value)

        self.setLayout(layout)

    def convert_units(self):
        try:
            value = float(self.input_field.text())
            from_unit = self.from_combo.currentText()
            to_unit = self.to_combo.currentText()

            if from_unit == to_unit:
                result = value
            elif from_unit == "Meters" and to_unit == "Feet":
                result = value * 3.28084
            elif from_unit == "Feet" and to_unit == "Meters":
                result = value / 3.28084
            elif from_unit == "Celsius" and to_unit == "Fahrenheit":
                result = (value * 9 / 5) + 32
            elif from_unit == "Fahrenheit" and to_unit == "Celsius":
                result = (value - 32) * 5 / 9
            else:
                result = "Invalid conversion"

            self.result_value.setText(f"{result}")
        except ValueError:
            self.result_value.setText("Invalid input")

# ===================== Calculator Dialog =====================
from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QFormLayout
)

from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QLineEdit, QComboBox,
    QPushButton, QFormLayout, QListWidget
)

class CalculatorDialog(QDialog):
    calculation_done = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")

        # Input fields
        self.num1_label = QLabel("Number 1:")
        self.num1_input = QLineEdit()

        self.num2_label = QLabel("Number 2:")
        self.num2_input = QLineEdit()

        # Operator selection
        self.operator_label = QLabel("Operator:")
        self.operator_combo = QComboBox()
        self.operator_combo.addItems(["+", "-", "*", "/"])

        # Result display
        self.result_label = QLabel("Result:")
        self.result_value = QLabel("")

        # Buttons
        self.calc_button = QPushButton("Calculate")
        self.calc_button.clicked.connect(self.calculate_result)

        self.save_button = QPushButton("Save Result")
        self.save_button.clicked.connect(self.save_result)

        self.history_button = QPushButton("View History")
        self.history_button.clicked.connect(self.view_history)

        # Layout using QFormLayout
        form_layout = QFormLayout()
        form_layout.addRow(self.num1_label, self.num1_input)
        form_layout.addRow(self.num2_label, self.num2_input)
        form_layout.addRow(self.operator_label, self.operator_combo)
        form_layout.addRow(self.calc_button)
        form_layout.addRow(self.result_label, self.result_value)
        form_layout.addRow(self.save_button)
        form_layout.addRow(self.history_button)

        self.setLayout(form_layout)

    def view_history(self):
        dialog = HistoryDialog()
        dialog.exec()





    def calculate_result(self):
        try:
            num1 = float(self.num1_input.text())
            num2 = float(self.num2_input.text())
            operator = self.operator_combo.currentText()

            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                if num2 == 0:
                    self.result_value.setText("Cannot divide by zero")
                    return
                result = num1 / num2
            else:
                result = "Invalid operator"

            self.result_value.setText(str(result))
            self.calculation_done.emit(str(result))

        except ValueError:
            self.result_value.setText("Invalid input")

    def save_result(self):
                result_text = self.result_value.text()
                if result_text:
                    try:
                        with open("calc_results.txt", "a") as file:
                            num1 = self.num1_input.text()
                            num2 = self.num2_input.text()
                            op = self.operator_combo.currentText()
                            file.write(f"{num1} {op} {num2} = {result_text}\n")
                        self.result_value.setText(result_text + " (Saved)")
                    except Exception as e:
                        self.result_value.setText(f"Error: {e}")
                else:
                    self.result_value.setText("Nothing to save.")

class HistoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculation History")

        self.list_widget = QListWidget()
        self.clear_button = QPushButton("Clear History")
        self.clear_button.clicked.connect(self.clear_history)

        self.load_history()

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.clear_button)
        self.setLayout(layout)

    def load_history(self):
        self.list_widget.clear()
        try:
            with open("calc_results.txt", "r") as file:
                lines = file.readlines()
                self.list_widget.addItems([line.strip() for line in lines])
        except FileNotFoundError:
            self.list_widget.addItem("No history found.")

    def clear_history(self):
        try:
            open("calc_results.txt", "w").close()
            self.list_widget.clear()
            self.list_widget.addItem("History cleared.")
        except Exception as e:
            self.list_widget.addItem(f"Error clearing history: {e}")



# ===================== Main Window =====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utility App - Unit Converter & Calculator")
        self.setMinimumSize(400, 400)

        # Menus
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        tools_menu = menu_bar.addMenu("Tools")
        help_menu = menu_bar.addMenu("Help")

        # Menu actions
        open_converter_action = QAction("Open Unit Converter", self)
        open_converter_action.setShortcut("Ctrl+U")
        open_converter_action.triggered.connect(self.open_unit_converter)

        open_calculator_action = QAction("Open Calculator", self)
        open_calculator_action.setShortcut("Ctrl+C")
        open_calculator_action.triggered.connect(self.open_calculator)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        tools_menu.addAction(open_converter_action)
        tools_menu.addAction(open_calculator_action)
        file_menu.addAction(exit_action)

        # Buttons
        btn_converter = QPushButton("Open Unit Converter")
        btn_converter.setFixedSize(300, 70)
        btn_converter.setStyleSheet("font-size: 18px;")
        btn_converter.clicked.connect(self.open_unit_converter)

        btn_calculator = QPushButton("Open Calculator")
        btn_calculator.setFixedSize(300, 70)
        btn_calculator.setStyleSheet("font-size: 18px;")
        btn_calculator.clicked.connect(self.open_calculator)

        # Layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(40)
        layout.addWidget(btn_converter, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(btn_calculator, alignment=Qt.AlignmentFlag.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def open_unit_converter(self):
        dialog = UnitConverterDialog()
        dialog.exec()

    from PyQt6.QtWidgets import QMessageBox

    def on_calculation_done(self, result_text):
        QMessageBox.information(self, "Calculation Done", f"Result: {result_text}")

    def open_calculator(self):
        dialog = CalculatorDialog()
        dialog.calculation_done.connect(self.on_calculation_done)
        dialog.exec()


# ===================== Entry Point =====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
