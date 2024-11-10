#/usr/bin/python3

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QVBoxLayout, QTextEdit, QComboBox, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import subprocess
import re
from PyQt5.QtCore import QProcess

class WorkerThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        process = subprocess.run(self.command, capture_output=True, text=True)
        # Clean up ANSI escape codes
        clean_output = self.remove_ansi_escape_codes(process.stdout)
        self.finished.emit(clean_output)

    def remove_ansi_escape_codes(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mG]')  # Regex pattern for ANSI codes
        return ansi_escape.sub('', text)

class Realtic(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mutex = QMutex()
        self.threads = []

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel('Select a tool to run:', self)
        layout.addWidget(self.label)

        self.toolSelector = QComboBox(self)
        self.toolSelector.addItems(['Linear Trails', 'SHA1 Collision Detection', 'Break OTS', 'RSA CTF Tool', 'S-Box Gates'])
        self.toolSelector.currentIndexChanged.connect(self.toolChanged)
        layout.addWidget(self.toolSelector)

        self.fileLabel = QLabel('Select XML file for Linear Trails:', self)
        layout.addWidget(self.fileLabel)

        self.btn = QPushButton('Browse', self)
        self.btn.clicked.connect(self.openFileDialog)
        layout.addWidget(self.btn)

        # Add input fields for BreakOTS parameters
        self.p_input = QLineEdit(self)
        self.p_input.setPlaceholderText("Enter value for p")
        self.p_input.hide()  # Hide by default
        layout.addWidget(self.p_input)

        self.w1_input = QLineEdit(self)
        self.w1_input.setPlaceholderText("Enter value for w1")
        self.w1_input.hide()  # Hide by default
        layout.addWidget(self.w1_input)

        self.w2_input = QLineEdit(self)
        self.w2_input.setPlaceholderText("Enter value for w2")
        self.w2_input.hide()  # Hide by default
        layout.addWidget(self.w2_input)

        self.delta_input = QLineEdit(self)
        self.delta_input.setPlaceholderText("Enter value for delta")
        self.delta_input.hide()  # Hide by default
        layout.addWidget(self.delta_input)

        self.relax_input = QLineEdit(self)
        self.relax_input.setPlaceholderText("Enter value for relax")
        self.relax_input.hide()  # Hide by default
        layout.addWidget(self.relax_input)

        self.threshold_input = QLineEdit(self)
        self.threshold_input.setPlaceholderText("Enter value for threshold")
        self.threshold_input.hide()  # Hide by default
        layout.addWidget(self.threshold_input)

        self.maxBFround_input = QLineEdit(self)
        self.maxBFround_input.setPlaceholderText("Enter value for maxBFround")
        self.maxBFround_input.hide()  # Hide by default
        layout.addWidget(self.maxBFround_input)

        self.runBtn = QPushButton('Run', self)
        self.runBtn.clicked.connect(self.runTool)
        layout.addWidget(self.runBtn)

        self.outputBox = QTextEdit(self)
        self.outputBox.setReadOnly(True)
        layout.addWidget(self.outputBox)

        self.setLayout(layout)
        self.setWindowTitle('Realtic')
        self.setGeometry(500, 100, 1000, 850)
        self.show()

    def toolChanged(self):
        if self.toolSelector.currentText() == 'Linear Trails':
            self.fileLabel.setText('Select XML file for Linear Trails:')
            self.btn.setText('Browse XML File')
            self.filePath = None
            self.p_input.hide()
            self.w1_input.hide()
            self.w2_input.hide()
            self.delta_input.hide()
            self.relax_input.hide()
            self.threshold_input.hide()
            self.maxBFround_input.hide()            

        elif self.toolSelector.currentText() == 'SHA1 Collision Detection':
            self.fileLabel.setText('Select PDF files for SHA1 Collision Detection:')
            self.btn.setText('Browse PDF Files')
            self.p_input.hide()
            self.w1_input.hide()
            self.w2_input.hide()
            self.delta_input.hide()
            self.relax_input.hide()
            self.threshold_input.hide()
            self.maxBFround_input.hide()            

        elif self.toolSelector.currentText() == 'Break OTS':
            self.fileLabel.setText('Select TXT file for BreakOTS:')
            self.btn.setText('Browse TXT File')
            # Show BreakOTS input fields
            self.p_input.show()
            self.w1_input.show()
            self.w2_input.show()
            self.delta_input.show()
            self.relax_input.show()
            self.threshold_input.show()
            self.maxBFround_input.show()
        
        elif self.toolSelector.currentText() == 'RSA CTF Tool':
            self.fileLabel.setText('Select PUB files for RSA CTF Tool:')
            self.btn.setText('Browse PUB Files')
            self.filePath = None
            self.p_input.hide()
            self.w1_input.hide()
            self.w2_input.hide()
            self.delta_input.hide()
            self.relax_input.hide()
            self.threshold_input.hide()
            self.maxBFround_input.hide()  
            
        elif self.toolSelector.currentText() == 'S-Box Gates':
            self.fileLabel.setText('Select TXT file for S-Box Gates:')
            self.btn.setText('Browse TXT File')
            self.filePath = None
            self.p_input.hide()
            self.w1_input.hide()
            self.w2_input.hide()
            self.delta_input.hide()
            self.relax_input.hide()
            self.threshold_input.hide()
            self.maxBFround_input.hide()

    def openFileDialog(self):
        options = QFileDialog.Options()
        if self.toolSelector.currentText() == 'Linear Trails':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select XML File", "", "XML Files (*.xml);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {self.filePath}')
        
        elif self.toolSelector.currentText() == 'SHA1 Collision Detection':
            self.pdfFiles, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf);;All Files (*)", options=options)
            if self.pdfFiles:
                self.fileLabel.setText(f'Selected: {len(self.pdfFiles)} PDF file(s)')
        
        elif self.toolSelector.currentText() == 'Break OTS':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select TXT File", "", "TXT Files (*.txt);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {self.filePath}')
        
        elif self.toolSelector.currentText() == 'RSA CTF Tool':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select PUB File", "", "PUB Files (*.pub);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {self.filePath}')
        
        elif self.toolSelector.currentText() == 'S-Box Gates':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select TXT File", "", "TXT Files (*.txt);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {self.filePath}')


    def runTool(self):
        if self.toolSelector.currentText() == 'Linear Trails' and self.filePath:
            commands = [
                ['timeout', '30', '/root/Documents/ReInfoSec/Realtic/Linear_Trails/lin', '-I', '10', '-S', '2', '-i', self.filePath],
            ]
            self.runCommandsInThreads(commands)

        elif self.toolSelector.currentText() == 'SHA1 Collision Detection' and self.pdfFiles:
            command = ['/root/Documents/ReInfoSec/Realtic/SHA1_Collision_Detection/bin/sha1dcsum'] + self.pdfFiles
            self.runCommandsInThreads([command])

        elif self.toolSelector.currentText() == 'Break OTS' and self.filePath:
            # Get values from input fields
            p_value = self.p_input.text()
            w1_value = self.w1_input.text()
            w2_value = self.w2_input.text()
            delta_value = self.delta_input.text()
            relax_value = self.relax_input.text()
            threshold_value = self.threshold_input.text()
            maxBFround_value = self.maxBFround_input.text()

            command = ['/root/Documents/ReInfoSec/Realtic/Persichetti_OTS_CryptAnalysis/breakOTS', p_value, w1_value, w2_value, delta_value, relax_value, self.filePath, threshold_value, maxBFround_value]
            self.runCommandsInThreads([command])
        
        elif self.toolSelector.currentText() == 'RSA CTF Tool':
            self.runRsaCtfToolInNewTerminal()
        
        elif self.toolSelector.currentText() == 'S-Box Gates' and self.filePath:
            command = ['/root/Documents/ReInfoSec/Realtic/S-Box_Gates/build/sboxgates', self.filePath]
            self.runCommandsInThreads([command])
        
    
    def runRsaCtfToolInNewTerminal(self):
        # Define the command to open a new terminal and execute RsaCtfTool
        self.process = QProcess(self)
        self.process.start("x-terminal-emulator", ["-e", "bash", "-c", f"python3 /root/Documents/ReInfoSec/Realtic/RSA_CTF_Tool/RsaCtfTool.py --publickey {self.filePath} --private; exec bash"])

    def runCommandsInThreads(self, commands):
        for command in commands:
            worker = WorkerThread(command)
            worker.finished.connect(self.displayOutput)
            worker.finished.connect(lambda: self.threads.remove(worker))
            self.threads.append(worker)
            worker.start()

    def displayOutput(self, output):
        self.mutex.lock()
        self.outputBox.append(output)
        self.mutex.unlock()

    def closeEvent(self, event):
        for thread in self.threads:
            thread.quit()
            thread.wait()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Realtic()
    sys.exit(app.exec_())
