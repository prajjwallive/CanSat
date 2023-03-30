from PyQt5 import QtCore, QtGui, QtWidgets
from folium import Map, Marker, Icon, Popup, PolyLine
import io, os

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.parent = parent
        self.setupUi()
    def setupUi(self):
        self.setObjectName("MainWindow")
        
        self.map = Map(location=[28.3949, 84.1240], zoom_start=2)
        self.data = io.BytesIO()
        self.last:list = []
        
        self.coord: list = []
        
        self.resize(800, 600)
        
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.graphicsView = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 565))
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Poppins")
        font.setBold(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)
        self.map_loc = 'C:\\Users\\ccs\\Desktop\\dashboard_original\\UI\\map.html'
        if os.path.exists(self.map_loc):
            with open(self.map_loc, 'a'):
                pass
        url = QtCore.QUrl.fromLocalFile(self.map_loc)
        self.graphicsView.load(QtCore.QUrl(url))
        # self.graphicsView.show()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
    def showMap(self, altitude, latitude, longitude):
        "lattitude longitude"
        self.label_3.setText(self._translate("MainWindow", f"Altitude - {altitude}"))
        self.label_2.setText(self._translate("MainWindow", f"Latitude - {latitude}"))
        self.label.setText(self._translate("MainWindow", f"Longitude - {longitude}"))
        self.coord.append((latitude, longitude))
        if self.last != [latitude, longitude]:
            Marker(
                location=[latitude, longitude],
                icon=Icon(color='red'),
                popup=Popup(f"<b>Latitude</b> {latitude}<br><b>Longitude</b> {longitude}", min_width=150, max_width=500)
            ).add_to(self.map)
            self.map.save(self.map_loc)
            self.last = [latitude, longitude]
            url = QtCore.QUrl.fromLocalFile(self.map_loc)
            self.graphicsView.load(url)
    def retranslateUi(self):
        self._translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(self._translate("MainWindow", "GeoGraphical Plots"))
        self.label_3.setText(self._translate("MainWindow", "Altitude"))
        self.label_2.setText(self._translate("MainWindow", "Latitude"))
        self.label.setText(self._translate("MainWindow", "Longitude"))
from PyQt5 import QtWebEngineWidgets
