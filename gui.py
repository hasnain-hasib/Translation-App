import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit


class MyGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connected = False
        self.init_ui()

    def init_ui(self):
        # Set up window dimensions
        window_width = self.frameGeometry().width()
        window_height = self.frameGeometry().height()
        
        # Create label to display "Enter text:"

        label_width = 200
        label_height = 30
        label_x = int((window_width - label_width) / 2)
        label_y = int((window_height - label_height) / 2 - 50)

        self.label = QLabel("Enter text:", self)
        self.label.setGeometry(label_x, label_y, label_width, label_height)

        
        # Create textbox for entering text
        
        
        textbox_width = 200
        textbox_height = 30
        textbox_x = int((window_width - textbox_width) / 2)
        textbox_y = int((window_height - textbox_height) / 2 - 20)

        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(textbox_x, textbox_y, textbox_width, textbox_height)
        self.textbox.textChanged.connect(self.detect_language)

        # Create translate button

        button_width = 100
        button_height = 30
        button_x = int((window_width - button_width) / 2)
        button_y = int((window_height - button_height) / 2 + 20)

        self.translate_button = QPushButton("Translate", self)
        self.translate_button.setGeometry(button_x, button_y, button_width, button_height)
        self.translate_button.clicked.connect(self.translate_text)

        # Create label to display translation result

        translation_label_width = 200
        translation_label_height = 30
        translation_label_x = int((window_width - translation_label_width) / 2)
        translation_label_y = int((window_height - translation_label_height) / 2 + 50)
        self.translation_label = QLabel("", self)
        self.translation_label.setGeometry(translation_label_x, translation_label_y, translation_label_width, translation_label_height)

        #Create server address textbox

        server_address_width = 200
        server_address_height = 30
        server_address_x = int((window_width - server_address_width) / 2)
        server_address_y = int((window_height - server_address_height) / 2 + 100)
        self.server_address_textbox = QLineEdit(self)
        self.server_address_textbox.setGeometry(server_address_x, server_address_y, server_address_width, server_address_height)
        
        # Create connect button
        connect_button_width = 100
        connect_button_height = 30
        connect_button_x = int((window_width - connect_button_width) / 2)
        connect_button_y = int((window_height - connect_button_height) / 2 + 140)
        self.connect_button = QPushButton("Connect", self)
        self.connect_button.setGeometry(connect_button_x, connect_button_y, connect_button_width, connect_button_height)
        self.connect_button.clicked.connect(self.connect_to_server)
        
        # Create "Enter Adress Label"
        
        
        server_address_label_width = 120
        server_address_label_height = 30
        server_address_label_x = server_address_x - server_address_label_width - 10
        server_address_label_y = server_address_y
        self.server_address_label = QLabel("Enter address:", self)
        self.server_address_label.setGeometry(server_address_label_x, server_address_label_y, server_address_label_width, server_address_label_height)

        # Create exit button

        self.exit_button = QPushButton("Exit", self)
        button_width = self.exit_button.sizeHint().width()
        button_height = self.exit_button.sizeHint().height()
        self.exit_button.setGeometry(int((window_width - button_width) / 2), int(self.height() - button_height - 10), button_width, button_height)
        self.exit_button.clicked.connect(self.exit_application)


        # Window title
        
        self.setWindowTitle("Translation GUI")
        self.setGeometry(100, 100, 700, 500)


    # function for server adress varification and taking server address
    
    def connect_to_server(self):
        server_address = self.server_address_textbox.text()
        if server_address.startswith("http://") or server_address.startswith("https://"):
            self.connected = True
            self.translation_label.setText(f"Connected to server: {server_address}")
        else:
            self.connected = False
            self.translation_label.setText("Enter a valid address something liek this  !!  http://localhost:8000")

    # function for detecting language 
    def detect_language(self, text):
        if self.connected:
            if text:
                language_detection_response = requests.post(f"{self.server_address_textbox.text()}/language-detection", json={"text": text})
                if language_detection_response.status_code == 200:
                    language_data = language_detection_response.json()
                    detected_language = language_data.get("language")
                    self.translation_label.setText(f"Detected Language: {detected_language}")
                else:
                    self.translation_label.setText("Language detection failed")
            else:
                self.translation_label.setText("")
        else:
            self.translation_label.setText("Not connected to the server")
            
    # function for actual translation
    
    def translate_text(self):
        if self.connected:
            text = self.textbox.text()
            if text:
                translation_response = requests.post(f"{self.server_address_textbox.text()}/translate", json={"text": text})
                if translation_response.status_code == 200:
                    translation_data = translation_response.json()
                    translation = translation_data.get("translation")
                    self.translation_label.setText(f"Translation: {translation}")
                else:
                    self.translation_label.setText("Translation failed")
            else:
                self.translation_label.setText("")

    # function for exit button 
    
    def exit_application(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    my_gui = MyGUI()
    my_gui.show()

    sys.exit(app.exec_())
