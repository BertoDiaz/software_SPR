"""
Copyright (C) 2018  Heriberto J. Díaz Luis-Ravelo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QMessageBox, QLabel, QFileDialog
from PyQt5.QtWidgets import QDesktopWidget, QHBoxLayout, QGridLayout, QGroupBox, QSpinBox
from PyQt5.QtCore import Qt
import styles as style


class ViewSystemControl(QWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.timeoutMessage = {
            'Laser': 'The laser was not switch ON/OFF, try again.',
            'Peristaltic': 'The peristaltic did not respond, try again.',
            'Impulsional A': 'The impulsional A pump did not respond, try again.',
            'Impulsional B': 'The impulsional B pump did not respond, try again.'
        }

        self.notCeroMessage = {
            'Impulsional A': 'The value of the impulsional A cannot be 0.',
            'Impulsional B': 'The value of the impulsional B cannot be 0.'
        }

        self.btnLaser = QPushButton('Laser OFF')

        self.lblPeristaltic = QLabel("Flow Peristaltic")
        self.edtPeristaltic = QSpinBox()
        self.lblImpulsional_A = QLabel("Injection Impulsional A:")
        self.edtImpulsional_A = QSpinBox()
        self.lblImpulsional_B = QLabel("Injection Impulsional B:")
        self.edtImpulsional_B = QSpinBox()

        self.btnPeristaltic = QPushButton("START")
        self.btnImpulsional_A = QPushButton("INJECT")
        self.btnImpulsional_B = QPushButton("INJECT")

        self.layoutGrid = QGridLayout(self)

        self.laserBoxLayout = QGroupBox("Laser Control")
        self.dataBoxLayout = QGroupBox("Pumps control")
        self.otherBoxLayout = QGroupBox("Other Layout")
        self.peristalticBoxLayout = QGroupBox("Peristaltic Pump Control")
        self.impulsionalABoxLayout = QGroupBox("Impulsional Pump A Control")
        self.impulsionalBBoxLayout = QGroupBox("Impulsional Pump B Control")

        self.dataLayout = QGridLayout(self)
        self.peristalticLayout = QGridLayout(self)
        self.impulsionalALayout = QGridLayout(self)
        self.impulsionalBLayout = QGridLayout(self)

        self.laserLayout = QVBoxLayout(self)

        self.otherLayout = QHBoxLayout(self)

        self.setStyleSpinBox()
        self.setStyleButtons()

        self.resize(1200, 800)
        self.centerWindowOnScreen()
        self.setWindowTitle('SPR v2')

    def centerWindowOnScreen(self):
        windowGeometry = self.frameGeometry()
        desktopWidget = QDesktopWidget().availableGeometry().center()
        windowGeometry.moveCenter(desktopWidget)
        self.move(windowGeometry.topLeft())

    def mainWindow(self):
        self.layoutGrid.addWidget(self.setLaserGroup(), 0, 0)
        self.layoutGrid.addWidget(self.setDataGroup(), 0, 1, 1, 3)
        self.layoutGrid.addWidget(self.setOtherGroup(), 1, 0, 5, 6)

    def setLaserGroup(self):
        self.laserLayout.addWidget(self.btnLaser, 0, Qt.AlignBottom)

        self.laserBoxLayout.setStyleSheet(style.groupBoxGeneral)
        self.laserBoxLayout.setLayout(self.laserLayout)

        return self.laserBoxLayout

    def setDataGroup(self):
        self.lblPeristaltic.setFixedWidth(100)
        self.lblPeristaltic.setAlignment(Qt.AlignBottom)
        self.lblImpulsional_A.setFixedWidth(100)
        self.lblImpulsional_A.setAlignment(Qt.AlignBottom)
        self.lblImpulsional_B.setFixedWidth(100)
        self.lblImpulsional_B.setAlignment(Qt.AlignBottom)

        self.peristalticLayout.addWidget(self.lblPeristaltic, 0, 0)
        self.peristalticLayout.addWidget(self.edtPeristaltic, 1, 0)
        self.peristalticLayout.addWidget(self.btnPeristaltic, 0, 1, 2, 1)

        self.impulsionalALayout.addWidget(self.lblImpulsional_A, 0, 0)
        self.impulsionalALayout.addWidget(self.edtImpulsional_A, 1, 0)
        self.impulsionalALayout.addWidget(self.btnImpulsional_A, 0, 1, 2, 1)

        self.impulsionalBLayout.addWidget(self.lblImpulsional_B, 0, 0)
        self.impulsionalBLayout.addWidget(self.edtImpulsional_B, 1, 0)
        self.impulsionalBLayout.addWidget(self.btnImpulsional_B, 0, 1, 2, 1)

        self.peristalticBoxLayout.setStyleSheet(style.groupBoxGeneral)
        self.peristalticBoxLayout.setLayout(self.peristalticLayout)

        self.impulsionalABoxLayout.setStyleSheet(style.groupBoxGeneral)
        self.impulsionalABoxLayout.setLayout(self.impulsionalALayout)

        self.impulsionalBBoxLayout.setStyleSheet(style.groupBoxGeneral)
        self.impulsionalBBoxLayout.setLayout(self.impulsionalBLayout)

        self.dataLayout.addWidget(self.peristalticBoxLayout, 0, 0)
        self.dataLayout.addWidget(self.impulsionalABoxLayout, 0, 1)
        self.dataLayout.addWidget(self.impulsionalBBoxLayout, 0, 2)

        self.dataBoxLayout.setStyleSheet(style.groupBoxGeneral)
        self.dataBoxLayout.setLayout(self.dataLayout)

        return self.dataBoxLayout

    def setOtherGroup(self):
        self.otherBoxLayout.setLayout(self.otherLayout)

        return self.otherBoxLayout

    """
    ********************************************************************************************************************
    *                                              Laser Control Functions                                             *
    ********************************************************************************************************************
    """

    def setBtnLaserStatus(self, status):
        if status:
            text = 'Laser ON'

        else:
            text = 'Laser OFF'

        self.btnLaser.setText(text)
        self.btnLaser.setChecked(status)

    def setBtnLaserDisable(self, disable):
        self.btnLaser.setDisabled(disable)

    """
    ********************************************************************************************************************
    *                                            End Laser Control Functions                                           *
    ********************************************************************************************************************
    """

    """
    ********************************************************************************************************************
    *                                           Peristaltic Control Functions                                          *
    ********************************************************************************************************************
    """

    def setBtnPeristalticStatus(self, status):
        if status:
            text = 'STOP'

        else:
            text = 'START'

        self.btnPeristaltic.setText(text)
        self.btnPeristaltic.setChecked(status)

    def getBtnPeristalticStatus(self):
        return self.btnPeristaltic.isChecked()

    def setBtnPeristalticDisable(self, disable):
        self.btnPeristaltic.setDisabled(disable)

    def setEdtPeristalticValue(self, value):
        self.edtPeristaltic.setValue(value)

    def getEdtPeristalticValue(self):
        return self.edtPeristaltic.value()

    """
    ********************************************************************************************************************
    *                                         End Peristaltic Control Functions                                        *
    ********************************************************************************************************************
    """

    """
    ********************************************************************************************************************
    *                                          Impulsional A Control Functions                                         *
    ********************************************************************************************************************
    """

    def setBtnImpulsionalAStatus(self, status):
        self.btnImpulsional_A.setChecked(status)
        self.setBtnImpulsionalADisable(status)

    def getBtnImpulsionalAStatus(self):
        return self.btnImpulsional_A.isChecked()

    def setBtnImpulsionalADisable(self, disable):
        self.btnImpulsional_A.setDisabled(disable)

    def setEdtImpulsionalAValue(self, value):
        self.edtImpulsional_A.setValue(value)

    def getEdtImpulsionalAValue(self):
        return self.edtImpulsional_A.value()

    """
    ********************************************************************************************************************
    *                                        End Impulsional A Control Functions                                       *
    ********************************************************************************************************************
    """

    """
    ********************************************************************************************************************
    *                                          Impulsional B Control Functions                                         *
    ********************************************************************************************************************
    """

    def setBtnImpulsionalBStatus(self, status):
        self.btnImpulsional_B.setChecked(status)
        self.setBtnImpulsionalBDisable(status)

    def getBtnImpulsionalBStatus(self):
        return self.btnImpulsional_B.isChecked()

    def setBtnImpulsionalBDisable(self, disable):
        self.btnImpulsional_B.setDisabled(disable)

    def setEdtImpulsionalBValue(self, value):
        self.edtImpulsional_B.setValue(value)

    def getEdtImpulsionalBValue(self):
        return self.edtImpulsional_B.value()

    """
    ********************************************************************************************************************
    *                                        End Impulsional B Control Functions                                       *
    ********************************************************************************************************************
    """

    """
    ********************************************************************************************************************
    *                                             Buttons Styles Functions                                             *
    ********************************************************************************************************************
    """

    def setStyleButtons(self):
        self.btnLaser.setStyleSheet(style.buttonLaserBig)
        self.btnLaser.setCheckable(True)

        self.btnPeristaltic.setStyleSheet(style.buttonPeristaltic)
        self.btnPeristaltic.setCheckable(True)

        self.btnImpulsional_A.setStyleSheet(style.buttonImpulsional)
        self.btnImpulsional_A.setCheckable(True)

        self.btnImpulsional_B.setStyleSheet(style.buttonImpulsional)
        self.btnImpulsional_B.setCheckable(True)

    """
    ********************************************************************************************************************
    *                                           End Buttons Styles Functions                                           *
    ********************************************************************************************************************
    """

    """
    ********************************************************************************************************************
    *                                            Spin Boxes Styles Functions                                           *
    ********************************************************************************************************************
    """

    def setStyleSpinBox(self):
        self.edtPeristaltic.setStyleSheet(style.spinBoxGeneral)
        self.edtImpulsional_A.setStyleSheet(style.spinBoxGeneral)
        self.edtImpulsional_B.setStyleSheet(style.spinBoxGeneral)

        self.edtPeristaltic.setRange(0, 100)
        self.edtImpulsional_A.setRange(0, 100)
        self.edtImpulsional_B.setRange(0, 100)

    """
    ********************************************************************************************************************
    *                                          End Spin Boxes Styles Functions                                         *
    ********************************************************************************************************************
    """

    """
    ********************************************************************************************************************
    *                                                Messages Functions                                                *
    ********************************************************************************************************************
    """

    def setMessageCritical(self, typeMessage, message):
        QMessageBox.critical(self, typeMessage, message)

    def setMessageExistsFile(self):
        loadFile = QMessageBox.question(self, "Question", "Load a configuration file?",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if loadFile == QMessageBox.Yes:
            fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "/home", "*.cfg")

            return [True, fileName]

        else:
            return [False, None]

    """
    ********************************************************************************************************************
    *                                              End Messages Functions                                              *
    ********************************************************************************************************************
    """
