# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CreateNew_LUDialog
                                 A QGIS plugin
 CreateNew_LU
                             -------------------
        begin                : 2016-10-17
        git sha              : $Format:%H$
        copyright            : (C) 2016 by CreateNew_LU
        email                : CreateNew_LU
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from utility_functions import getQGISDbs
from PyQt4 import QtCore, QtGui, uic
from DbSettings_dialog import DbSettingsDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'CreateNew_LU_dialog_base.ui'))


class CreateNew_LUDialog(QtGui.QDialog, FORM_CLASS):
    create_new_layer = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(CreateNew_LUDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # setup signals
        self.pushButtonSelectLocationLU.clicked.connect(self.selectSaveLocationLU)
        self.pushButtonLUNewFileDLG.clicked.connect(self.newLULayer)
        self.closePopUpLUButton.clicked.connect(self.closePopUpLU)

        available_dbs = getQGISDbs()
        self.dbsettings_dlg = DbSettingsDialog(available_dbs)
        self.dbsettings_dlg.nameLineEdit.setText('landuse')

        self.lu_memory_radioButton.setChecked(True)
        self.lineEditLU.setPlaceholderText('Save as temporary layer')
        self.lineEditLU.setDisabled(True)
        self.lu_shp_radioButton.setChecked(False)
        self.lu_postgis_radioButton.setChecked(False)

        self.lu_shp_radioButton.clicked.connect(self.setOutput)
        self.lu_postgis_radioButton.clicked.connect(self.setOutput)
        self.lu_memory_radioButton.clicked.connect(self.setOutput)

        self.dbsettings_dlg.setDbOutput.connect(self.setOutput)

    def closePopUpLU(self):
        self.close()

    # Open Save file dialogue and set location in text edit
    def selectSaveLocationLU(self):
        if self.lu_shp_radioButton.isChecked():
            filename = QtGui.QFileDialog.getSaveFileName(None, "Select Save Location ", "", '*.shp')
            self.lineEditLU.setText(filename)
        elif self.lu_postgis_radioButton.isChecked():
            self.setOutput()
            self.dbsettings_dlg.show()

            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            db_layer_name = "%s:%s:%s" % (
                self.dbsettings['dbname'], self.dbsettings['schema'], self.dbsettings['table_name'])
            print 'db_layer_name'
            self.lineEditLU.setText(db_layer_name)
        elif self.lu_memory_radioButton.isChecked():
            pass

    def setOutput(self):
        if self.lu_shp_radioButton.isChecked():
            self.lineEditLU.clear()
            self.lineEditLU.setPlaceholderText('')
            self.lineEditLU.setDisabled(False)
        elif self.lu_postgis_radioButton.isChecked():
            self.dbsettings = self.dbsettings_dlg.getDbSettings()
            print self.dbsettings
            db_layer_name = "%s:%s:%s" % (
                self.dbsettings['dbname'], self.dbsettings['schema'], self.dbsettings['table_name'])
            self.lineEditLU.setText(db_layer_name)
            self.lineEditLU.setDisabled(False)
        elif self.lu_memory_radioButton.isChecked():
            self.lineEditLU.clear()
            self.lineEditLU.setPlaceholderText('Save as temporary layer')
            self.lineEditLU.setDisabled(True)

    def newLULayer(self):
        self.create_new_layer.emit()

    def getSelectedLULayerID(self):
        return self.selectIDbuildingCombo.currentText()