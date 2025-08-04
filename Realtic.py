#!/usr/bin/python3

import sys
import os
import datetime
import tempfile
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog, QLabel, 
                            QVBoxLayout, QHBoxLayout, QTextEdit, QComboBox, QLineEdit, 
                            QScrollArea, QFrame, QSplitter, QCheckBox, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, Qt
import subprocess
import re
from PyQt5.QtCore import QProcess

class WorkerThread(QThread):
    finished = pyqtSignal(str, str)  # output, tool_name
    progress = pyqtSignal(str, str)  # output, tool_name

    def __init__(self, command, tool_name):
        super().__init__()
        self.command = command
        self.tool_name = tool_name

    def run(self):
        try:
            process = subprocess.Popen(self.command, stdout=subprocess.PIPE, 
                                     stderr=subprocess.STDOUT, text=True, 
                                     universal_newlines=True)
            
            # Read output line by line for real-time updates
            for line in iter(process.stdout.readline, ''):
                if line:
                    clean_line = self.remove_ansi_escape_codes(line)
                    self.progress.emit(clean_line, self.tool_name)
            
            process.wait()
            self.finished.emit("", self.tool_name)
            
        except Exception as e:
            error_msg = f"Error running {self.tool_name}: {str(e)}\n"
            self.finished.emit(error_msg, self.tool_name)

    def remove_ansi_escape_codes(self, text):
        ansi_escape = re.compile(r'\x1B\[[0-?9;]*[mG]')
        return ansi_escape.sub('', text)

class ToolOutputWidget(QFrame):
    def __init__(self, tool_name):
        super().__init__()
        self.tool_name = tool_name
        self.initUI()
        
    def initUI(self):
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        
        layout = QVBoxLayout()
        
        # Header with tool name and close button
        header_layout = QHBoxLayout()
        self.title_label = QLabel(f"🔧 {self.tool_name}")
        self.title_label.setStyleSheet("font-weight: bold; color: #2E8B57; font-size: 12px;")
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setMaximumSize(20, 20)
        self.close_btn.setStyleSheet("QPushButton { background-color: #FF6B6B; color: white; border: none; border-radius: 10px; }")
        self.close_btn.clicked.connect(self.close_output)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_btn)
        
        # Output text area
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(200)
        self.output_text.setStyleSheet("QTextEdit { font-family: 'Courier New'; font-size: 9px; }")
        
        layout.addLayout(header_layout)
        layout.addWidget(self.output_text)
        self.setLayout(layout)
        
    def append_output(self, text):
        self.output_text.append(text.rstrip())
        # Auto-scroll to bottom
        cursor = self.output_text.textCursor()
        cursor.movePosition(cursor.End)
        self.output_text.setTextCursor(cursor)
        
    def close_output(self):
        self.setParent(None)
        self.deleteLater()

class Realtic(QWidget):
    def __init__(self):
        super().__init__()
        # Get the directory where this script is located
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.running_tools = {}  # Dictionary to track running tools
        self.temp_log_dir = None
        self.tool_log_files = {}  # Track individual tool log files
        self.initUI()
        self.mutex = QMutex()
        self.threads = []
        self.setup_temp_logging()

    def setup_temp_logging(self):
        """Setup temporary logging directory for individual tool logs"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_log_dir = os.path.join(tempfile.gettempdir(), f"realtic_logs_{timestamp}")
        os.makedirs(self.temp_log_dir, exist_ok=True)

    def create_tool_log_file(self, tool_name):
        """Create a temporary log file for a specific tool"""
        timestamp = datetime.datetime.now().strftime("%H%M%S")
        safe_tool_name = tool_name.replace(" ", "_").replace("/", "_")
        log_filename = f"{safe_tool_name}_{timestamp}.log"
        log_path = os.path.join(self.temp_log_dir, log_filename)
        
        # Initialize the log file
        with open(log_path, 'w') as f:
            f.write(f"=== {tool_name} Log ===\n")
            f.write(f"Started at: {datetime.datetime.now()}\n")
            f.write(f"Working Directory: {self.base_path}\n")
            f.write("=" * 50 + "\n\n")
        
        return log_path

    def log_to_tool_file(self, tool_name, output, log_file_path):
        """Log output to specific tool's log file"""
        try:
            with open(log_file_path, 'a') as f:
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                f.write(f"[{timestamp}] {output}")
                if not output.endswith('\n'):
                    f.write('\n')
        except Exception as e:
            print(f"Error writing to tool log file: {e}")

    def generate_consolidated_report(self):
        """Generate a consolidated report from all tool logs"""
        if not self.tool_log_files:
            QMessageBox.information(self, "Info", "No tool logs available to generate report.")
            return
        
        # Create consolidated report
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.base_path, f"Realtic_Consolidated_Report_{timestamp}.txt")
        
        try:
            with open(report_path, 'w') as report_file:
                # Write header
                report_file.write("REALTIC CONSOLIDATED ANALYSIS REPORT\n")
                report_file.write("=" * 60 + "\n")
                report_file.write(f"Generated at: {datetime.datetime.now()}\n")
                report_file.write(f"Number of tools executed: {len(self.tool_log_files)}\n")
                report_file.write("=" * 60 + "\n\n")
                
                # Write summary
                report_file.write("EXECUTION SUMMARY:\n")
                report_file.write("-" * 30 + "\n")
                for tool_name, log_data in self.tool_log_files.items():
                    status = "✓ Completed" if log_data.get('completed', False) else "⚠ Running/Incomplete"
                    duration = log_data.get('duration', 'Unknown')
                    report_file.write(f"• {tool_name}: {status}")
                    if duration != 'Unknown':
                        report_file.write(f" (Duration: {duration})")
                    report_file.write("\n")
                
                report_file.write("\n" + "=" * 60 + "\n\n")
                
                # Write detailed logs for each tool
                for tool_name, log_data in self.tool_log_files.items():
                    log_file_path = log_data['log_path']
                    if os.path.exists(log_file_path):
                        report_file.write(f"DETAILED LOG: {tool_name.upper()}\n")
                        report_file.write("=" * 60 + "\n")
                        
                        with open(log_file_path, 'r') as tool_log:
                            content = tool_log.read()
                            report_file.write(content)
                        
                        report_file.write("\n" + "=" * 60 + "\n\n")
                
                # Write footer
                report_file.write("END OF REPORT\n")
                report_file.write(f"Report generated by Realtic at {datetime.datetime.now()}\n")
            
            QMessageBox.information(self, "Success", 
                                  f"Consolidated report generated successfully!\n\nSaved to: {report_path}")
            
            # Offer to open the report
            reply = QMessageBox.question(self, "Open Report", 
                                       "Would you like to open the generated report?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.open_file_in_editor(report_path)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")

    def open_file_in_editor(self, file_path):
        """Open file in default text editor"""
        try:
            if sys.platform.startswith('linux'):
                subprocess.run(['xdg-open', file_path])
            elif sys.platform.startswith('darwin'):
                subprocess.run(['open', file_path])
            elif sys.platform.startswith('win'):
                os.startfile(file_path)
        except Exception as e:
            QMessageBox.warning(self, "Warning", f"Could not open file: {str(e)}")

    def view_temp_logs_folder(self):
        """Open the temporary logs folder"""
        if self.temp_log_dir and os.path.exists(self.temp_log_dir):
            self.open_file_in_editor(self.temp_log_dir)
        else:
            QMessageBox.information(self, "Info", "No temporary logs folder found.")

    def initUI(self):
        main_layout = QHBoxLayout()
        
        # Left panel for controls
        left_panel = QWidget()
        left_panel.setMaximumWidth(350)
        left_layout = QVBoxLayout()

        self.label = QLabel('Select a tool to run:', self)
        left_layout.addWidget(self.label)

        self.toolSelector = QComboBox(self)
        self.toolSelector.addItems(['Linear Trails', 'SHA1 Collision Detection', 'Break OTS', 'RSA CTF Tool', 'S-Box Gates'])
        self.toolSelector.currentIndexChanged.connect(self.toolChanged)
        left_layout.addWidget(self.toolSelector)

        self.fileLabel = QLabel('Select XML file for Linear Trails:', self)
        left_layout.addWidget(self.fileLabel)

        self.btn = QPushButton('Browse', self)
        self.btn.clicked.connect(self.openFileDialog)
        left_layout.addWidget(self.btn)

        # Add input fields for BreakOTS parameters
        self.p_input = QLineEdit(self)
        self.p_input.setPlaceholderText("Enter value for p")
        self.p_input.hide()
        left_layout.addWidget(self.p_input)

        self.w1_input = QLineEdit(self)
        self.w1_input.setPlaceholderText("Enter value for w1")
        self.w1_input.hide()
        left_layout.addWidget(self.w1_input)

        self.w2_input = QLineEdit(self)
        self.w2_input.setPlaceholderText("Enter value for w2")
        self.w2_input.hide()
        left_layout.addWidget(self.w2_input)

        self.delta_input = QLineEdit(self)
        self.delta_input.setPlaceholderText("Enter value for delta")
        self.delta_input.hide()
        left_layout.addWidget(self.delta_input)

        self.relax_input = QLineEdit(self)
        self.relax_input.setPlaceholderText("Enter value for relax")
        self.relax_input.hide()
        left_layout.addWidget(self.relax_input)

        self.threshold_input = QLineEdit(self)
        self.threshold_input.setPlaceholderText("Enter value for threshold")
        self.threshold_input.hide()
        left_layout.addWidget(self.threshold_input)

        self.maxBFround_input = QLineEdit(self)
        self.maxBFround_input.setPlaceholderText("Enter value for maxBFround")
        self.maxBFround_input.hide()
        left_layout.addWidget(self.maxBFround_input)

        # Logging and reporting options
        logging_frame = QFrame()
        logging_frame.setFrameStyle(QFrame.Box)
        logging_layout = QVBoxLayout()
        
        logging_label = QLabel("Logging & Reports:")
        logging_label.setStyleSheet("font-weight: bold; color: #333;")
        logging_layout.addWidget(logging_label)
        
        self.log_checkbox = QCheckBox("Enable individual tool logging")
        self.log_checkbox.setChecked(True)
        logging_layout.addWidget(self.log_checkbox)
        
        self.generate_report_btn = QPushButton('📄 Generate Consolidated Report')
        self.generate_report_btn.clicked.connect(self.generate_consolidated_report)
        self.generate_report_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 6px; }")
        logging_layout.addWidget(self.generate_report_btn)
        
        self.view_temp_logs_btn = QPushButton('📁 View Individual Logs Folder')
        self.view_temp_logs_btn.clicked.connect(self.view_temp_logs_folder)
        logging_layout.addWidget(self.view_temp_logs_btn)
        
        logging_frame.setLayout(logging_layout)
        left_layout.addWidget(logging_frame)

        self.runBtn = QPushButton('Run Tool', self)
        self.runBtn.clicked.connect(self.runTool)
        self.runBtn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 8px; }")
        left_layout.addWidget(self.runBtn)

        # Running tools status
        self.status_label = QLabel('Running tools: 0', self)
        self.status_label.setStyleSheet("color: #666; font-weight: bold;")
        left_layout.addWidget(self.status_label)

        # Stop all tools button
        self.stop_all_btn = QPushButton('Stop All Tools', self)
        self.stop_all_btn.clicked.connect(self.stop_all_tools)
        self.stop_all_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 8px; }")
        left_layout.addWidget(self.stop_all_btn)

        # View log button
        self.view_log_btn = QPushButton('📊 View Temp Logs Directory', self)
        self.view_log_btn.clicked.connect(self.view_temp_logs_folder)
        left_layout.addWidget(self.view_log_btn)

        left_layout.addStretch()
        left_panel.setLayout(left_layout)

        # Right panel for tool outputs
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        outputs_label = QLabel('Tool Outputs:')
        outputs_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        right_layout.addWidget(outputs_label)
        
        # Scroll area for tool outputs
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)
        right_layout.addWidget(self.scroll_area)
        
        right_panel.setLayout(right_layout)

        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        self.setWindowTitle('Realtic - Multi-Tool Cryptographic Analysis')
        self.setGeometry(100, 100, 1400, 900)
        self.show()

    def get_tool_path(self, tool_subpath):
        """Helper method to get the full path to a tool executable"""
        return os.path.join(self.base_path, tool_subpath)

    def toolChanged(self):
        if self.toolSelector.currentText() == 'Linear Trails':
            self.fileLabel.setText('Select XML file for Linear Trails:')
            self.btn.setText('Browse XML File')
            self.filePath = None
            self.hide_all_inputs()

        elif self.toolSelector.currentText() == 'SHA1 Collision Detection':
            self.fileLabel.setText('Select PDF files for SHA1 Collision Detection:')
            self.btn.setText('Browse PDF Files')
            self.hide_all_inputs()

        elif self.toolSelector.currentText() == 'Break OTS':
            self.fileLabel.setText('Select TXT file for BreakOTS:')
            self.btn.setText('Browse TXT File')
            self.show_breakots_inputs()
        
        elif self.toolSelector.currentText() == 'RSA CTF Tool':
            self.fileLabel.setText('Select PUB files for RSA CTF Tool:')
            self.btn.setText('Browse PUB Files')
            self.filePath = None
            self.hide_all_inputs()
            
        elif self.toolSelector.currentText() == 'S-Box Gates':
            self.fileLabel.setText('Select TXT file for S-Box Gates:')
            self.btn.setText('Browse TXT File')
            self.filePath = None
            self.hide_all_inputs()

    def hide_all_inputs(self):
        """Hide all input fields"""
        inputs = [self.p_input, self.w1_input, self.w2_input, self.delta_input, 
                 self.relax_input, self.threshold_input, self.maxBFround_input]
        for input_field in inputs:
            input_field.hide()

    def show_breakots_inputs(self):
        """Show BreakOTS input fields"""
        self.hide_all_inputs()
        inputs = [self.p_input, self.w1_input, self.w2_input, self.delta_input, 
                 self.relax_input, self.threshold_input, self.maxBFround_input]
        for input_field in inputs:
            input_field.show()

    def openFileDialog(self):
        options = QFileDialog.Options()
        if self.toolSelector.currentText() == 'Linear Trails':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select XML File", "", "XML Files (*.xml);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {os.path.basename(self.filePath)}')
        
        elif self.toolSelector.currentText() == 'SHA1 Collision Detection':
            self.pdfFiles, _ = QFileDialog.getOpenFileNames(self, "Select PDF Files", "", "PDF Files (*.pdf);;All Files (*)", options=options)
            if self.pdfFiles:
                self.fileLabel.setText(f'Selected: {len(self.pdfFiles)} PDF file(s)')
        
        elif self.toolSelector.currentText() == 'Break OTS':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select TXT File", "", "TXT Files (*.txt);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {os.path.basename(self.filePath)}')
        
        elif self.toolSelector.currentText() == 'RSA CTF Tool':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select PUB File", "", "PUB Files (*.pub);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {os.path.basename(self.filePath)}')
        
        elif self.toolSelector.currentText() == 'S-Box Gates':
            self.filePath, _ = QFileDialog.getOpenFileName(self, "Select TXT File", "", "TXT Files (*.txt);;All Files (*)", options=options)
            if self.filePath:
                self.fileLabel.setText(f'Selected: {os.path.basename(self.filePath)}')

    def create_tool_output_widget(self, tool_name):
        """Create a new output widget for a tool"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        widget_tool_name = f"{tool_name} ({timestamp})"
        
        output_widget = ToolOutputWidget(widget_tool_name)
        self.scroll_layout.addWidget(output_widget)
        
        # Create individual log file for this tool
        log_file_path = None
        if self.log_checkbox.isChecked():
            log_file_path = self.create_tool_log_file(tool_name)
            self.tool_log_files[tool_name] = {
                'log_path': log_file_path,
                'start_time': datetime.datetime.now(),
                'completed': False
            }
        
        # Store reference
        self.running_tools[tool_name] = {
            'widget': output_widget,
            'start_time': datetime.datetime.now(),
            'log_path': log_file_path
        }
        
        self.update_status()
        return output_widget

    def update_status(self):
        """Update the running tools status"""
        count = len(self.running_tools)
        self.status_label.setText(f'Running tools: {count}')

    def runTool(self):
        tool_name = self.toolSelector.currentText()
        
        if tool_name == 'Linear Trails':
            if not hasattr(self, 'filePath') or not self.filePath:
                QMessageBox.warning(self, "Warning", "Please select an XML file first!")
                return
            self.run_linear_trails()
            
        elif tool_name == 'SHA1 Collision Detection':
            if not hasattr(self, 'pdfFiles') or not self.pdfFiles:
                QMessageBox.warning(self, "Warning", "Please select PDF files first!")
                return
            self.run_sha1_detection()
            
        elif tool_name == 'Break OTS':
            if not hasattr(self, 'filePath') or not self.filePath:
                QMessageBox.warning(self, "Warning", "Please select a TXT file first!")
                return
            if not self.validate_breakots_inputs():
                return
            self.run_break_ots()
            
        elif tool_name == 'RSA CTF Tool':
            if not hasattr(self, 'filePath') or not self.filePath:
                QMessageBox.warning(self, "Warning", "Please select a PUB file first!")
                return
            self.run_rsa_ctf_tool()
            
        elif tool_name == 'S-Box Gates':
            if not hasattr(self, 'filePath') or not self.filePath:
                QMessageBox.warning(self, "Warning", "Please select a TXT file first!")
                return
            self.run_sbox_gates()

    def validate_breakots_inputs(self):
        """Validate BreakOTS input fields"""
        inputs = [self.p_input, self.w1_input, self.w2_input, self.delta_input, 
                 self.relax_input, self.threshold_input, self.maxBFround_input]
        
        for input_field in inputs:
            if not input_field.text().strip():
                QMessageBox.warning(self, "Warning", f"Please fill in all BreakOTS parameters!")
                return False
        return True

    def run_linear_trails(self):
        tool_name = "Linear Trails"
        linear_trails_path = self.get_tool_path('Linear_Trails/lin')
        command = ['timeout', '30', linear_trails_path, '-I', '10', '-S', '2', '-i', self.filePath]
        self.start_tool_thread(command, tool_name)

    def run_sha1_detection(self):
        tool_name = "SHA1 Collision Detection"
        sha1_tool_path = self.get_tool_path('SHA1_Collision_Detection/bin/sha1dcsum')
        command = [sha1_tool_path] + self.pdfFiles
        self.start_tool_thread(command, tool_name)

    def run_break_ots(self):
        tool_name = "Break OTS"
        breakots_path = self.get_tool_path('Persichetti_OTS_CryptAnalysis/breakOTS')
        command = [breakots_path, self.p_input.text(), self.w1_input.text(), 
                  self.w2_input.text(), self.delta_input.text(), self.relax_input.text(), 
                  self.filePath, self.threshold_input.text(), self.maxBFround_input.text()]
        self.start_tool_thread(command, tool_name)

    def run_rsa_ctf_tool(self):
        tool_name = "RSA CTF Tool"
        rsa_tool_path = self.get_tool_path('RSA_CTF_Tool/RsaCtfTool.py')
        command = ['python3', rsa_tool_path, '--publickey', self.filePath, '--private']
        self.start_tool_thread(command, tool_name)

    def run_sbox_gates(self):
        tool_name = "S-Box Gates"
        sboxgates_path = self.get_tool_path('S-Box_Gates/build/sboxgates')
        command = [sboxgates_path, self.filePath]
        self.start_tool_thread(command, tool_name)

    def start_tool_thread(self, command, tool_name):
        """Start a new thread for running a tool"""
        # Create output widget
        output_widget = self.create_tool_output_widget(tool_name)
        
        # Start worker thread
        worker = WorkerThread(command, tool_name)
        worker.progress.connect(self.handle_tool_progress)
        worker.finished.connect(self.handle_tool_finished)
        worker.finished.connect(lambda: self.cleanup_thread(worker))
        
        self.threads.append(worker)
        worker.start()
        
        # Log start to individual file
        if self.log_checkbox.isChecked() and output_widget:
            log_path = self.running_tools[tool_name]['log_path']
            if log_path:
                self.log_to_tool_file(tool_name, f"Command: {' '.join(command)}\n", log_path)
                self.log_to_tool_file(tool_name, "Output:\n", log_path)

    def handle_tool_progress(self, output, tool_name):
        """Handle real-time output from tools"""
        if tool_name in self.running_tools:
            self.running_tools[tool_name]['widget'].append_output(output)
            
            # Log to individual tool file
            if self.log_checkbox.isChecked():
                log_path = self.running_tools[tool_name]['log_path']
                if log_path:
                    self.log_to_tool_file(tool_name, output, log_path)

    def handle_tool_finished(self, final_output, tool_name):
        """Handle when a tool finishes"""
        if tool_name in self.running_tools:
            if final_output:
                self.running_tools[tool_name]['widget'].append_output(final_output)
            
            self.running_tools[tool_name]['widget'].append_output(f"\n--- {tool_name} completed ---\n")
            
            # Log completion to individual file
            if self.log_checkbox.isChecked():
                log_path = self.running_tools[tool_name]['log_path']
                if log_path and tool_name in self.tool_log_files:
                    end_time = datetime.datetime.now()
                    start_time = self.tool_log_files[tool_name]['start_time']
                    duration = end_time - start_time
                    
                    self.log_to_tool_file(tool_name, f"\n--- Tool completed ---\n", log_path)
                    self.log_to_tool_file(tool_name, f"End time: {end_time}\n", log_path)
                    self.log_to_tool_file(tool_name, f"Total duration: {duration}\n", log_path)
                    
                    # Update tool log metadata
                    self.tool_log_files[tool_name]['completed'] = True
                    self.tool_log_files[tool_name]['duration'] = str(duration)
            
            # Remove from running tools
            del self.running_tools[tool_name]
            self.update_status()

    def cleanup_thread(self, worker):
        """Clean up finished threads"""
        if worker in self.threads:
            self.threads.remove(worker)

    def stop_all_tools(self):
        """Stop all running tools"""
        for thread in self.threads[:]:  # Copy list to avoid modification during iteration
            thread.terminate()
            thread.wait(3000)  # Wait up to 3 seconds
            if thread.isRunning():
                thread.kill()
        
        self.threads.clear()
        self.running_tools.clear()
        self.update_status()
        
        # Clear all output widgets
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

    def cleanup_on_close(self):
        """Clean up temporary files when application closes"""
        try:
            # Optionally clean up temp directory
            # Uncomment the next lines if you want to delete temp logs on close
            # if self.temp_log_dir and os.path.exists(self.temp_log_dir):
            #     shutil.rmtree(self.temp_log_dir)
            pass
        except Exception as e:
            print(f"Error during cleanup: {e}")

    def closeEvent(self, event):
        """Handle application close"""
        self.stop_all_tools()
        self.cleanup_on_close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Realtic()
    sys.exit(app.exec_())

