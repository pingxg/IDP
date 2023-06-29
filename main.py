#Imports
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from evaluate import segmentation_image



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('GUI.ui',self)
        self.show()

        
        #Declare variable for image path
        #tmp retains path in case of cancellations
        self.img_path = None
        self.img_path_tmp = None
        
        #Set default filepath for compatibility
        self.search_folder = 'C:\\'

        #Browse and analysis buttons connected to their functions
        self.browse_btn.clicked.connect(self.open_image)
       
        self.analyze_btn.clicked.connect(self.analyze_image)

    def open_image(self):
        #Select the file dialog design
        dialog_style = QFileDialog.DontUseNativeDialog
        dialog_style |= QFileDialog.DontUseCustomDirectoryIcons


        #Open the file dialog window and show only tiff-format images (or not?)
        self.img_path, _ = QFileDialog.getOpenFileName(self, "File selector", self.search_folder,
        "All Files (*);;TIFF (*.TIF *.tif *.TIFF *.tiff)", options=dialog_style)

        #update temporary path variable only if a new one was chosen
        if self.img_path != "":
            self.img_path_tmp = self.img_path

        #Show the path of the file chosen.
        if self.img_path:
                #Change the text on the label to display the file path chosen.
                self.browse_bar.setText(self.img_path)
                
                #Load and scale the image to its QLabel         
                orig_pixmap = QtGui.QPixmap(self.img_path).scaled(512, 512, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
                self.orig_img.setPixmap(orig_pixmap)

                #Replace the priously analyzed picture with an empty QLabel
                self.anal_img.setPixmap(QtGui.QPixmap())

                 
        else:
                #If nothing chosen, retain previous path in the bar
                self.browse_bar.setText(self.img_path_tmp)
                
        
    
    def analyze_image(self):
          #run the chosen image through the model and scale it to its QLabel
          if self.img_path:
             analyzed_image = segmentation_image(self.img_path)
             anal_pixmap = QtGui.QPixmap(analyzed_image).scaled(512, 512, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
             self.anal_img.setPixmap(anal_pixmap)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
