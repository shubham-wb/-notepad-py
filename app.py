import fileinput
import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QPlainTextEdit, QStatusBar, QToolBar, QVBoxLayout, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFontDatabase, QIcon, QKeySequence, QAction
from PySide6.QtPrintSupport import QPrintDialog

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("./icons/notepad.ico"))
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width , self.screen_height)
        self.filterTypes = "Text Document (*.txt);; Python (*.py);; Markdown (*.md)"
        self.path = None

        fixed_font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        fixed_font.setPointSize(12)
        
        main_layout = QVBoxLayout()

        #editor

        self.editor = QPlainTextEdit()
        self.editor.setFont(fixed_font)
        main_layout.addWidget(self.editor)

#statusbar
        self.statusbar = self.statusBar()

#app container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
#---------------------
# File Menus
#----------------------

        file_menu = self.menuBar().addMenu("&File")
#---------------------
# File Toolbar
#----------------------
        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(60,60))
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, file_toolbar)

        open_file_action = self.create_action(self,"./icons/open-folder.ico", "Open File", "Open File",self.file_open)
        open_file_action.setShortcut(QKeySequence.StandardKey.Open)

        save_file_action = self.create_action(self,"./icons/save_file.ico","Save","Save",self.file_save())
        save_file_action.setShortcut(QKeySequence.StandardKey.Save)

        save_file_as_action = self.create_action(self,"./icons/save_file.ico","Save as","Save as",self.file_save_as())
        save_file_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)

        print_file_action = self.create_action(self, './icons/printer.ico', 'Print File', 'Print File',lambda:print("Print File"))
        print_file_action.setShortcut(QKeySequence.StandardKey.Print)

        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addAction(save_file_as_action)
        file_menu.addAction(print_file_action)

        self.update_title()



    def file_save(self):
        if self.path is None:
            self.file_save_as()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, "w") as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
    def file_save_as(self):
        path , _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            self.filterTypes
        )
        text = self.editor.toPlainText()
        if not path:
            return
        else:
            try:
                with open(path, "w") as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()


    def update_title(self):
        self.setWindowTitle('{0} - NotepadX'.format(os.path.basename(self.path) if self.path else "Untitled"))
    def dialog_message(self , message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.exec()



    def file_open(self):
        path,_ = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open File",
            filter = self.filterTypes,

        )
        if path:
            try:
                with open(path, "r") as file:
                    text = file.read()
                    file.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()
    def create_action (self , parent , icon_path, action_name , set_status_tip, triggered_method):
        action = QAction(QIcon(icon_path), action_name , parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action

app = QApplication(sys.argv)
notePad = AppDemo()
notePad.show()
sys.exit(app.exec())