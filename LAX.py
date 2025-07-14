'''AIRPORT DATABASE APP AND GUI'''

from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import time

#Modules omitted for GitHub demo
# from insert_aircraft3 import Ui_InsertAircraftWindow
# from delete_aicraft5 import Ui_Delete_Aircraft
# from update_airline import Ui_update_airline
# from insert_airline import Ui_insert_airline
# from delete_airline import Ui_Delete_Airline
# from update_scheduled_flight import Ui_MainWindow2
# from insert_scheduled import Ui_MainWindow5
# from delete_scheduled import Ui_MainWindow20
# from update_flight import Ui_Flight

import datetime

class Ui_MainWindow(object):
    def __init__(self,d):
        self.database = d
        self.aircraft_clicked = False
        self.airline_clicked = False
        self.scheduled_flight = False
        self.gate_clicked = False
        self.counter_clicked = False
        self.flight_clicked = False

        self.options = {"type": "DEPARTURES", "airport": "%", "airline": "%","flight_number": "> 0" }
                        

    #Μέθοδοι που ανοίγουν τα παράθυρα των λειτουργιών insert, update, delete
    def open_insert_aircraft_window(self):
        self.insert_aircraft_window = QtWidgets.QMainWindow()
        self.insert_aircraft_ui = Ui_InsertAircraftWindow()
        self.insert_aircraft_ui.setupUi(self.insert_aircraft_window)
        self.insert_aircraft_window.show()
        
    def open_delete_aircraft_window(self):
        self.delete_aircraft_window = QtWidgets.QMainWindow()
        self.delete_aircraft_ui = Ui_Delete_Aircraft()
        self.delete_aircraft_ui.setupUi(self.delete_aircraft_window)
        self.delete_aircraft_ui.filter.addItem("ID")
        self.delete_aircraft_ui.filter.addItem("Name")
        self.delete_aircraft_ui.filter.addItem("ICAO")
        self.delete_aircraft_ui.filter.addItem("IATA")
        self.delete_aircraft_ui.comboBox.setEnabled(False)
        self.delete_aircraft_ui.comboBox_2.setEnabled(False)
        self.delete_aircraft_ui.comboBox_3.setEnabled(False)
        self.delete_aircraft_ui.comboBox_4.setEnabled(False)
        self.delete_aircraft_window.show()

        self.delete_aircraft_ui.aircraft_done_2.clicked.connect(self.setAircraftValues)

    def open_update_airline_window(self):
        self.update_airline_window = QtWidgets.QMainWindow()
        self.update_airline_ui = Ui_update_airline()
        self.update_airline_ui.setupUi(self.update_airline_window)
        sql = "select airline_id from AIRLINE order by airline_id"
        results = self.database.executeSQL(sql)

        for i in range(len(results)):
                number = str(results[i][-1])
                self.update_airline_ui.airline_id.addItem(number)
        self.update_airline_window.show()

    def open_insert_airline_window(self):
        self.insert_airline_window = QtWidgets.QMainWindow()
        self.insert_airline_ui = Ui_insert_airline()
        self.insert_airline_ui.setupUi(self.insert_airline_window)
        self.insert_airline_window.show()
    
    def open_delete_airline_window(self):
        self.delete_airline_window = QtWidgets.QMainWindow()
        self.delete_airline_ui = Ui_Delete_Airline()
        self.delete_airline_ui.setupUi(self.delete_airline_window)
        self.delete_airline_ui.comboBox.setEnabled(False)
        self.delete_airline_ui.comboBox_2.setEnabled(False)
        self.delete_airline_ui.comboBox_3.setEnabled(False)
        self.delete_airline_ui.comboBox_4.setEnabled(False)
        
        self.delete_airline_window.show()
        self.delete_airline_ui.aircraft_done_2.clicked.connect(self.setAirlineValues)

    def open_update_scheduled_flight_window(self):
        self.update_scheduled_flight_window = QtWidgets.QMainWindow()
        self.update_scheduled_flight_ui = Ui_MainWindow2()
        self.update_scheduled_flight_ui.setupUi(self.update_scheduled_flight_window)
        sql = "select FlightNumber from SCHEDULED_FLIGHT where julianday(Valid_Until) > julianday('2022-01-04') order by FlightNumber"
        results = self.database.executeSQL(sql)
        for i in range(len(results)):
                number = str(results[i][-1])
                self.update_scheduled_flight_ui.flight_number.addItem(number)
        self.update_scheduled_flight_window.show()
        self.update_scheduled_flight_ui.ok.clicked.connect(self.setValidUntil)
        
    def open_insert_scheduled_flight_window(self):
        self.insert_scheduled_flight_window = QtWidgets.QMainWindow()
        self.insert_scheduled_flight_ui = Ui_MainWindow5()
        self.insert_scheduled_flight_ui.setupUi(self.insert_scheduled_flight_window)
        self.set_airports_aircrafts_airlines()
        self.insert_scheduled_flight_window.show()
        self.insert_scheduled_flight_ui.origin_airport.activated.connect(self.change_destination_airport)
        self.insert_scheduled_flight_ui.destination_airport.activated.connect(self.change_origin_airport)


    def open_delete_scheduled_flight_window(self):
        self.delete_scheduled_flight_window = QtWidgets.QMainWindow()
        self.delete_scheduled_flight_ui = Ui_MainWindow20()
        self.delete_scheduled_flight_ui.setupUi(self.delete_scheduled_flight_window)
        sql = "select FlightNumber from SCHEDULED_FLIGHT order by FlightNumber"
        results = self.database.executeSQL(sql)
        for i in range(len(results)):
            number = str(results[i][-1])
            self.delete_scheduled_flight_ui.flight_number.addItem(number)
                
        self.delete_scheduled_flight_window.show()

    def open_update_flight_window(self):
        self.update_flight_window = QtWidgets.QMainWindow()
        self.update_flight_ui = Ui_Flight()
        self.update_flight_ui.setupUi(self.update_flight_window)
        self.set_todays_flights()
        self.update_flight_ui.pushButton.clicked.connect(self.fillGateStatus)
        self.update_flight_window.show()
    

    #Methods that put Items in the comboBoxes of the insert, update, delete windows
    def setAircraftValues(self):
        if (self.delete_aircraft_ui.filter.currentText() == "ID"):
            sql1 = "select ID from AIRCRAFT"
            results_id = self.database.executeSQL(sql1)
            for i in range(len(results_id)):
                number = str(results_id[i][-1])
                self.delete_aircraft_ui.comboBox.addItem(number)
                self.delete_aircraft_ui.comboBox.setEnabled(True)
                self.delete_aircraft_ui.comboBox_2.setEnabled(False)
                self.delete_aircraft_ui.comboBox_3.setEnabled(False)
                self.delete_aircraft_ui.comboBox_4.setEnabled(False)

                self.delete_aircraft_ui.comboBox_2.clear()
                self.delete_aircraft_ui.comboBox_3.clear()
                self.delete_aircraft_ui.comboBox_4.clear()


        elif (self.delete_aircraft_ui.filter.currentText() == "Name"):
            sql2 = "select distinct(Name) from AIRCRAFT where Name is not null order by Name"
            results_name = self.database.executeSQL(sql2)
            for i in range(len(results_name)):
                number = str(results_name[i][-1])
                self.delete_aircraft_ui.comboBox_2.addItem(number)                 
                self.delete_aircraft_ui.comboBox.setEnabled(False)
                self.delete_aircraft_ui.comboBox_2.setEnabled(True)
                self.delete_aircraft_ui.comboBox_3.setEnabled(False)
                self.delete_aircraft_ui.comboBox_4.setEnabled(False)

                self.delete_aircraft_ui.comboBox.clear()
                self.delete_aircraft_ui.comboBox_3.clear()
                self.delete_aircraft_ui.comboBox_4.clear()

        elif (self.delete_aircraft_ui.filter.currentText() == "ICAO"):
            sql3 = "select distinct(ICAO) from AIRCRAFT where ICAO is not null order by ICAO"
            results_icao = self.database.executeSQL(sql3)
            for i in range(len(results_icao)):
                number = str(results_icao[i][-1])
                self.delete_aircraft_ui.comboBox_3.addItem(number)                 
                self.delete_aircraft_ui.comboBox.setEnabled(False)
                self.delete_aircraft_ui.comboBox_2.setEnabled(False)
                self.delete_aircraft_ui.comboBox_3.setEnabled(True)
                self.delete_aircraft_ui.comboBox_4.setEnabled(False)

                self.delete_aircraft_ui.comboBox.clear()
                self.delete_aircraft_ui.comboBox_2.clear()
                self.delete_aircraft_ui.comboBox_4.clear()

        else :
            sql4 = "select distinct(IATA) from AIRCRAFT where IATA is not null order by IATA"
            results_iata = self.database.executeSQL(sql4)
            for i in range(len(results_iata)):
                number = str(results_iata[i][-1])
                self.delete_aircraft_ui.comboBox_4.addItem(number)
                self.delete_aircraft_ui.comboBox.setEnabled(False)
                self.delete_aircraft_ui.comboBox_2.setEnabled(False)
                self.delete_aircraft_ui.comboBox_3.setEnabled(False)
                self.delete_aircraft_ui.comboBox_4.setEnabled(True)

                self.delete_aircraft_ui.comboBox.clear()
                self.delete_aircraft_ui.comboBox_2.clear()
                self.delete_aircraft_ui.comboBox_3.clear()



    def setAirlineValues(self):
        if (self.delete_airline_ui.filter.currentText() == "airline_id"):
            sql1 = "select airline_id from AIRLINE"
            results_id = self.database.executeSQL(sql1)
            for i in range(len(results_id)):
                number = str(results_id[i][-1])
                self.delete_airline_ui.comboBox.addItem(number)
                self.delete_airline_ui.comboBox.setEnabled(True)
                self.delete_airline_ui.comboBox_2.setEnabled(False)
                self.delete_airline_ui.comboBox_3.setEnabled(False)
                self.delete_airline_ui.comboBox_4.setEnabled(False)

                self.delete_airline_ui.comboBox_2.clear()
                self.delete_airline_ui.comboBox_3.clear()
                self.delete_airline_ui.comboBox_4.clear()


        elif (self.delete_airline_ui.filter.currentText() == "name"):
            sql2 = "select distinct(name) from AIRLINE where name is not null order by name"
            results_name = self.database.executeSQL(sql2)
            for i in range(len(results_name)):
                number = str(results_name[i][-1])
                self.delete_airline_ui.comboBox_2.addItem(number)                 
                self.delete_airline_ui.comboBox.setEnabled(False)
                self.delete_airline_ui.comboBox_2.setEnabled(True)
                self.delete_airline_ui.comboBox_3.setEnabled(False)
                self.delete_airline_ui.comboBox_4.setEnabled(False)
                
                self.delete_airline_ui.comboBox.clear()
                self.delete_airline_ui.comboBox_3.clear()
                self.delete_airline_ui.comboBox_4.clear()    

        elif (self.delete_airline_ui.filter.currentText() == "ICAO"):
            sql3 = "select distinct(ICAO) from AIRLINE where ICAO is not null order by ICAO"
            results_icao = self.database.executeSQL(sql3)
            for i in range(len(results_icao)):
                number = str(results_icao[i][-1])
                self.delete_airline_ui.comboBox_3.addItem(number)                 
                self.delete_airline_ui.comboBox.setEnabled(False)
                self.delete_airline_ui.comboBox_2.setEnabled(False)
                self.delete_airline_ui.comboBox_3.setEnabled(True)
                self.delete_airline_ui.comboBox_4.setEnabled(False)

                self.delete_airline_ui.comboBox.clear()
                self.delete_airline_ui.comboBox_2.clear()
                self.delete_airline_ui.comboBox_4.clear()
                
        else :
            sql4 = "select distinct(IATA) from AIRLINE where IATA is not null order by IATA"
            results_iata = self.database.executeSQL(sql4)
            for i in range(len(results_iata)):
                number = str(results_iata[i][-1])
                self.delete_airline_ui.comboBox_4.addItem(number)
                self.delete_airline_ui.comboBox.setEnabled(False)
                self.delete_airline_ui.comboBox_2.setEnabled(False)
                self.delete_airline_ui.comboBox_3.setEnabled(False)
                self.delete_airline_ui.comboBox_4.setEnabled(True)

                self.delete_airline_ui.comboBox.clear()
                self.delete_airline_ui.comboBox_2.clear()
                self.delete_airline_ui.comboBox_3.clear()
        


    def setValidUntil(self):
        flight_num = self.update_scheduled_flight_ui.flight_number.currentText()
        sql = "select Valid_Until from SCHEDULED_FLIGHT where FlightNumber = ?"
        data = (flight_num,)
        date = self.database.executeSQLparam(sql,data)
        valid_until = date[0].get('Valid_Until')

        self.update_scheduled_flight_ui.valid_until.setText(valid_until)
        self.update_scheduled_flight_ui.calendar_ui.calendarWidget.setMinimumDate(QtCore.QDate(int(valid_until[:4]),int(valid_until[5:7]),int(valid_until[8:])))
        self.update_scheduled_flight_ui.calendar_ui.calendarWidget.setSelectedDate(QtCore.QDate(int(valid_until[:4]),int(valid_until[5:7]),int(valid_until[8:])))




    def fillGateStatus(self):
        flight_num = self.update_flight_ui.flight_number.currentText()
        sql = "select Status from ACTUAL_FLIGHT where Flight_Number = ?"
        results = self.database.executeSQLparam(sql,(flight_num,))
        status = results[0].get('Status')
        if (status == "Departures_Soon"):
            self.update_flight_ui.gate.setEnabled(True)
            sql = "select ID from GATE"
            res = self.database.executeSQL(sql)
            for i in res:
                self.update_flight_ui.gate.addItem(str(i[-1]))
                
            self.update_flight_ui.status.clear()
            self.update_flight_ui.status.addItem("Departures_Soon")
            self.update_flight_ui.status.addItem("Departed")
            self.update_flight_ui.status.addItem("Cancelled")

        elif (status == "Expected"):
            self.update_flight_ui.gate.clear()
            self.update_flight_ui.gate.setEnabled(False)
            self.update_flight_ui.status.clear()
            self.update_flight_ui.status.addItem("Expected")
            self.update_flight_ui.status.addItem("Cancelled")
            self.update_flight_ui.status.addItem("Arrived")


        
    def set_todays_flights(self):
        sql = "select Flight_Number from ACTUAL_FLIGHT where Status = 'Departures_Soon' or Status = 'Expected'"
        results = self.database.executeSQL(sql)
        for i in range(len(results)):
            number = str(results[i][-1])
            self.update_flight_ui.flight_number.addItem(number)
            
    def set_airports_aircrafts_airlines(self):
        sql = "select IATA from AIRPORT"
        results = self.database.executeSQL(sql)
        for i in range(len(results)):
            airport = str(results[i][-1])
            self.insert_scheduled_flight_ui.origin_airport.addItem(airport)
            self.insert_scheduled_flight_ui.destination_airport.addItem(airport)

        sql = "select IATA from AIRCRAFT"
        results = self.database.executeSQL(sql)
        for i in range(len(results)):
            aircraft = str(results[i][-1])
            self.insert_scheduled_flight_ui.aircraft.addItem(aircraft)

        sql = "select airline_id from AIRLINE"
        results = self.database.executeSQL(sql)
        for i in range(len(results)):
            airline = str(results[i][-1])
            self.insert_scheduled_flight_ui.airline_id.addItem(airline)


    def change_destination_airport(self):
        origin_airport = self.insert_scheduled_flight_ui.origin_airport.currentText()
        destination_airport = self.insert_scheduled_flight_ui.destination_airport.currentText()
        if (origin_airport != "LAX"):
            self.insert_scheduled_flight_ui.destination_airport.setCurrentText("LAX")


    def change_origin_airport(self):
        origin_airport = self.insert_scheduled_flight_ui.origin_airport.currentText()
        destination_airport = self.insert_scheduled_flight_ui.destination_airport.currentText()
        if (destination_airport != "LAX"):
            self.insert_scheduled_flight_ui.origin_airport.setCurrentText("LAX")


    #Setting up the interface  
    def setupUi(self, MainWindow):

        self.stylesheet = '''
    #MainWindow {
        border-image: url(background.jpg);
        background-repeat: no-repeat; 

        background-position: center;
    }
'''        
        MainWindow.setStyleSheet(self.stylesheet)
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 822)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.wecolme_label = QtWidgets.QLabel(self.centralwidget)
        self.wecolme_label.setGeometry(QtCore.QRect(410, 10, 781, 71))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.wecolme_label.setFont(font)
        self.wecolme_label.setObjectName("wecolme_label")
        self.results = QtWidgets.QTableWidget(self.centralwidget)
        self.results.setGeometry(QtCore.QRect(30, 260, 1171, 481))
        self.results.setObjectName("results")
        self.results.setColumnCount(0)
        self.results.setRowCount(0)
        self.action = QtWidgets.QLabel(self.centralwidget)
        self.action.setGeometry(QtCore.QRect(110, 120, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.action.setFont(font)
        self.action.setObjectName("action")
        self.cb = QtWidgets.QComboBox(self.centralwidget)
        self.cb.setGeometry(QtCore.QRect(220, 130, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cb.setFont(font)
        self.cb.setObjectName("cb")
        self.cb.addItem("")
        self.cb.addItem("")
        self.cb.addItem("")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1048, 26))
        self.menubar.setObjectName("menubar")


        
        self.menuHome = QtWidgets.QMenu(self.menubar)
        self.menuHome.setObjectName("menuHome")


        self.menuFlights = QtWidgets.QMenu(self.menubar)
        self.menuFlights.setObjectName("menuFlights")


        
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")


        
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionAIRCRAFT = QtWidgets.QAction(MainWindow)
        self.actionAIRCRAFT.setObjectName("actionAIRCRAFT")
        self.actionAIRCRAFT_2 = QtWidgets.QAction(MainWindow)
        self.actionAIRCRAFT_2.setObjectName("actionAIRCRAFT_2")
        self.actionAIRLINE = QtWidgets.QAction(MainWindow)
        self.actionAIRLINE.setObjectName("actionAIRLINE")
        self.actionACTUAL_FLIGHT = QtWidgets.QAction(MainWindow)
        self.actionACTUAL_FLIGHT.setObjectName("actionACTUAL_FLIGHT")
        self.actionAIRCRAFT_3 = QtWidgets.QAction(MainWindow)
        self.actionAIRCRAFT_3.setObjectName("actionAIRCRAFT_3")
        self.actionAIRLINE_2 = QtWidgets.QAction(MainWindow)
        self.actionAIRLINE_2.setObjectName("actionAIRLINE_2")
        self.actionAIRLINE_AIRCRAFT = QtWidgets.QAction(MainWindow)
        self.actionAIRLINE_AIRCRAFT.setObjectName("actionAIRLINE_AIRCRAFT")
        self.actionAIRPORT = QtWidgets.QAction(MainWindow)
        self.actionAIRPORT.setObjectName("actionAIRPORT")
        self.actionCOUNTER_AIRLINE = QtWidgets.QAction(MainWindow)
        self.actionCOUNTER_AIRLINE.setObjectName("actionCOUNTER_AIRLINE")

        self.actionSCHEDULED = QtWidgets.QAction(MainWindow)
        self.actionSCHEDULED.setObjectName("actionSCHEDULED")

        self.actionDelete_a_record = QtWidgets.QAction(MainWindow)
        self.actionDelete_a_record.setObjectName("actionDelete_a_record")
        self.actionUpdate_an_existing_record = QtWidgets.QAction(MainWindow)
        self.actionUpdate_an_existing_record.setObjectName("actionUpdate_an_existing_record")
        self.actionACTUAL_FLIGHT_2 = QtWidgets.QAction(MainWindow)
        self.actionACTUAL_FLIGHT_2.setObjectName("actionACTUAL_FLIGHT_2")
        self.actionAIRCRAFT_4 = QtWidgets.QAction(MainWindow)
        self.actionAIRCRAFT_4.setObjectName("actionAIRCRAFT_4")
        self.actionAIRLINE_3 = QtWidgets.QAction(MainWindow)
        self.actionAIRLINE_3.setObjectName("actionAIRLINE_3")
        self.actionSCHEDULED_FLIGHT = QtWidgets.QAction(MainWindow)
        self.actionSCHEDULED_FLIGHT.setObjectName("actionSCHEDULED_FLIGHT")
        self.actionGATE_2 = QtWidgets.QAction(MainWindow)
        self.actionGATE_2.setObjectName("actionGATE_2")
        self.actionInsert_a_record_2 = QtWidgets.QAction(MainWindow)
        self.actionInsert_a_record_2.setObjectName("actionInsert_a_record_2")
        self.actionUpdate_a_record = QtWidgets.QAction(MainWindow)
        self.actionUpdate_a_record.setObjectName("actionUpdate_a_record")
        self.actionDelete_a_record_2 = QtWidgets.QAction(MainWindow)
        self.actionDelete_a_record_2.setObjectName("actionDelete_a_record_2")
        self.actionInsert_a_record_3 = QtWidgets.QAction(MainWindow)
        self.actionInsert_a_record_3.setObjectName("actionInsert_a_record_3")
        self.actionUpdate_a_record_2 = QtWidgets.QAction(MainWindow)
        self.actionUpdate_a_record_2.setObjectName("actionUpdate_a_record_2")
        self.actionDelete_a_record_3 = QtWidgets.QAction(MainWindow)
        self.actionDelete_a_record_3.setObjectName("actionDelete_a_record_3")
        self.actionInsert_a_record_4 = QtWidgets.QAction(MainWindow)
        self.actionInsert_a_record_4.setObjectName("actionInsert_a_record_4")
        self.actionUpdate_a_record_3 = QtWidgets.QAction(MainWindow)
        self.actionUpdate_a_record_3.setObjectName("actionUpdate_a_record_3")
        self.actionDelete_a_record_4 = QtWidgets.QAction(MainWindow)
        self.actionDelete_a_record_4.setObjectName("actionDelete_a_record_4")
        self.actionInsert_a_record_5 = QtWidgets.QAction(MainWindow)
        self.actionInsert_a_record_5.setObjectName("actionInsert_a_record_5")
        self.actionUpdate_a_record_4 = QtWidgets.QAction(MainWindow)
        self.actionUpdate_a_record_4.setObjectName("actionUpdate_a_record_4")
        self.actionDelete_a_record_5 = QtWidgets.QAction(MainWindow)
        self.actionDelete_a_record_5.setObjectName("actionDelete_a_record_5")
        self.actionInsert_a_record_6 = QtWidgets.QAction(MainWindow)
        self.actionInsert_a_record_6.setObjectName("actionInsert_a_record_6")
        self.actionUpdate_a_record_5 = QtWidgets.QAction(MainWindow)
        self.actionUpdate_a_record_5.setObjectName("actionUpdate_a_record_5")
        self.actionDelete_a_record_6 = QtWidgets.QAction(MainWindow)
        self.actionDelete_a_record_6.setObjectName("actionDelete_a_record_6")
        self.actionInsert_a_record_7 = QtWidgets.QAction(MainWindow)
        self.actionInsert_a_record_7.setObjectName("actionInsert_a_record_7")
        self.actionUpdate_a_record_6 = QtWidgets.QAction(MainWindow)
        self.actionUpdate_a_record_6.setObjectName("actionUpdate_a_record_6")
        self.actionDelete_a_record_7 = QtWidgets.QAction(MainWindow)
        self.actionDelete_a_record_7.setObjectName("actionDelete_a_record_7")
        self.actionFLIGHT_2 = QtWidgets.QAction(MainWindow)
        self.actionFLIGHT_2.setObjectName("actionFLIGHT_2")
        self.actionAIRCRAFT_6 = QtWidgets.QAction(MainWindow)
        self.actionAIRCRAFT_6.setObjectName("actionAIRCRAFT_6")
        self.actionAIRLINE_5 = QtWidgets.QAction(MainWindow)
        self.actionAIRLINE_5.setObjectName("actionAIRLINE_5")
        self.actionSCHEDULED_FLIGHT_3 = QtWidgets.QAction(MainWindow)
        self.actionSCHEDULED_FLIGHT_3.setObjectName("actionSCHEDULED_FLIGHT_3")
        self.actionFLIGHT_3 = QtWidgets.QAction(MainWindow)
        self.actionFLIGHT_3.setObjectName("actionFLIGHT_3")
        self.actionGATE_4 = QtWidgets.QAction(MainWindow)
        self.actionGATE_4.setObjectName("actionGATE_4")


        self.menuEdit.addAction(self.actionAIRCRAFT_6)
        self.menuEdit.addAction(self.actionAIRLINE_5)
        self.menuEdit.addAction(self.actionSCHEDULED_FLIGHT_3)
        self.menuEdit.addAction(self.actionFLIGHT_3)


        
        self.menubar.addAction(self.menuHome.menuAction())
        self.menubar.addAction(self.menuFlights.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())


        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(80, 250, 1300, 531))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        MainWindow.setCentralWidget(self.centralwidget)

        self.DEPARTURES = QtWidgets.QPushButton(self.centralwidget)
        self.DEPARTURES.setGeometry(QtCore.QRect(440, 90, 281, 81))
        self.DEPARTURES.setObjectName("DEPARTURES")
        self.DEPARTURES.setFont(QtGui.QFont('Arial', 14))


        self.ARRIVALS = QtWidgets.QPushButton(self.centralwidget)
        self.ARRIVALS.setGeometry(QtCore.QRect(780, 90, 261, 81))
        self.ARRIVALS.setObjectName("ARRIVALS")
        self.ARRIVALS.setFont(QtGui.QFont('Arial', 14))

        self.airport = QtWidgets.QComboBox(self.centralwidget)
        self.airport.setGeometry(QtCore.QRect(690, 200, 155, 41))
        self.airport.setObjectName("comboBox")
        self.airport.addItem("")
        self.font = self.airport.font()
        self.font.setPointSize(12)
        self.airport.setFont(self.font)


        sql = "select Origin_Airport, Destination_Airport from SCHEDULED_FLIGHT"
        airports = self.database.executeSQL(sql)
        airs = []
        for i in range(len(airports)):
                for j in range(len(airports[0])):
                    airs.append(str(airports[i][j]))
        airs = list( dict.fromkeys(airs) )
        airs.sort()
        airs.remove('LAX')
        for i in airs:
            self.airport.addItem(i)


        self.airlines = QtWidgets.QComboBox(self.centralwidget)
        self.airlines.setGeometry(QtCore.QRect(880, 200, 175, 41))
        self.airlines.setFont(self.font)
        self.airlines.setObjectName("airlines")
        self.airlines.addItem("")
        
        sql = "select name from AIRLINE"
        airlines = self.database.executeSQL(sql)
        airs = []
        for i in range(len(airlines)):
                for j in range(len(airlines[0])):
                    airs.append(str(airlines[i][j]))
        airs = list( dict.fromkeys(airs) )
        airs.sort()
        for i in airs:
            self.airlines.addItem(i)


        self.search_label = QtWidgets.QLabel(self.centralwidget)
        self.search_label.setGeometry(QtCore.QRect(330, 200, 189, 41))
        self.search_label.setObjectName("label")
        self.search_label.setFont(self.font)

        self.flight_number = QtWidgets.QLineEdit(self.centralwidget)
        self.flight_number.setGeometry(QtCore.QRect(530, 200, 113, 41))
        self.flight_number.setText("")
        self.flight_number.setObjectName("lineEdit")
        self.flight_number.setFont(self.font)
        self.error_dialog = QtWidgets.QErrorMessage()
        self.tableWidget.hide()
        self.results.hide()
        self.action.hide()
        self.cb.hide()
        self.DEPARTURES.hide()
        self.ARRIVALS.hide()
        self.airport.hide()
        self.airlines.hide()
        self.search_label.hide()
        self.flight_number.hide()

        self.label20 = QtWidgets.QLabel(MainWindow)
        self.pixmap = QtGui.QPixmap('plane.png')
        self.label20.setPixmap(self.pixmap)
 
        self.label20.setGeometry(QtCore.QRect(220, 220, self.pixmap.width(), self.pixmap.height()))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

 
        #Σύνδεση των events των διαφόρων widgets του gui με μεθόδους
        self.actionAIRCRAFT_6.triggered.connect(lambda: self.table_clicked("AIRCRAFT"))
        self.actionAIRLINE_5.triggered.connect(lambda: self.table_clicked("AIRLINE"))
        self.actionSCHEDULED_FLIGHT_3.triggered.connect(lambda: self.table_clicked("SCHEDULED_FLIGHT"))
        self.actionFLIGHT_3.triggered.connect(lambda: self.table_clicked("ACTUAL_FLIGHT"))

        self.cb.activated.connect(self.combo_box_clicked)
        self.menuHome.aboutToShow.connect(self.showHome)
        self.menuFlights.aboutToShow.connect(self.showFlights)

        self.DEPARTURES.clicked.connect(lambda: self.departures_arrivals_clicked("DEPARTURES"))
        self.ARRIVALS.clicked.connect(lambda: self.departures_arrivals_clicked("ARRIVALS"))
        self.airlines.activated.connect(self.Airline_Clicked)
        self.airport.activated.connect(self.Airport_Clicked)
        self.flight_number.returnPressed.connect(self.Select_Fnumber)
        self.error_dialog.setWindowTitle("Error")


    #1η καρτέλα Home
    def showHome(self):
        self.wecolme_label.show()
        self.label20.show()
        if (self.results.isVisible()):
            self.results.hide()
        if (self.action.isVisible()):
            self.action.hide()
        if (self.cb.isVisible()):
            self.cb.hide()
        if (self.DEPARTURES.isVisible()):
            self.DEPARTURES.hide()
        if (self.ARRIVALS.isVisible()):
            self.ARRIVALS.hide()
        if (self.airport.isVisible()):
            self.airport.hide()

        if (self.airlines.isVisible()):
            self.airlines.hide()
        if (self.search_label.isVisible()):
            self.search_label.hide()
        if (self.flight_number.isVisible()):
            self.flight_number.hide()

        if (self.tableWidget.isVisible()):
            self.tableWidget.hide()


    #2η καρτέλα Flights
    def showFlights(self):
        self.DEPARTURES.show()
        self.ARRIVALS.show()
        self.wecolme_label.show()
        self.airport.show()
        self.airlines.show()
        self.search_label.show()
        self.flight_number.show()
        
        if (self.results.isVisible()):
            self.results.hide()
            
        if (self.action.isVisible()):
            self.action.hide()
            
        if (self.cb.isVisible()):
            self.cb.hide()
            
        if (self.label20.isVisible()):
            self.label20.hide()


    #Αναφέρεται στο combobox της 3ης καρτέλας Edit
    def combo_box_clicked(self):
        if (self.aircraft_clicked or self.airline_clicked or self.scheduled_flight or self.gate_clicked or self.counter_clicked
            or self.flight_clicked):
            if (self.aircraft_clicked): 
                if (self.cb.currentText() == "Insert a record"):
                    self.open_insert_aircraft_window()
                    self.insert_aircraft_ui.final_submit.clicked.connect(lambda: self.insert_into_table("AIRCRAFT"))
                if (self.cb.currentText() == "Delete an existing record"):
                    self.open_delete_aircraft_window()
                    self.delete_aircraft_ui.aircraft_done.clicked.connect(lambda: self.delete_from_table("AIRCRAFT"))

            if (self.airline_clicked):
                if (self.cb.currentText() == "Update a record"):
                    self.open_update_airline_window()
                    self.update_airline_ui.pushButton.clicked.connect(self.update_airline)

                if (self.cb.currentText() == "Insert a record"):
                    self.open_insert_airline_window()
                    self.insert_airline_ui.submit_airline.clicked.connect(lambda: self.insert_into_table("AIRLINE"))
                    
                if (self.cb.currentText() == "Delete an existing record"):
                    self.open_delete_airline_window()
                    self.delete_airline_ui.aircraft_done.clicked.connect(lambda: self.delete_from_table("AIRLINE"))

            if (self.scheduled_flight):
                if (self.cb.currentText() == "Update a record"):
                    self.open_update_scheduled_flight_window()
                    self.update_scheduled_flight_ui.update_scheduled.clicked.connect(self.update_scheduled_flight)
                    
                if (self.cb.currentText() == "Insert a record"):
                    self.open_insert_scheduled_flight_window()
                    self.insert_scheduled_flight_ui.submit.clicked.connect(lambda: self.insert_into_table("SCHEDULED_FLIGHT"))

                if (self.cb.currentText() == "Delete an existing record"):
                    self.open_delete_scheduled_flight_window()
                    self.delete_scheduled_flight_ui.aircraft_done.clicked.connect(lambda: self.delete_from_table("SCHEDULED_FLIGHT"))

            if (self.flight_clicked):
                if (self.cb.currentText() == "Update a record"):
                    self.open_update_flight_window()
                    self.update_flight_ui.update.clicked.connect(self.update_flight)


    #The following methods refer to the insert, update, delete functions of the 3rd tab
    #Depending on the user input, the various widgets create the appropriate SQL commands and executes them
    def update_flight(self):
        flight_num =  self.update_flight_ui.flight_number.currentText()
        sql = "select * from ACTUAL_FLIGHT where Flight_Number = ?"
        results = self.database.executeSQLparam(sql,(flight_num,))
        status = self.update_flight_ui.status.currentText()
        departure = results[0].get('Departure')
        arrival = results[0].get('Arrival')
        old_delay = results[0].get('Delay')
        
        sql = "select Duration from ACTUAL_FLIGHT join SCHEDULED_FLIGHT on FlightNumber = Scheduled_Flight_Number where Flight_Number = ?"
        results = self.database.executeSQLparam(sql,(flight_num,))
        duration = results[0].get('Duration')


    
        new_delay = self.update_flight_ui.delay.time().toString()
        new_delay = new_delay[:5]            
        
        old_dep = datetime.datetime(2021,1,1,int(departure[:2]),int(departure[3:5]),00)
        new_dep_time = old_dep + datetime.timedelta(hours = int(new_delay[:2]) , minutes = int(new_delay[3:]))

        old_arr = datetime.datetime(2021,1,1,int(arrival[:2]),int(arrival[3:5]),00)
        arrival_time = old_arr + datetime.timedelta(hours = int(new_delay[:2]) , minutes = int(new_delay[3:]))

        new_dep_time = str(new_dep_time.time())[:5]
        arrival_time = str(arrival_time.time())[:5]

        #print(new_dep_time , arrival_time)

        old_delay = datetime.datetime(2021,1,1,int(old_delay[:2]),int(old_delay[3:5]),00)
        new_delay = str((old_delay + datetime.timedelta(hours = int(new_delay[:2]) , minutes = int(new_delay[3:]))).time())[:5]

        if (status == "Departures_Soon" or status == "Departed"):
            sql = "update ACTUAL_FLIGHT set Departure = ? , Arrival = ? , Delay = ? , Gate = ? , Status = ? where Flight_Number = ? "
            t = (new_dep_time , arrival_time , new_delay , self.update_flight_ui.gate.currentText() , status , flight_num)
            self.database.executeSQLparam(sql,t)
            self.table_clicked("ACTUAL_FLIGHT")

        elif (status == "Cancelled") :
            sql = "update ACTUAL_FLIGHT set Departure = null , Arrival = null , Delay = null , Gate = null , Status = 'Cancelled' where Flight_Number = ?"
            self.database.executeSQLparam(sql , (flight_num , ))
            self.table_clicked("ACTUAL_FLIGHT")

        else :
            sql = "update ACTUAL_FLIGHT set Departure = ? , Arrival = ? , Delay = ? , Status = ? where Flight_Number = ? "
            t = (new_dep_time , arrival_time , new_delay , status , flight_num)
            self.database.executeSQLparam(sql , t)
            self.table_clicked("ACTUAL_FLIGHT")

       
                

    def update_scheduled_flight(self):
        if (self.update_scheduled_flight_ui.valid_until.text()):
            sql = "update SCHEDULED_FLIGHT set Valid_Until = ? where FlightNumber = ?"
            t = (self.update_scheduled_flight_ui.valid_until.text() , self.update_scheduled_flight_ui.flight_number.currentText())
            self.database.executeSQLparam(sql,t)
            self.table_clicked("SCHEDULED_FLIGHT")

        if (self.update_scheduled_flight_ui.days.text()):
            sql = "update SCHEDULED_FLIGHT set Days = ? where FlightNumber = ?"
            t = (self.update_scheduled_flight_ui.days.text() , self.update_scheduled_flight_ui.flight_number.currentText())
            self.database.executeSQLparam(sql,t)
            self.table_clicked("SCHEDULED_FLIGHT")

        if(self.update_scheduled_flight_ui.update_departure_time_cb.currentText() == "Update departure time"):
            departure_time = self.update_scheduled_flight_ui.update_departure_time.time().toString()
            departure_time_hours = departure_time[:2]
            departure_time_minutes = departure_time[3:5]
            departure_time = departure_time_hours + ":" + departure_time_minutes

            
            dep_date = datetime.datetime(2021,1,1,int(departure_time_hours),int(departure_time_minutes),00)

            sql_dur = "select Duration from SCHEDULED_FLIGHT where FlightNumber = ?"
            duration = self.database.executeSQLparam(sql_dur,(self.update_scheduled_flight_ui.flight_number.currentText(),))
            duration = duration[0]
            duration = duration['Duration']
            duration_hours = int(duration[:2])
            duration_minutes = int(duration[3:])

            arr_time = str((dep_date + datetime.timedelta(hours = duration_hours , minutes = duration_minutes)).time())[:5]
            
            sql = "update SCHEDULED_FLIGHT set Departure = ? , Arrival = ? where FlightNumber = ?"
            t = (departure_time, arr_time , self.update_scheduled_flight_ui.flight_number.currentText())
            self.database.executeSQLparam(sql,t)
            self.table_clicked("SCHEDULED_FLIGHT")
               


    def update_airline(self):
        new_value = self.update_airline_ui.comboBox.currentText()
        airline_id = self.update_airline_ui.airline_id.currentText()
        sql = "update AIRLINE set Active = ? where airline_id = ?"
        t = (new_value,airline_id)
        self.database.executeSQLparam(sql,t)
        self.table_clicked("AIRLINE")

        
    def insert_into_table(self,table):
        if (table == "AIRCRAFT"):
            mydict = {'ID': self.insert_aircraft_ui.ID.text() , 'Name': self.insert_aircraft_ui.Name.text() , 'Capacity': self.insert_aircraft_ui.Capacity.text() ,
                    'ICAO': self.insert_aircraft_ui.ICAO.text() , 'IATA' : self.insert_aircraft_ui.IATA.text()}
        
            self.database._insertIntoTable(table,mydict)
            self.table_clicked("AIRCRAFT")
        elif (table == "AIRLINE"):
            if (self.insert_airline_ui.active.currentText() == "Y") :
                active = "Y"
            else :
                active = "N"
            mydict = {'airline_id': self.insert_airline_ui.airline_id.text() , 'name': self.insert_airline_ui.airline_name.text(), 'IATA': self.insert_airline_ui.airline_iata.text() ,
                    'ICAO': self.insert_airline_ui.airline_icao.text() , 'country' : self.insert_airline_ui.airline_country.text() , 'active' : active}
            self.database._insertIntoTable(table,mydict)
            self.table_clicked("AIRLINE")
            
        elif (table == "SCHEDULED_FLIGHT"):
            departure_time = self.insert_scheduled_flight_ui.departure.time().toString()
            departure1 = departure_time[:2]
            departure2 = departure_time[3:5]
            departure_time = departure1 + ":" + departure2
            

            duration = self.insert_scheduled_flight_ui.duration.time().toString()
            duration1 = duration[:2]
            duration2 = duration[3:5]
            duration = duration1 + ":" + duration2

            dep_date = datetime.datetime(2021,1,1,int(departure1),int(departure2),00)
            arr_time = str((dep_date + datetime.timedelta(hours = int(duration1) , minutes = int(duration2))).time())[:5]

            mydict = {'FlightNumber': self.insert_scheduled_flight_ui.flight_number.text() ,
                      'Origin_Airport' : self.insert_scheduled_flight_ui.origin_airport.currentText() ,
                      'Destination_Airport' : self.insert_scheduled_flight_ui.destination_airport.currentText() ,
                      'Valid_From' : self.insert_scheduled_flight_ui.valid_from.text() ,
                      'Valid_Until' : self.insert_scheduled_flight_ui.valid_until.text() ,
                      'Days' : self.insert_scheduled_flight_ui.days.text() ,
                      'Departure' : departure_time ,
                      'Arrival' : arr_time ,
                      'Aircraft' : self.insert_scheduled_flight_ui.aircraft.currentText() ,
                      'Airline_id' : self.insert_scheduled_flight_ui.airline_id.currentText() ,
                      'Duration' : duration }
            
            self.database._insertIntoTable(table,mydict)
            self.table_clicked("SCHEDULED_FLIGHT")


            
    def delete_from_table(self,table,):
        if(table == "AIRCRAFT"):
            if (self.delete_aircraft_ui.comboBox.isEnabled()) :
                sql = 'Delete from AIRCRAFT where ID =?'
                t = (self.delete_aircraft_ui.comboBox.currentText(),)
                self.database.executeSQLparam(sql,t)

            if (self.delete_aircraft_ui.comboBox_2.isEnabled()):
                sql = 'Delete from AIRCRAFT where Name =?'
                t = (self.delete_aircraft_ui.comboBox_2.currentText(),)
                self.database.executeSQLparam(sql,t)
                
            if (self.delete_aircraft_ui.comboBox_3.isEnabled()):
                sql = 'Delete from AIRCRAFT where ICAO =?'
                t = (self.delete_aircraft_ui.comboBox_3.currentText(),)
                self.database.executeSQLparam(sql,t)
            if (self.delete_aircraft_ui.comboBox_4.isEnabled()):
                sql = 'Delete from AIRCRAFT where IATA =?'
                t = (self.delete_aircraft_ui.comboBox_4.currentText(),)
                self.database.executeSQLparam(sql,t)
            self.table_clicked("AIRCRAFT")


        if (table == "AIRLINE"):
            if(self.delete_airline_ui.comboBox.isEnabled()):
                sql = 'Delete from AIRLINE where airline_id =?'
                t = (self.delete_airline_ui.comboBox.currentText(),)
                self.database.executeSQLparam(sql,t)
                
            if(self.delete_airline_ui.comboBox_2.isEnabled()):
                sql = 'Delete from AIRLINE where name =?'
                t = (self.delete_airline_ui.comboBox_2.currentText(),)
                self.database.executeSQLparam(sql,t)
                
            if(self.delete_airline_ui.comboBox_3.isEnabled()):
                sql = 'Delete from AIRLINE where ICAO =?'
                t = (self.delete_airline_ui.comboBox_3.currentText(),)
                self.database.executeSQLparam(sql,t)
                
            if(self.delete_airline_ui.comboBox_4.isEnabled()):
                sql = 'Delete from AIRLINE where IATA =?'
                t = (self.delete_airline_ui.comboBox_4.currentText(),)
                self.database.executeSQLparam(sql,t)
            self.table_clicked("AIRLINE")

        if (table == "SCHEDULED_FLIGHT"):
            sql = 'Delete from SCHEDULED_FLIGHT where FlightNumber =?'
            t = (self.delete_scheduled_flight_ui.flight_number.currentText(),)
            self.database.executeSQLparam(sql,t) 
            self.table_clicked("SCHEDULED_FLIGHT")
     
    


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.wecolme_label.setText(_translate("MainWindow", "WELCOME TO LAX AIRPORT!"))
        self.action.setText(_translate("MainWindow", "Action"))
        self.cb.setItemText(0, _translate("MainWindow", "Update a record"))
        self.cb.setItemText(1, _translate("MainWindow", "Insert a record"))
        self.cb.setItemText(2, _translate("MainWindow", "Delete an existing record"))
        self.menuHome.setTitle(_translate("MainWindow", "Home"))
        self.menuFlights.setTitle(_translate("MainWindow", "Flights"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))


        self.actionAIRCRAFT.setText(_translate("MainWindow", "ACTUAL_FLIGHT"))
        self.actionAIRCRAFT_2.setText(_translate("MainWindow", "AIRCRAFT"))
        self.actionAIRLINE.setText(_translate("MainWindow", "AIRLINE"))
        self.actionACTUAL_FLIGHT.setText(_translate("MainWindow", "ACTUAL_FLIGHT"))
        self.actionAIRCRAFT_3.setText(_translate("MainWindow", "AIRCRAFT"))
        self.actionAIRLINE_2.setText(_translate("MainWindow", "AIRLINE"))
        self.actionAIRLINE_AIRCRAFT.setText(_translate("MainWindow", "AIRLINE_AIRCRAFT"))
        self.actionAIRPORT.setText(_translate("MainWindow", "AIRPORT"))
        self.actionCOUNTER_AIRLINE.setText(_translate("MainWindow", "COUNTER_AIRLINE"))
        self.actionSCHEDULED.setText(_translate("MainWindow", "SCHEDULED"))

        self.actionDelete_a_record.setText(_translate("MainWindow", "Delete a record"))
        self.actionUpdate_an_existing_record.setText(_translate("MainWindow", "Update an existing record"))
        self.actionACTUAL_FLIGHT_2.setText(_translate("MainWindow", "ACTUAL_FLIGHT"))
        self.actionAIRCRAFT_4.setText(_translate("MainWindow", "AIRCRAFT"))
        self.actionAIRLINE_3.setText(_translate("MainWindow", "AIRLINE"))
        self.actionSCHEDULED_FLIGHT.setText(_translate("MainWindow", "SCHEDULED_FLIGHT"))
        self.actionInsert_a_record_2.setText(_translate("MainWindow", "Insert a record"))
        self.actionUpdate_a_record.setText(_translate("MainWindow", "Update a record"))
        self.actionDelete_a_record_2.setText(_translate("MainWindow", "Delete a record"))
        self.actionInsert_a_record_3.setText(_translate("MainWindow", "Insert a record"))
        self.actionUpdate_a_record_2.setText(_translate("MainWindow", "Update a record"))
        self.actionDelete_a_record_3.setText(_translate("MainWindow", "Delete a record"))
        self.actionInsert_a_record_4.setText(_translate("MainWindow", "Insert a record"))
        self.actionUpdate_a_record_3.setText(_translate("MainWindow", "Update a record"))
        self.actionDelete_a_record_4.setText(_translate("MainWindow", "Delete a record"))
        self.actionInsert_a_record_5.setText(_translate("MainWindow", "Insert a record"))
        self.actionUpdate_a_record_4.setText(_translate("MainWindow", "Update a  record"))
        self.actionDelete_a_record_5.setText(_translate("MainWindow", "Delete a record"))
        self.actionInsert_a_record_6.setText(_translate("MainWindow", "Insert a record"))
        self.actionUpdate_a_record_5.setText(_translate("MainWindow", "Update a record"))
        self.actionDelete_a_record_6.setText(_translate("MainWindow", "Delete a record"))
        self.actionInsert_a_record_7.setText(_translate("MainWindow", "Insert a record"))
        self.actionUpdate_a_record_6.setText(_translate("MainWindow", "Update a record"))
        self.actionDelete_a_record_7.setText(_translate("MainWindow", "Delete a record"))
        self.actionFLIGHT_2.setText(_translate("MainWindow", "FLIGHT"))
        self.actionAIRCRAFT_6.setText(_translate("MainWindow", "AIRCRAFT"))
        self.actionAIRLINE_5.setText(_translate("MainWindow", "AIRLINE"))
        self.actionSCHEDULED_FLIGHT_3.setText(_translate("MainWindow", "SCHEDULED_FLIGHT"))
        self.actionFLIGHT_3.setText(_translate("MainWindow", "FLIGHT"))

        self.DEPARTURES.setText(_translate("MainWindow", "DEPARTURES"))
        self.ARRIVALS.setText(_translate("MainWindow", "ARRIVALS"))
        self.airport.setItemText(0, _translate("MainWindow", "All Airports"))
        self.airlines.setItemText(0, _translate("MainWindow", "All Airlines"))
        self.search_label.setText(_translate("MainWindow", "Select Flight Number:"))



    #Κλικ σε κάποιον από τους πίνακες του υπομενού Edit 
    def table_clicked(self,table):
        if (self.wecolme_label.isVisible()):
            self.wecolme_label.hide()
        if (self.label20.isVisible()):
            self.label20.hide()

        if (self.DEPARTURES.isVisible()):
            self.DEPARTURES.hide()

        if (self.ARRIVALS.isVisible()):
            self.ARRIVALS.hide()

        if (self.airport.isVisible()):
            self.airport.hide()

        if (self.airlines.isVisible()):
            self.airlines.hide()

        if (self.search_label.isVisible()):
            self.search_label.hide()
            
        if (self.flight_number.isVisible()):
            self.flight_number.hide()

        if (self.tableWidget.isVisible()):
            self.tableWidget.hide()
            
        self.action.show()
        self.cb.show()
        
        if (table == "AIRCRAFT"):
            self.aircraft_clicked = True
            self.airline_clicked = False
            self.scheduled_flight = False
            self.gate_clicked = False
            self.counter_clicked = False
            self.flight_clicked = False

        if (table == "AIRLINE"):
            self.aircraft_clicked = False
            self.airline_clicked = True
            self.scheduled_flight = False
            self.gate_clicked = False
            self.counter_clicked = False
            self.flight_clicked = False

        if (table == "SCHEDULED_FLIGHT"):
            self.aircraft_clicked = False
            self.airline_clicked = False
            self.scheduled_flight = True
            self.gate_clicked = False
            self.counter_clicked = False
            self.flight_clicked = False

        
                
        if (table == "COUNTER"):
            self.aircraft_clicked = False
            self.airline_clicked = False
            self.scheduled_flight = False
            self.gate_clicked = False
            self.counter_clicked = True
            self.flight_clicked = False
            
        if (table == "ACTUAL_FLIGHT"):
            self.aircraft_clicked = False
            self.airline_clicked = False
            self.scheduled_flight = False
            self.gate_clicked = False
            self.counter_clicked = False
            self.flight_clicked = True
        
        sql = f"select * from {table}"
       
        results = self.database.executeSQL(sql)

        self.results.setRowCount(len(results))
        self.results.setColumnCount(len(results[0]))
    
        column_names = self.database.getColumnNamesOfTable(f"{table}")
        self.results.setHorizontalHeaderLabels(column_names)
        for i in range(len(results)):
            for j in range(len(results[0])):
                self.results.setItem(i,j,QtWidgets.QTableWidgetItem(str(results[i][j])))
        self.results.show()
     
    #Creation and execution of Departures, Arrivals Queries
    def execute_table_query(self):
        #Query that returns the Departures table for the day 2021-01-04
        dep_query = f'''SELECT AIRPORT.City, Flight.Destination_Airport, AIRLINE.NAME as Airline_Name, Flight_Number, Gate, group_concat(counter_id,' ') as Check_in,
        datetime(ACTUAL_FLIGHT.date, SCHEDULED.Departure) as Date_scheduled_time, time(ACTUAL_FLIGHT.Departure) as Actual_or_Estimated_Departure, Flight.Status
        
        FROM  (ACTUAL_FLIGHT JOIN SCHEDULED_FLIGHT AS SCHEDULED on Scheduled_Flight_Number=FlightNumber) as Flight, AIRPORT, COUNTER_AIRLINE, AIRLINE
        
        WHERE  Flight.Destination_Airport<>"LAX" and Flight.DATE = date("2022-01-04") and Flight.Destination_Airport=AIRPORT.IATA and Flight.airline_id=AIRLINE.airline_id
        and COUNTER_AIRLINE.airline_id=AIRLINE.airline_id
        and Flight.Destination_Airport LIKE "{self.options["airport"]}" and AIRLINE_NAME LIKE "{self.options["airline"]}" and Flight_Number {self.options["flight_number"]}
        group by Flight_Number
        order by Date_scheduled_time;'''
        
        #Query that returns the Arrivals table for the day 2021-01-04
        arr_query = f'''SELECT AIRPORT.City, Flight.Origin_Airport, AIRLINE.NAME as Airline_Name, Flight_Number, datetime(ACTUAL_FLIGHT.date, SCHEDULED.Arrival) as Date_scheduled_time,
        time(ACTUAL_FLIGHT.Arrival) as Actual_or_Estimated_Arrival, Flight.Status
        FROM  (ACTUAL_FLIGHT JOIN SCHEDULED_FLIGHT as SCHEDULED on Scheduled_Flight_Number=FlightNumber) as Flight, AIRPORT, AIRLINE
        where  Flight.Origin_Airport<>"LAX" and Flight.DATE = date("2022-01-04") and Flight.Origin_Airport=AIRPORT.IATA and Flight.airline_id=AIRLINE.airline_id
        and Flight.Origin_Airport LIKE "{self.options["airport"]}" and AIRLINE_NAME LIKE "{self.options["airline"]}" and Flight_Number {self.options["flight_number"]}
        group by Flight_Number
        order by Date_scheduled_time;'''


        sql = dep_query if self.options["type"] == "DEPARTURES" else arr_query
        #print(sql)
        
        query_res = self.database.executeSQLdict(sql)

        return query_res
    

    #Updating tableWidget records in the Flights tab           
    def departures_arrivals_clicked(self,table):
        if (table == "DEPARTURES"):
            self.options["type"] = "DEPARTURES"
        else :
            self.options["type"] = "ARRIVALS"

        query_res = self.execute_table_query()
        if (query_res==[]):
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
        else:
            self.AddTable(query_res)
            
    #Updating tableWidget records in the Flights tab
    def Airline_Clicked(self):
        
        content = self.airlines.currentText()
        self.options["airline"] = content if content != "All Airlines" else "%"
        
        query_res = self.execute_table_query()
        if query_res==[]:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
        else:
            self.AddTable(query_res)

    #Updating tableWidget records in the Flights tab            
    def Airport_Clicked(self):
        
        content = self.airport.currentText()
        self.options["airport"] = content if content != "All Airports" else "%"
        
        query_res = self.execute_table_query()
        if query_res==[]:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
        else:
            self.AddTable(query_res)

    #Show Error Message
    def Error_Pop(self):
        error_dialog = QtWidgets.QErrorMessage()

    #Updating tableWidget records in the Flights tab     
    def Select_Fnumber(self):
        content = self.flight_number.text()
        try:
            if (content != ""):
                self.options["flight_number"] = f" = {int(content)}"
            else:
                self.options["flight_number"] = f" > 0"

            query_res = self.execute_table_query()
        
            if query_res==[]:
                self.tableWidget.setRowCount(0)
                self.tableWidget.setColumnCount(0)
            else:
                self.AddTable(query_res)
                
        #If the user enters an incorrect character, display an error message
        except BaseException:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            
            self.error_dialog.showMessage("Oops!  That was no valid number.  Try again...")
            
                    
   
    #Updating the QTableWidget with the Queries values
    def AddTable(self, query):
        row_count = (len(query))
        column_count = (len(query[0]))

        self.tableWidget.setColumnCount(column_count)
        self.tableWidget.setRowCount(row_count)

        self.tableWidget.setHorizontalHeaderLabels((list(query[0].keys())))

        for row in range(row_count):  # add items from array to QTableWidget
            for column in range(column_count):

                item = (list(query[row].values())[column])
                itemm = QtWidgets.QTableWidgetItem(str(item))
                self.tableWidget.setItem(row, column, itemm)
                
        self.resizeColumns()
        self.tableWidget.show()

    def resizeColumns(self):
        columnCount = self.tableWidget.columnCount()
        header = self.tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)


        for i in range(1,int(columnCount)):
            header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

            

class DataModel():
    '''Database connection and cursor creation class'''
    def __init__(self, filename):
        self.filename = filename
        
        try:
            self.con = sqlite3.connect(filename,check_same_thread=False)
            self.con.row_factory = sqlite3.Row  # so that we can get the names of the table columns
            self.cursor = self.con.cursor()
            print("Successful connection to the database", filename)
            sqlite_select_Query = "select sqlite_version();"
            self.cursor.execute(sqlite_select_Query)
            record = self.cursor.fetchall()

            for rec in record:
                print("SQLite Database Version is: ", rec[0])
        except sqlite3.Error as error:
            print("Error connecting to sqlite database", error)
    
    def close(self):
        self.con.commit()
        self.con.close()

    
    #Execute a SQL query that returns results in a list
    def executeSQL(self, query):
        try:
            t1 = time.perf_counter()
            for statement in query.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)


                    sql_time = time.perf_counter() - t1
                    #print(f'εκτέλεση εντολής {statement[:40]}... σε {sql_time:.5f} sec')
                    print("The SQL command was executed successfully.")
                results = []

            #epistrefoume ta results
            results =self.cursor.fetchall()
            self.con.commit()
            return results
              
                    
        except sqlite3.Error as error:
            print(f"SQL command execution error", error)
            return False

    #Execute a SQL query that returns results in a dictionary
    def executeSQLdict(self, query):
        try:
            t1 = time.perf_counter()
            for statement in query.split(";"):
                if statement.strip():
                    self.cursor.execute(statement)
                    sql_time = time.perf_counter() -t1
                    #print(f'εκτέλεση εντολής {statement[:40]}... σε {sql_time:.5f} sec')
                    print("The SQL command was executed successfully.")
            self.con.commit()
            return self.getQueryData()
              
                    
        except sqlite3.Error as error:
            print(f"SQL command execution error", error)
            return False

    
    #Εισαγωγή εγγραφής σε μορφή λεξικού σε πίνακα
    def _insertIntoTable(self, table, row_dict):
        '''Insert a record in dictionary format into a table'''
        try:
            query_param = f"""INSERT INTO {table} ({",".join(row_dict.keys())}) VALUES ({", ".join((len(row_dict)-1) * ["?"])}, ?);"""
            data = tuple(row_dict.values())
            self.cursor.execute(query_param, data)
            self.con.commit()
            print("Import completed.")
            return True
        except sqlite3.Error as error:
            print(f"Error inserting data into the table {table}", error)
            return False

    #Execute a parametric query
    def executeSQLparam(self,query,data):
        try:
            self.cursor.execute(query,data)
            records = self.cursor.fetchall()
            results = []
            for row in records:
                results.append(dict(row))
            self.con.commit()
            print("The SQL command was executed successfully.")
            return results
        
        except sqlite3.Error as error:
            print(f"SQL command execution error", error)
            return False
            


    def getColumnNamesOfTable(self,table):
        self.executeSQL(f"select * from {table}")
        names = list(map(lambda x: x[0], self.cursor.description))
        return names
    
    def getQueryData(self):
        result = []
        columnNames = [column[0] for column in self.cursor.description]
        
        for record in self.cursor.fetchall():
            result.append(dict( zip( columnNames , record ) ) )
        return result
        



if __name__ == "__main__":
    import sys
    dbfile = "LAX_FINAL.db"
    
    d = DataModel(dbfile)     
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()


    ui = Ui_MainWindow(d)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    d.close()
