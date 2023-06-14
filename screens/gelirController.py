import os
import pandas as pd
import xlrd
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QTableWidget, QComboBox
import numpy
from pandas import DataFrame
from openpyxl import Workbook

from Constants.gelir import GelirConst
from Constants.vergi_daire import data_map
from error.error_box import  show_warning_message
from screens.gelir import Ui_Gelir


class myGelir(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.myPageForm = Ui_Gelir()
        self.myPageForm.setupUi(self)
        self.gelirConst = GelirConst()

        self.myPageForm.pushButton_select_folder.clicked.connect(self.selectFolder)
        self.myPageForm.pushButton.clicked.connect(self.createExcel)

        self.myPageForm.pushButton_doldur.clicked.connect(self.doldur)
        self.myPageForm.pushButton_temizle.clicked.connect(self.temizle)

        self.name = self.myPageForm.comboBox_name.currentText()  # combo box'ta seçili olan metni alır
        self.myPageForm.comboBox_name.currentTextChanged.connect(self.updateName)  # combo box'ta seçim değiştiğinde updateName fonksiyonunu çağırır

        self.type = self.myPageForm.comboBox_type.currentText()
        self.myPageForm.comboBox_type.currentTextChanged.connect(self.updateType)

        self.myPageForm.pushButton_kaydet.clicked.connect(self.kaydetButton)

    def kaydetButton(self):
        self.myPageForm.pushButton_kaydet.setStyleSheet("background-color: rgb(61, 255, 2);")
        self.myPageForm.tableWidgetFaturalar_2.clear()

    def updateName(self,new_text):
        self.name = new_text
        self.myPageForm.pushButton_kaydet.setStyleSheet("background-color: rgb(255, 95, 21);")

    def updateType(self,new_text):
        self.type = new_text
        self.myPageForm.pushButton_kaydet.setStyleSheet("background-color: rgb(255, 95, 21);")

    def doldur(self):

        self.clear(1)
        self.oneToSecondTable()


    def clear(self,table:int):
        if table ==0:
            self.myPageForm.tableWidgetFaturalar_1.clear()
        elif table == 1:
            self.myPageForm.tableWidgetFaturalar_2.clear()
        else:
            self.myPageForm.tableWidgetFaturalar_1.clear()
            self.myPageForm.tableWidgetFaturalar_2.clear()



    def temizle(self):
        self.myPageForm.tableWidgetFaturalar_2.clear()


    def oneToSecondTable(self):

        # İşaretlenmiş satırları al
        selected_rows = []
        for row in range(self.myPageForm.tableWidgetFaturalar_1.rowCount()):
            item = self.myPageForm.tableWidgetFaturalar_1.item(row, 0)

            if item is not None and item.checkState() == Qt.Checked:
                selected_rows.append(row)

        # Verileri DataFrame'e aktar
        data = []
        header_labels = []
        for col in range(self.myPageForm.tableWidgetFaturalar_1.columnCount()):
            header_item = self.myPageForm.tableWidgetFaturalar_1.horizontalHeaderItem(col)
            if header_item is not None:
                header_labels.append(header_item.text())

        for row in selected_rows:
            row_data = []
            for col in range(self.myPageForm.tableWidgetFaturalar_1.columnCount()):
                item = self.myPageForm.tableWidgetFaturalar_1.item(row, col)
                if item is not None:
                    row_data.append(item.text())
            data.append(row_data)

        df = pd.DataFrame(data, columns=header_labels)


        self.fill_crated_excel_2(df)

    def fill_crated_excel_2(self,df:DataFrame):

        self.table_widget = self.myPageForm.tableWidgetFaturalar_2

        rowCount = df.shape[0]

        if self.type == "e-arşiv":
            header = GelirConst.gelirHeader
        else:
            header = GelirConst.gelir_e_Fatura


        self.table_widget.setColumnCount(len(header))
        self.table_widget.setRowCount(rowCount+1)

        self.table_widget.setHorizontalHeaderLabels(header)

        column_names = []
        for i in range(self.myPageForm.tableWidgetFaturalar_1.columnCount()):
            header = self.myPageForm.tableWidgetFaturalar_1.horizontalHeaderItem(i)
            column_names.append(header.text())


        # Populate combo boxes
        for col in column_names:
            combo_box = QComboBox()
            for item in column_names:
                combo_box.addItem(str(item))
            index = column_names.index(col)
            self.table_widget.setCellWidget(0, index, combo_box)
            combo_box.currentIndexChanged.connect(
                lambda index, row=0, col=index: self.update_table(index, row, col,column_names))



        self.fill_ready_part_date(df,"Belge Tarihi",'Oluşturulma Tarihi')
        self.fill_ready_part_date(df, "Deftere Kayıt Tarihi", 'Oluşturulma Tarihi')
        self.fill_ready_part(df, "Adı/Unvan Devamı", 'Firma Ünvanı')

        self.fill_ready_part(df, "Fatura No", 'Fatura No')
        if self.type == "e-arşiv":
            self.fill_ready_part_with_constants("Nihai Tüketici", "Evet")
            self.fill_ready_part_with_constants("Açıklama", 'Fatura Toplu Belge')
        else:
            self.fill_ready_part_tc(df, "TCKN/VKN", 'Alıcı VKN')
            self.fill_ready_part_with_constants("Açıklama", 'e-Fatura Toplu Belge')
            #self.fill_ready_part_with_constants("Vergi Dairesi/Ülke", "052")
            self.fill_comboBox("Vergi Dairesi/Ülke",data_map)


        self.fill_ready_part_name_surname(df, "Adı/Unvan Devamı", 'Firma Ünvanı',True)
        self.fill_ready_part_name_surname(df, "Soyadı/Unvan", 'Firma Ünvanı', False)



        self.fill_ready_part_with_constants("Satış Türü", "1")
        self.fill_ready_part_with_constants("Gelir Kayıt Türü", "1")
        self.fill_ready_part_with_constants("Gelir Kayıt Alt Türü", "2")

        self.fill_ready_part_with_constants("Faaliyet Kodu", "479114")
        self.fill_ready_part_with_constants("KDV Oranı", "18")

        self.fill_ready_part_kdv_haric(df,"Tutar (KDV Hariç)","Fatura Tutarı","Toplam Vergi")

        self.fill_ready_part_with_constants("Kredi Kartı", '0')



    def fill_comboBox(self,header,data_map):
        # Create the ComboBox widget
        combo_box = QComboBox()
        combo_box.setEditable(True)
        combo_box.setInsertPolicy(QtWidgets.QComboBox.NoInsert)

        # Add the items to the ComboBox
        for name, value in data_map.items():
            combo_box.addItem(name, value)
        selected_item = combo_box.currentText()
        column_index = 6
        for row in range(1,self.table_widget.rowCount()):
            # Connect the currentIndexChanged signal of the ComboBox to a function
            def update_table_cell(index):
                selected_item = combo_box.currentText()
                self.table_widget.setItem(row, column_index, QTableWidgetItem(data_map[selected_item].zfill(6)))

            combo_box.currentIndexChanged.connect(update_table_cell)

            # Set the initial value for the cell
            selected_item = combo_box.currentText()
            number = data_map[selected_item]
            print(number)
            print(selected_item)
            self.table_widget.setItem(row, column_index, QTableWidgetItem(number))

            # Set the ComboBox as the cell widget
            self.table_widget.setCellWidget(row, column_index, combo_box)
        self.table_widget.setColumnWidth(column_index, 400)

    def createExcel(self):
        row_count = self.table_widget.rowCount()
        col_count = self.table_widget.columnCount()
        headers = [self.table_widget.horizontalHeaderItem(col).text() for col in range(col_count)]

        data = []
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = self.table_widget.item(row, col)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)

        df = pd.DataFrame(data, columns=headers)

        # Excel dosyasını kaydetmek için dosya yolunu al
        file_path, _ = QFileDialog.getSaveFileName(self, "Excel Kaydet", "", "Excel Dosyası (*.xlsx)")

        if file_path:

            workbook = Workbook()
            sheet = workbook.active
            sheet.append(df.columns.tolist())

            for index, row in df.iloc[1:].iterrows():
                sheet.append(row.tolist())

            # Excel dosyasını kaydetme
            workbook.save(file_path)

    def fill_ready_part(self,df:DataFrame,first:str,second:str):
        # hazır kodları otomatik dolduracak
        # Sütun başlıklarının alınması

        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        # "belge_tarihi" sütununun indeksinin bulunması
        belge_tarihi_column_index = headers.index(first)

        # "belge_tarihi" sütununun güncellenmesi
        for row in range(1,self.table_widget.rowCount()):

            belge_tarihi = df.iloc[row-1][second]
            item = QTableWidgetItem(str(belge_tarihi))
            self.table_widget.setItem(row, belge_tarihi_column_index, item)

    def fill_ready_part_tc(self,df:DataFrame,first:str,second:str):
        # hazır kodları otomatik dolduracak
        # Sütun başlıklarının alınması

        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        # "belge_tarihi" sütununun indeksinin bulunması
        belge_tarihi_column_index = headers.index(first)

        # "belge_tarihi" sütununun güncellenmesi
        for row in range(1,self.table_widget.rowCount()):
            belge_tarihi = str(df.iloc[row-1][second]).split(".")[0]
            # alttaki satıra belge tarihni yazdırırsan tcyi yazar
            item = QTableWidgetItem(belge_tarihi)
            self.table_widget.setItem(row, belge_tarihi_column_index, item)

    def fill_ready_part_date(self,df:DataFrame,first:str,second:str):
        # hazır kodları otomatik dolduracak
        # Sütun başlıklarının alınması

        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        # "belge_tarihi" sütununun indeksinin bulunması
        belge_tarihi_column_index = headers.index(first)

        # "belge_tarihi" sütununun güncellenmesi
        for row in range(1,self.table_widget.rowCount()):

            belge_tarihi = str(df.iloc[row-1][second]).split(" ")[0].replace("-", ".")
            new_date = str(belge_tarihi.split(".")[-1])+"."+str(belge_tarihi.split(".")[-2])+"."+str(belge_tarihi.split(".")[-3][-2:])
            item = QTableWidgetItem(new_date)
            self.table_widget.setItem(row, belge_tarihi_column_index, item)

    def fill_ready_part_kdv_haric(self,df:DataFrame,first:str,second:str,third:str):
        # hazır kodları otomatik dolduracak
        # Sütun başlıklarının alınması

        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        # "belge_tarihi" sütununun indeksinin bulunması
        belge_tarihi_column_index = headers.index(first)

        # "belge_tarihi" sütununun güncellenmesi
        for row in range(1,self.table_widget.rowCount()):
            #fiyat = df.iloc[row-1][second] - df.iloc[row-1][third]
            fiyat = float(df.iloc[row - 1][second]) - float(df.iloc[row - 1][third])

            formatli_fiyat = "{:,.2f}".format(fiyat).replace(".", ",")
            item = QTableWidgetItem(str(formatli_fiyat))
            self.table_widget.setItem(row, belge_tarihi_column_index, item)

    def fill_ready_part_with_constants(self,first:str,const:str):
        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        # "belge_tarihi" sütununun indeksinin bulunması
        belge_tarihi_column_index = headers.index(first)

        # "belge_tarihi" sütununun güncellenmesi
        for row in range(1, self.table_widget.rowCount()):

            item = QTableWidgetItem(str(const))
            self.table_widget.setItem(row, belge_tarihi_column_index, item)

    def fill_ready_part_with_constants(self,first:str,const:str):
        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        # "belge_tarihi" sütununun indeksinin bulunması
        belge_tarihi_column_index = headers.index(first)

        # "belge_tarihi" sütununun güncellenmesi
        for row in range(1, self.table_widget.rowCount()):

            item = QTableWidgetItem(str(const))
            self.table_widget.setItem(row, belge_tarihi_column_index, item)


    def fill_ready_part_name_surname(self,df:DataFrame,first:str,second:str,isName:bool):
        # hazır kodları otomatik dolduracak
        # Sütun başlıklarının alınması

        headers = [self.table_widget.horizontalHeaderItem(i).text() for i in range(self.table_widget.columnCount())]

        # "belge_tarihi" sütununun indeksinin bulunması
        belge_tarihi_column_index = headers.index(first)

        # "belge_tarihi" sütununun güncellenmesi
        for row in range(1,self.table_widget.rowCount()):
            belge_tarihi = df.iloc[row-1][second]
            if isName:
                belge_tarihi = " ".join(belge_tarihi.split(" ")[:-1])

            else:
                belge_tarihi = belge_tarihi.split(" ")[-1]
            item = QTableWidgetItem(str(belge_tarihi))
            self.table_widget.setItem(row, belge_tarihi_column_index, item)

    def fill_crated_excel(self,df:DataFrame):

        self.table_widget = self.myPageForm.tableWidgetFaturalar_2

        rowCount = self.myPageForm.tableWidgetFaturalar_1.rowCount()

        header = GelirConst.gelirHeader


        self.table_widget.setColumnCount(len(header))
        self.table_widget.setRowCount(rowCount+1)

        self.table_widget.setHorizontalHeaderLabels(header)

        column_names = []
        for i in range(self.myPageForm.tableWidgetFaturalar_1.columnCount()):
            header = self.myPageForm.tableWidgetFaturalar_1.horizontalHeaderItem(i)
            column_names.append(header.text())


        # Populate combo boxes
        for col in column_names:
            combo_box = QComboBox()
            for item in column_names:
                combo_box.addItem(str(item))
            index = column_names.index(col)
            self.table_widget.setCellWidget(0, index, combo_box)
            combo_box.currentIndexChanged.connect(
                lambda index, row=0, col=index: self.update_table(index, row, col,column_names))



        self.fill_ready_part_date(df,"Belge Tarihi",'Oluşturulma Tarihi')
        self.fill_ready_part_date(df, "Deftere Kayıt Tarihi", 'Oluşturulma Tarihi')
        self.fill_ready_part(df, "Adı/Unvan Devamı", 'Firma Ünvanı')

        self.fill_ready_part(df, "Fatura No", 'Fatura No')
        self.fill_ready_part_with_constants("Nihai Tüketici","Evet")
        self.fill_ready_part_tc(df, "TCKN/VKN", 'Alıcı VKN')

        self.fill_ready_part_name_surname(df, "Adı/Unvan Devamı", 'Firma Ünvanı',True)
        self.fill_ready_part_name_surname(df, "Soyadı/Unvan", 'Firma Ünvanı', False)

        self.fill_ready_part_with_constants("Vergi Dairesi/Ülke", "")

        self.fill_ready_part_with_constants("Satış Türü", "1")
        self.fill_ready_part_with_constants("Gelir Kayıt Türü", "1")
        self.fill_ready_part_with_constants("Gelir Kayıt Alt Türü", "2")

        self.fill_ready_part_with_constants("Faaliyet Kodu", "479114")

        self.fill_ready_part_with_constants("KDV Oranı", "18")

        self.fill_ready_part_kdv_haric(df,"Tutar (KDV Hariç)","Fatura Tutarı","Toplam Vergi")

        self.fill_ready_part_with_constants("Kredi Kartı", '0')
        self.fill_ready_part_with_constants("Açıklama", 'Fatura Toplu Belge')


    def update_combo_box(self):

        column_names = []
        for i in range(self.myPageForm.tableWidgetFaturalar_1.columnCount()):
            header = self.myPageForm.tableWidgetFaturalar_1.horizontalHeaderItem(i)
            column_names.append(header.text())
            self.myComboBox.addItem(header.text())




    def update_table(self, index, row,col,column_names):

        oneColumnDatas = []
        columnIndex = index  # 0'dan başlayarak sıfırdan başlayarak 3. sütunun indeksi 2'dir

        for row in range(self.myPageForm.tableWidgetFaturalar_1.rowCount()):
            item = self.myPageForm.tableWidgetFaturalar_1.item(row, columnIndex)
            if item is not None:
                oneColumnDatas.append(item.text())


        for row in range(0, self.table_widget.rowCount()-1):
            cell = QTableWidgetItem(str(oneColumnDatas[row]))
            self.table_widget.setItem(row+1, col, cell)


    def selectFolder(self):
        file_filter = 'Data File (*.xlsx *.csv *.dat);; Excel File (*.xlsx *.xls)'
        file, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Excel File (*.xlsx *.xls)'
        )


        if file == "":
            return None

        self.setLineEditText(file)
        df = self.getPDdata()
        if df is None:
            return None
        self.writeToQTableWidget(df)
        rowCount = self.myPageForm.tableWidgetFaturalar_1.rowCount()
        self.myPageForm.tableWidgetFaturalar_2.setRowCount(rowCount)
        #self.fill_crated_excel(df)





    def getPDdata(self):

        df = None
        try:
            file_name = self.myPageForm.lineEdit_path_excel.text()
            wb = xlrd.open_workbook(file_name, logfile=open(os.devnull, 'w'))
            df = pd.read_excel(io=wb,engine='xlrd')
        except Exception as e:
            print("hata = " + str(e))

        if type(df) != DataFrame:
            return None

        self.myPageForm.tableWidgetFaturalar_1.setRowCount(len(df)-1)
        self.myPageForm.tableWidgetFaturalar_1.setColumnCount(len(df.columns))
        try:
            if self.type == "e-arşiv":
                df['Rapor Oluşturulma Tarihi'] = pd.to_datetime(df['Rapor Oluşturulma Tarihi'],
                                                                format='%d.%m.%Y %H:%M:%S')
            else:
                df['Rapor Oluşturulma Tarihi'] = pd.to_datetime(df['Oluşturulma Tarihi'], format='%d.%m.%Y %H:%M:%S')
        except:
            #show_warning_message("format yanlış E-fatura veya E-arşiv değiştir onu  ")
            return None


        df = df.sort_values(by='Rapor Oluşturulma Tarihi')

        return df

    def writeToQTableWidget(self,df:DataFrame):

        try:
            for row in range(len(df)):
                for col in range(len(df.columns)):
                    if col % len(df.columns) == 0:
                        item = QTableWidgetItem(str(df.iloc[row, col]))
                        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                        item.setCheckState(Qt.CheckState.Checked)
                        self.myPageForm.tableWidgetFaturalar_1.setItem(row, col, item)
                    else:
                        self.myPageForm.tableWidgetFaturalar_1.setItem(row, col, QTableWidgetItem(str(df.iloc[row, col])))


            for i, column_name in enumerate(df.columns):
                item = QTableWidgetItem(column_name)
                self.myPageForm.tableWidgetFaturalar_1.setHorizontalHeaderItem(i, item)
        except:
            pass

    def setLineEditText(self,file):
        self.myPageForm.lineEdit_path_excel.setText(file)
