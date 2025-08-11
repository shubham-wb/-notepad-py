import sys, os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, \
                            QPushButton, QLabel, QPlainTextEdit, QVBoxLayout, QFileDialog, QMessageBox
from PySide6.QtCore import Qt, QSize                          
from PySide6.QtGui import QFontDatabase, QIcon, QKeySequence, QAction
from PySide6.QtPrintSupport import QPrintDialog

class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('./icons/notepad.ico'))
        self.screen_width, self.screen_height = self.geometry().width(), self.geometry().height()
        self.resize(self.screen_width * 2, self.screen_height * 2) 

        self.filterTypes = 'Text Document (*.txt);; Python (*.py);; Markdown (*.md)'

        self.path = None

        fixedFont = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        fixedFont.setPointSize(12)

        mainLayout = QVBoxLayout()

        # editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(fixedFont)
        mainLayout.addWidget(self.editor)

        # stautsBar
        self.statusBar = self.statusBar()

        # app container
        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        #----------------------------------
        # File Menu
        #----------------------------------
        file_menu = self.menuBar().addMenu('&File')

        """
        open, save, saveAs
        """
        open_file_action = QAction(QIcon('./icons/open.ico'), 'Open File', self)
        open_file_action.setStatusTip('Open file')
        open_file_action.setShortcut(QKeySequence.StandardKey.Open)
        open_file_action.triggered.connect(self.file_open) #TODO

        save_file_action = self.create_action(self, './icons/save_file.ico', 'Save File', 'Save file', self.file_save)
        save_file_action.setShortcut(QKeySequence.StandardKey.Save)

        save_fileAs_action = self.create_action(self, './icons/save_as.ico', 'Save As', 'Save as', self.file_saveAs)
        save_fileAs_action.setShortcut(QKeySequence('Ctrl+Shift+S'))

        file_menu.addActions([open_file_action, save_file_action, save_fileAs_action])
        
        # Print Action (Print Document)
        print_action = self.create_action(self, './icons/printer.ico', 'Print File', 'Print file', self.print_file)
        print_action.setShortcut(QKeySequence.StandardKey.Print)
        file_menu.addAction(print_action)
      
        #----------------------------------
        # Edit Menu
        #----------------------------------
        edit_menu = self.menuBar().addMenu('&Edit')


        # Undo, Redo Actions
        undo_action = self.create_action(self, './icons/undo.ico', 'Undo', 'Undo', self.editor.undo)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)

        redo_action = self.create_action(self, './icons/redo.ico', 'Redo', 'Redo', self.editor.redo)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)

        edit_menu.addActions([undo_action, redo_action])


        # Clear action
        clear_action = self.create_action(self, './icons/cleaning.ico', 'Clear', 'Clear', self.clear_content)
        edit_menu.addAction(clear_action)


        # add separator
        edit_menu.addSeparator()


        # cut, copy, paste, select all
        cut_action = self.create_action(self, './icons/cut.ico', 'Cut', 'Cut', self.editor.cut)
        copy_action = self.create_action(self, './icons/copy.ico', 'Copy', 'Copy', self.editor.copy)
        paste_action = self.create_action(self, './icons/paste.ico', 'Paste', 'Paste', self.editor.paste)
        select_all_action = self.create_action(self, './icons/select text.ico', 'Select All', 'Select all', self.editor.selectAll)

        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)

        edit_menu.addActions([cut_action, copy_action, paste_action, select_all_action])
      
      
        # add separator
        edit_menu.addSeparator()
      
      
        # wrap text
        wrap_text_action = self.create_action(self, './icons/wrap_text.ico', 'Wrap Text', 'Wrap text', self.toggle_wrap_text)
        wrap_text_action.setShortcut('Ctrl+Shift+W')
        edit_menu.addAction(wrap_text_action)
        

        self.update_title()

    def toggle_wrap_text(self):
        self.editor.setLineWrapMode(not self.editor.lineWrapMode())

    def clear_content(self):
        self.editor.setPlainText('')

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            parent=self,
            filter=self.filterTypes
        )

        if path:
            try:    
                with open(path, 'r') as f:
                    text = f.read()
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            self.file_saveAs()
        else:
            try:
                text = self.editor.toPlainText()
                with open(self.path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e:  
                self.dialog_message(str(e))

    def file_saveAs(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            'Save file as',
            '',
            self.filterTypes
        )                               

        text = self.editor.toPlainText()

        if not path:
            return
        else:
            try:
                with open(path, 'w') as f:
                    f.write(text)
                    f.close()
            except Exception as e:
                self.dialog_message(str(e))
            else:
                self.path = path
                self.update_title()

    def print_file(self):
        printDialog = QPrintDialog()
        if printDialog.exec():
            self.editor.print_(printDialog.printer())

    def update_title(self):
        self.setWindowTitle('{0} - NotepadX'.format(os.path.basename(self.path) if self.path else 'Unittled'))

    def dialog_message(self, message):
        dlg = QMessageBox(self)
        dlg.setText(message)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()

    def create_action(self, parent, icon_path, action_name, set_status_tip, triggered_method)   :
        action = QAction(QIcon(icon_path), action_name, parent)
        action.setStatusTip(set_status_tip)
        action.triggered.connect(triggered_method)
        return action



app = QApplication(sys.argv)
notepad = AppDemo()
notepad.show()
sys.exit(app.exec())
