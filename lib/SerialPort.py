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

from PyQt5.QtCore import QObject, QIODevice, pyqtSignal
from PyQt5.QtSerialPort import QSerialPort
from serial.tools.list_ports import comports


class SerialPort(QObject):
    packet_received = pyqtSignal(str)

    def __init__(self):
        super(SerialPort, self).__init__()
        self.ports = []
        self.serialData = ''
        self.commands = {
            'CurveTemporal': '|',
            'GainOffset': ':',
            'Laser': '#',
            'TimeAverage': '&',
            'StopTemporal': '[',
            'StopTechnical': '.',
            'ControlPeris': '*',
            'ControlImpulA': '!',
            'ControlImpulB': '+',
            'BackPeris': '<',
            'StopPeris': '=',
            'ForwardPeris': '>',
            'TimePulsesPumps': '_',
            'VolumePurge': 'a7',
            'PurgeImpulA': '{',
            'PurgeImpulB': '}',
            'IAmAlive': '?',
            'PowerDown': '/'
        }

        self.serialPort = QSerialPort()

    def ask_for_port(self):
        """\
        Show a list of ports and ask the user for a choice. To make selection
        easier on systems with long device names, also allow the input of an
        index.
        """
        for n, (port, desc, hwid) in enumerate(sorted(comports()), 1):
            info = {'port': port, 'desc': desc, 'hwid': hwid}
            self.ports.append(info)

        return self.ports

    def open_port(self, numberOfItem):
        if numberOfItem != 0:
            item = self.ports[numberOfItem - 1]

            self.serialPort.setPortName(item['port'])
            portOpen = self.serialPort.open(QIODevice.ReadWrite)

            if portOpen:
                self.serialPort.setBaudRate(QSerialPort.Baud115200)
                self.serialPort.setDataBits(QSerialPort.Data8)
                self.serialPort.setParity(QSerialPort.NoParity)
                self.serialPort.setStopBits(QSerialPort.OneStop)
                self.serialPort.setFlowControl(QSerialPort.NoFlowControl)

                return True

            else:
                return False

    def close_port(self):
        self.serialPort.close()

    def receive_port(self):
        data = self.serialPort.readAll()
        self.serialData = data.data().decode('utf8')

        return self.serialData

    def receive_data(self):
        dataRead = self.serialPort.read(1).decode('utf8')

        self.packet_received.emit(dataRead)

    def receive_multiple_data(self):
        data = self.serialPort.readAll()

        dataRead = data.data().decode('utf8')

        self.packet_received.emit(dataRead)

    def write_port(self, data):
        self.serialPort.writeData(data.encode())

    def write_port_list(self, data):
        for value in data:
            self.serialPort.writeData(value.encode())

    def send_I_am_alive(self):
        self.write_port('?')

    def send_Gain_Offset(self, toSend):
        self.write_port(self.commands['GainOffset'])

        for value in toSend:
            self.write_port(f'{value:02x}')

    def send_Control_Peristaltic(self, toSend):
        self.write_port(self.commands['ControlPeris'])

        for value in toSend:
            self.write_port(f'{value:02x}')

    def send_Control_Impul_A(self, toSend):
        self.write_port(self.commands['ControlImpulA'])

        # for value in toSend:
        self.write_port(f'{toSend:04x}')

    def send_Control_Impul_B(self, toSend):
        self.write_port(self.commands['ControlImpulB'])

        # for value in toSend:
        self.write_port(f'{toSend:04x}')

    def send_Volume_Purges(self, toSend):
        self.write_port(self.commands['VolumePurge'])

        for value in toSend:
            self.write_port(f'{value:04x}')

    def send_Laser(self, toSend):
        self.write_port(self.commands['Laser'])

        self.write_port(f'{toSend:02x}')

    def send_Auto_Acquisition(self, toSend):
        self.write_port(self.commands['TimeAverage'])
        self.write_port('@')

        self.write_port(f'{toSend:04x}')

    def send_Finish_Experiment(self):
        self.write_port('[')

    def send_Init_Experiment(self):
        self.write_port(self.commands['CurveTemporal'])
        self.write_port('@')

        self.write_port(f'{1:04x}')

    def send_Back_Peristaltic(self):
        self.write_port(self.commands['BackPeris'])

        self.write_port(f'{0:04x}')

    def send_Stop_Peristaltic(self):
        self.write_port(self.commands['StopPeris'])

        self.write_port(f'{0:04x}')

    def send_Forward_Peristaltic(self):
        self.write_port(self.commands['ForwardPeris'])

        self.write_port(f'{0:04x}')

    def send_BSF_Peristaltic(self, who):
        if who == 0:
            self.send_Back_Peristaltic()

        elif who == 1:
            self.send_Stop_Peristaltic()

        else:
            self.send_Forward_Peristaltic()
