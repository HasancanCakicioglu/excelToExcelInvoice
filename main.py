from PyQt5.QtWidgets import QApplication

from screens.mainPageController import myMain

app = QApplication([])
pencere = myMain()
pencere.show()
app.exec_()