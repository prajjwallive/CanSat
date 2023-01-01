from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from pyqtgraph import PlotWidget
from packages import Communication, Database
from MapWindow import Ui_MainWindow as MapWindow
import resources_rc, qtawesome as qta, numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QtWidgets.QMainWindow):
        # Configuration
        self.database = Database()
        self.serial_connect = Communication()
        QtGui.QFontDatabase.addApplicationFont('resources/Anurati-Regular.otf')
        QtGui.QFontDatabase.addApplicationFont('resources/Poppins-Regular.ttf')
        
        self.childWindow: QtWidgets.QMainWindow = MapWindow(MainWindow)
                   
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setWindowIcon(QtGui.QIcon(":/assets/icon.png"))
        MainWindow.setStyleSheet("* {font-family: Poppins}\n"
"#changeStateBtn, #closeWindowBtn, #storageBtn, #infoBtn{\n"
"    border-radius: 3px;\n"
"    background-color: rgb(253, 253, 253);\n"
"}\n"
"\n"
"#changeStateBtn:hover, #closeWindowBtn:hover, #infoBtn:hover {\n"
"    background-color: rgba(255, 255, 255, 128);\n"
"}\n"
"\n"
"#storageBtn:hover {\n"
"    background-color: rgba(55, 211, 185, 200);\n"
"}\n"
"\n"
"#changeStateBtn:pressed, #closeWindowBtn:pressed, #infoBtn:pressed {\n"
"    background-color: rgb(55, 211, 185);\n"
"    color: #ffffff;\n"
"}\n"
"\n"
" #storageBtn:pressed {\n"
"    background-color: rgb(253, 253, 253);\n"
"    color: #000;\n"
"}\n"
"\n"
"#storageBtn {\n"
"    background-color: rgb(55, 211, 185);\n"
"    color: #ffffff;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QLabel {\n"
"    font-family: \'Poppins\';\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_layout.setObjectName("title_layout")
        
        self.title_icon = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_icon.sizePolicy().hasHeightForWidth())
        self.title_icon.setSizePolicy(sizePolicy)
        self.title_icon.setMinimumSize(QtCore.QSize(40, 40))
        self.title_icon.setMaximumSize(QtCore.QSize(40, 40))
        self.title_icon.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.title_icon.setText("")
        self.title_icon.setPixmap(QtGui.QPixmap(":/assets/icon.png"))
        self.title_icon.setScaledContents(True)
        self.title_icon.setObjectName("title_icon")
        self.title_layout.addWidget(self.title_icon)
        
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(17)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.title_label.setObjectName("title_label")
        self.title_layout.addWidget(self.title_label)
        self.tools_layout = QtWidgets.QHBoxLayout()
        self.tools_layout.setObjectName("tools_layout")
        
        self.storageBtn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.storageBtn.sizePolicy().hasHeightForWidth())
        self.storageBtn.setSizePolicy(sizePolicy)
        self.storageBtn.setMinimumSize(QtCore.QSize(30, 30))
        self.storageBtn.setMaximumSize(QtCore.QSize(80, 40))
        self.storageBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.storageBtn.setObjectName("storageBtn")
        self.storageBtn.clicked.connect(self.handleStorage)
        self.tools_layout.addWidget(self.storageBtn)
        
        icon: QtGui.QIcon = qta.icon('ei.map-marker')
        self.infoBtn = QtWidgets.QPushButton(icon, '',self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.infoBtn.sizePolicy().hasHeightForWidth())
        self.infoBtn.setSizePolicy(sizePolicy)
        self.infoBtn.setMinimumSize(QtCore.QSize(40, 40))
        self.infoBtn.setMaximumSize(QtCore.QSize(40, 40))
        self.infoBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.infoBtn.setText("")
        self.infoBtn.setObjectName("infoBtn")
        self.infoBtn.clicked.connect(self.viewMap)
        self.tools_layout.addWidget(self.infoBtn)
        
        self.timer = QtCore.QTimer(MainWindow)
        self.timer.timeout.connect(self.updateCommunication)
        self.timer.start(1000)
        
        self.title_layout.addLayout(self.tools_layout)
        self.verticalLayout.addLayout(self.title_layout)
        
        self.dataTitleLayout = QtWidgets.QHBoxLayout()
        self.dataTitleLayout.setObjectName("dataTitleLayout")
        
        self.gps_title_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        self.gps_title_label.setFont(font)
        self.gps_title_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.gps_title_label.setObjectName("gps_title_label")
        self.dataTitleLayout.addWidget(self.gps_title_label)
        
        self.bmp_title_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(11)
        font.setBold(True)
        self.bmp_title_label.setFont(font)
        self.bmp_title_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.bmp_title_label.setObjectName("bmp_title_label")
        self.dataTitleLayout.addWidget(self.bmp_title_label)
        
        self.verticalLayout.addLayout(self.dataTitleLayout)
        
        self.dataValueLayout = QtWidgets.QGridLayout()
        self.dataValueLayout.setObjectName("dataValueLayout")
        self.altitudeBMPLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.altitudeBMPLabel.sizePolicy().hasHeightForWidth())
        self.altitudeBMPLabel.setSizePolicy(sizePolicy)
        self.altitudeBMPLabel.setMinimumSize(QtCore.QSize(170, 0))
        self.altitudeBMPLabel.setMaximumSize(QtCore.QSize(170, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        self.altitudeBMPLabel.setFont(font)
        self.altitudeBMPLabel.setObjectName("altitudeBMPLabel")
        self.dataValueLayout.addWidget(self.altitudeBMPLabel, 2, 3, 1, 1)
        
        self.altitudeGPSLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.altitudeGPSLabel.sizePolicy().hasHeightForWidth())
        self.altitudeGPSLabel.setSizePolicy(sizePolicy)
        self.altitudeGPSLabel.setMinimumSize(QtCore.QSize(130, 0))
        self.altitudeGPSLabel.setMaximumSize(QtCore.QSize(130, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        self.altitudeGPSLabel.setFont(font)
        self.altitudeGPSLabel.setObjectName("altitudeGPSLabel")
        self.dataValueLayout.addWidget(self.altitudeGPSLabel, 0, 0, 1, 1)
        
        self.lattitudeLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lattitudeLabel.sizePolicy().hasHeightForWidth())
        self.lattitudeLabel.setSizePolicy(sizePolicy)
        self.lattitudeLabel.setMinimumSize(QtCore.QSize(93, 0))
        self.lattitudeLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        self.lattitudeLabel.setFont(font)
        self.lattitudeLabel.setObjectName("lattitudeLabel")
        self.dataValueLayout.addWidget(self.lattitudeLabel, 1, 0, 1, 1)
        
        self.pressureValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.pressureValueLabel.setObjectName("pressureValueLabel")
        self.dataValueLayout.addWidget(self.pressureValueLabel, 0, 4, 1, 1)
        
        self.temperatureLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.temperatureLabel.sizePolicy().hasHeightForWidth())
        self.temperatureLabel.setSizePolicy(sizePolicy)
        self.temperatureLabel.setMinimumSize(QtCore.QSize(170, 0))
        self.temperatureLabel.setMaximumSize(QtCore.QSize(170, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        self.temperatureLabel.setFont(font)
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.dataValueLayout.addWidget(self.temperatureLabel, 1, 3, 1, 1)
        
        spacerItem = QtWidgets.QSpacerItem(69, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.dataValueLayout.addItem(spacerItem, 1, 2, 1, 1)
        
        self.lattitudeValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.lattitudeValueLabel.setObjectName("lattitudeValueLabel")
        self.dataValueLayout.addWidget(self.lattitudeValueLabel, 1, 1, 1, 1)
        
        self.longitudeLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.longitudeLabel.sizePolicy().hasHeightForWidth())
        self.longitudeLabel.setSizePolicy(sizePolicy)
        self.longitudeLabel.setMinimumSize(QtCore.QSize(93, 0))
        self.longitudeLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        self.longitudeLabel.setFont(font)
        self.longitudeLabel.setObjectName("longitudeLabel")
        self.dataValueLayout.addWidget(self.longitudeLabel, 2, 0, 1, 1)
        self.longitudeValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.longitudeValueLabel.setObjectName("longitudeValueLabel")
        self.dataValueLayout.addWidget(self.longitudeValueLabel, 2, 1, 1, 1)
        
        self.atpPressureLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.atpPressureLabel.sizePolicy().hasHeightForWidth())
        self.atpPressureLabel.setSizePolicy(sizePolicy)
        self.atpPressureLabel.setMinimumSize(QtCore.QSize(200, 0))
        self.atpPressureLabel.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        self.atpPressureLabel.setFont(font)
        self.atpPressureLabel.setObjectName("atpPressureLabel")
        self.dataValueLayout.addWidget(self.atpPressureLabel, 0, 3, 1, 1)
        
        self.altitudeBMPValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.altitudeBMPValueLabel.setObjectName("altitudeBMPValueLabel")
        self.dataValueLayout.addWidget(self.altitudeBMPValueLabel, 2, 4, 1, 1)
        
        self.altitudeGPSValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.altitudeGPSValueLabel.setObjectName("altitudeGPSValueLabel")
        self.dataValueLayout.addWidget(self.altitudeGPSValueLabel, 0, 1, 1, 1)
        
        self.temperatureValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.temperatureValueLabel.setObjectName("temperatureValueLabel")
        self.dataValueLayout.addWidget(self.temperatureValueLabel, 1, 4, 1, 1)
        
        self.ultravioletLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ultravioletLabel.sizePolicy().hasHeightForWidth())
        self.ultravioletLabel.setSizePolicy(sizePolicy)
        self.ultravioletLabel.setMinimumSize(QtCore.QSize(140, 0))
        self.ultravioletLabel.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(True)
        self.ultravioletLabel.setFont(font)
        self.ultravioletLabel.setObjectName("ultravioletLabel")
        self.dataValueLayout.addWidget(self.ultravioletLabel, 3, 3, 1, 1)
        self.uvValueLabel = QtWidgets.QLabel(self.centralwidget)
        self.uvValueLabel.setObjectName("uvValueLabel")
        self.dataValueLayout.addWidget(self.uvValueLabel, 3, 4, 1, 1)
        
        self.verticalLayout.addLayout(self.dataValueLayout)
        
        self.graphLayout = QtWidgets.QGridLayout()
        self.graphLayout.setObjectName("graphLayout")
        
        self.acceleratometerView = PlotWidget(self.centralwidget)
        self.acceleratometerView.setObjectName("acceleratometerView")
        self.graphLayout.addWidget(self.acceleratometerView, 1, 1, 1, 1)
        
        # Ploting Data
        self.acceleratometerView.addLegend()
        self.acceleratometerView.showGrid(x = True, y = True)

        # self.acceleratometerView.hideAxis("bottom")
        self.acc_x_axis = self.acceleratometerView.plot(pen=(102, 252, 241), name='X')
        self.acc_y_axis = self.acceleratometerView.plot(pen=(29, 185, 84), name='Y')
        self.acc_z_axis = self.acceleratometerView.plot(pen=(203, 45, 111), name='Z')
        self.acc_ptr = 0
        self.acc_x_data: list = np.linspace(0, 0)
        self.acc_y_data: list = np.linspace(0, 0)
        self.acc_z_data: list = np.linspace(0, 0)
        
        self.gyroscopicView = PlotWidget(self.centralwidget)
        self.gyroscopicView.setObjectName("gyroscopicView")
        self.graphLayout.addWidget(self.gyroscopicView, 1, 0, 1, 1)
        
        self.gyroscopicView.addLegend()
        self.gyroscopicView.showGrid(x = True, y = True)
        # self.acceleratometerView.hideAxis("bottom")
        self.gy_x_axis = self.gyroscopicView.plot(pen=(102, 252, 241), name='X')
        self.gy_y_axis = self.gyroscopicView.plot(pen=(29, 185, 84), name='Y')
        self.gy_z_axis = self.gyroscopicView.plot(pen=(203, 45, 111), name='Z')
        self.gy_ptr = 0
        self.gy_x_data: list = np.linspace(0, 0)
        self.gy_y_data: list = np.linspace(0, 0)
        self.gy_z_data: list = np.linspace(0, 0)
        
        self.accelaration_data = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        self.accelaration_data.setFont(font)
        self.accelaration_data.setObjectName("accelaration_data")
        
        # self.graphLayout.addWidget(self.accelaration_data, 0, 0, 1, 1)
        self.graphLayout.addWidget(self.accelaration_data, 0, 1, 1, 1)
        
        self.gyroscopic_data = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setPointSize(10)
        font.setBold(True)
        self.gyroscopic_data.setFont(font)
        self.gyroscopic_data.setObjectName("gyroscopic_data")
        # self.graphLayout.addWidget(self.gyroscopic_data, 0, 1, 1, 1)
        self.graphLayout.addWidget(self.gyroscopic_data, 0, 0, 1, 1)
        
        self.verticalLayout.addLayout(self.graphLayout)
        
        self.mapView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.mapView.setObjectName("mapView")
        self.verticalLayout.addWidget(self.mapView)
        self.plot_map = False
        
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def handleStorage(self):
        if self.database.isStoring:
            self.database.stop()
            self.storageBtn.setText(self._translate("MainWindow", "Start Storage"))
            self.storageBtn.setStyleSheet("""
            background-color: rgba(55, 211, 185, 200);                              
            """)
            return
        self.database.start()
        self.database.startStorage(["GPS Altitude","Lattitude","Longitude","Pressure", "Temperature","BMP Alititude","acceleration_x","acceleration_y","acceleration_z","gyro_x","gyro_y","gyro_z","UV Data", "time (millisecond)"])
        self.storageBtn.setText(self._translate("MainWindow", "Stop Storage"))
        self.storageBtn.setStyleSheet("""
        #storageBtn {
            background-color: rgb(255, 41, 26);
            color: #ffffff;
        }
        
        #storageBtn:hover {
            background-color: rgba(255, 41, 26, 200);
        }
        """)
        return
    def updateCommunication(self):
        self.data: list = self.serial_connect.getData()
        if len(self.data) > 2:
            isTitle: bool = False
            first_el = self.data.pop()
            if first_el == 'HEADING':
                isTitle = True
            elif first_el == 'DATA':
                # Updating Data Labels
                (
                    gps_latitude, 
                    gps_longitude, 
                    gps_altitude,
                    
                    temperature, 
                    atm_pressure, 
                    bmp_altitude, 
                    
                    acc_x, 
                    acc_y, 
                    acc_z, 
                    
                    gy_x, 
                    gy_y, 
                    gy_z, 
                    
                    uv_value,
                    _,
                    *_
                ) = self.data
                # GPS DATA
                self.altitudeGPSValueLabel.setText(self._translate("MainWindow", gps_altitude))
                self.lattitudeValueLabel.setText(self._translate("MainWindow", gps_latitude))
                self.longitudeValueLabel.setText(self._translate("MainWindow", gps_longitude))
                
                # BMP280 Module
                self.pressureValueLabel.setText(self._translate("MainWindow", atm_pressure))
                self.temperatureValueLabel.setText(self._translate("MainWindow", temperature))
                self.altitudeBMPValueLabel.setText(self._translate("MainWindow", bmp_altitude))
                
                self.uvValueLabel.setText(self._translate("MainWindow", uv_value))
                self.acceleration_update(acc_x, acc_y, acc_z)
                self.gyro_update(gy_x, gy_y, gy_z)
                
                if self.plot_map:
                    self.childWindow.showMap(gps_altitude, gps_latitude, gps_longitude)
            if first_el in ['HEADING', 'DATA']:
                self.database.startStorage(self.data, isTitle=isTitle)
            # else
            #   invalid data
    def gyro_update(self, ax, ay, az):
        self.gy_x_data[:-1] = self.gy_x_data[1:]
        self.gy_y_data[:-1] = self.gy_y_data[1:]
        self.gy_z_data[:-1] = self.gy_z_data[1:]
        
        self.gy_x_data[-1] = float(ax)
        self.gy_y_data[-1] = float(ay)
        self.gy_z_data[-1] = float(az)
        
        self.gy_ptr += 1
        
        self.gyroscopic_data.setText(self._translate("MainWindow", f"Gyroscope: X = {ax}, Y = {ay}, Z = {az}"))
        
        self.gy_x_axis.setData(self.gy_x_data)
        self.gy_y_axis.setData(self.gy_y_data)
        self.gy_z_axis.setData(self.gy_z_data)
        
        self.gy_x_axis.setPos(self.gy_ptr, 0) # Increasing X-Axis of GraphView
        self.gy_y_axis.setPos(self.gy_ptr, 0)
        self.gy_z_axis.setPos(self.gy_ptr, 0)
    def viewMap(self):
        self.plot_map = True
        self.childWindow.show()
    def acceleration_update(self, ax, ay, az):
        self.acc_x_data[:-1] = self.acc_x_data[1:]
        self.acc_y_data[:-1] = self.acc_y_data[1:]
        self.acc_z_data[:-1] = self.acc_z_data[1:]
        
        self.acc_x_data[-1] = float(ax)
        self.acc_y_data[-1] = float(ay)
        self.acc_z_data[-1] = float(az)
        
        self.acc_ptr += 1
        
        self.accelaration_data.setText(self._translate("MainWindow", f"Acceleration: X = {ax}, Y = {ay}, Z = {az}"))
        
        self.acc_x_axis.setData(self.acc_x_data)
        self.acc_y_axis.setData(self.acc_y_data)
        self.acc_z_axis.setData(self.acc_z_data)
        
        self.acc_x_axis.setPos(self.acc_ptr, 0) # Increasing X-Axis of GraphView
        self.acc_y_axis.setPos(self.acc_ptr, 0)
        self.acc_z_axis.setPos(self.acc_ptr, 0)
    def retranslateUi(self, MainWindow):
        self._translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(self._translate("MainWindow", "Data Visualization of Sensor Data ── loRa"))
        # self.title_label.setText(self._translate("MainWindow", "Data Visualization of Sensor Data ── loRa"))
        self.storageBtn.setText(self._translate("MainWindow", "Start Storage"))
        self.gps_title_label.setText(self._translate("MainWindow", "Global Positioning System (GPS)"))
        self.bmp_title_label.setText(self._translate("MainWindow", "Sensor (BMP280 and UV)"))
        self.altitudeBMPLabel.setText(self._translate("MainWindow", "Altitude (meter)"))
        self.altitudeGPSLabel.setText(self._translate("MainWindow", "Altitude (meter)"))
        self.lattitudeLabel.setText(self._translate("MainWindow", "Lattitude"))
        self.pressureValueLabel.setText(self._translate("MainWindow", "Dynamic Value"))
        self.temperatureLabel.setText(self._translate("MainWindow", "Temperature (°C)"))
        self.lattitudeValueLabel.setText(self._translate("MainWindow", "Dynamic Value"))
        self.longitudeLabel.setText(self._translate("MainWindow", "Longitude"))
        self.longitudeValueLabel.setText(self._translate("MainWindow", "Dynamic Value"))
        self.atpPressureLabel.setText(self._translate("MainWindow", "Atmospheric Pressure (KPa)"))
        self.altitudeBMPValueLabel.setText(self._translate("MainWindow", "Dynamic Value"))
        self.altitudeGPSValueLabel.setText(self._translate("MainWindow", "Dynamic Value"))
        self.temperatureValueLabel.setText(self._translate("MainWindow", "Dynamic Value"))
        self.ultravioletLabel.setText(self._translate("MainWindow", "Ultraviolet Data (Volt)"))
        self.uvValueLabel.setText(self._translate("MainWindow", "Dynamic Value"))
        self.accelaration_data.setText(self._translate("MainWindow", "Acceleration Dynamic Value"))
        self.gyroscopic_data.setText(self._translate("MainWindow", "Gyrocopy Dynamic Value"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
