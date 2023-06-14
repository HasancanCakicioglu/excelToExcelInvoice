from PyQt5.QtWidgets import QApplication, QMessageBox

def show_warning_message(text):
    app = QApplication([])
    message_box = QMessageBox()
    message_box.setIcon(QMessageBox.Warning)
    message_box.setWindowTitle("Uyarı")
    message_box.setText(text)
    message_box.exec_()


