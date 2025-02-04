from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QListWidget, QLineEdit, QInputDialog
from PyQt5.QtGui import QFont
import json
import sys

NOTES_FILE = "notes.json"

class Quiz_app(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = self.load_notes()

        self.setWindowTitle('Quiz App')
        self.resize(600, 800)

        ##Settings
        self.title_field = QLineEdit(self)
        self.content_field = QTextEdit(self)
        
        self.layout = QVBoxLayout()
        self.search_bar = QLineEdit(self)

        self.search_bar.setPlaceholderText("Search notes here....")
        self.search_bar.textChanged.connect(self.search_notes)
        self.layout.addWidget(self.search_bar)

        self.notes_list = QListWidget(self)
        self.notes_list.itemClicked.connect(self.display_notes)
        self.layout.addWidget(self.notes_list)

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)  

        self.add_button = QPushButton("Add note")
        self.add_button.clicked.connect(self.add_notes)  
        self.layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit note")
        self.edit_button.clicked.connect(self.edit_notes)
        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete note")
        self.delete_button.clicked.connect(self.delete_notes)
        self.layout.addWidget(self.delete_button)

        self.save_button = QPushButton("Save note")
        self.save_button.clicked.connect(self.save_notes)
        self.layout.addWidget(self.save_button)

        self.setLayout(self.layout)
        self.notes = self.load_notes()
        self.list_notes()


    def add_notes(self):
        title, ok = QInputDialog.getText(self, "New_note", "Enter the note title:")   
        if ok and title:
            if title in self.notes:
                QInputDialog.warning(self, "Error", "The note title already exist!!")
                return 
            self.notes[title] = ''
            self.save_notes()
            self.list_notes()

    def save_notes(self):
        title = self.title_field.text()
        content = self.content_field.toPlainText()
        if content and title:
            with open(f"{title}.txt", "w") as file: file .write(f"Title: {title} \n") 
            file.write(f"Content: {content}\n")
            print("Note saved successfully")
        else: 
            print('Title or content cannot be empty.')
                                                    

            

   
            
        


    def load_notes(self):#Load notes from JSON file
        try:
            with open(NOTES_FILE, "r") as file: return json.load(file)
                
                
        except(FileNotFoundError, json.JSONDecodeError):
            return{}

    def list_notes(self):      #List all notes in the QListWidget   
        self.notes_list.clear()
        for title in self.notes:
            self.notes_list.addItem(title)

    def display_notes(self, item):    #Load the selected note in the text edit
        title = item.text()
        self.text_edit.setText(self.notes.get(title, ""))

    def edit_notes(self):
        item = self.notes_list.currentItem()
        if item:
            title = item.text()
            self.notes[title] = self.text_edit.toPlainText()
            self.save_notes()

    def delete_notes(self):
        item = self.notes_list.currentItem()
        if item:
            title = item.text()
            
            del self.notes[title]
            self.save_notes()
            self.list_notes()
            self.text_edit.clear()

    def search_notes(self):
        query = self.search_bar.text().lower()
        self.notes_list.clear()
        for title in self.notes:
            if query in title.lower():
                self.notes_list.addItem(title)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Quiz_app() 
    window.show()
    sys.exit(app.exec_())







        
                
                
            
            