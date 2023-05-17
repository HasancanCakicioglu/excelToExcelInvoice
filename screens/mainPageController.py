from PyQt5.QtWidgets import QMainWindow

from screens.gelirController import myGelir
from screens.mainPage import Ui_MainWindow


class myMain(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.myPageForm = Ui_MainWindow()
        self.myPageForm.setupUi(self)

        self.gelirPage = myGelir()


        self.myPageForm.pushButton_gelir.clicked.connect(self.goToGelirPage)


    def goToGelirPage(self):
        self.gelirPage.show()
