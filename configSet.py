import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QSpinBox, QPushButton, QScrollArea,QLineEdit,QCheckBox
from PyQt5.QtCore import Qt
import yaml
import os
import shutil
from datetime import datetime

from config_module import create_default_config

class ConfigEditor(QMainWindow):
    def __init__(self):
        super(ConfigEditor, self).__init__()

        self.WGarray=[]

        self.setWindowTitle("Config Editor")
        self.setGeometry(48, 48, 1000, 1000)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a scroll area to handle too much content
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.central_widget.setLayout(QVBoxLayout())
        self.central_widget.layout().addWidget(self.scroll_area)

        # Create a widget to hold your content
        self.scroll_content_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_content_widget)

        self.layout = QVBoxLayout(self.scroll_content_widget)

        self.config_data = self.load_config()

        self.create_widgets_from_config(self.config_data)
        self.cWFC_after_burn()

        self.backup_button = QPushButton("Backup")
        self.backup_button.clicked.connect(self.backup_config)
        self.layout.addWidget(self.backup_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_button)

    def add_title(self,parent,group_box,key,color):
        # Recursive call for nested structures
        group_box = QWidget(parent)
        group_layout = QVBoxLayout(group_box)

        # Add title with background color
        title_label = QLabel(key)
        title_label.setStyleSheet('background-color: '+color+';')
        group_layout.addWidget(title_label)
        return group_box

    def create_widgets_from_config(self, config_data, parent=None):
        for key, value in config_data.items():
            label = QLabel(key)
            spin_box = QSpinBox()

            if isinstance(value, int):
                spin_box.setValue(value)
            elif isinstance(value, list) and all(isinstance(v, int) for v in value):
                spin_box.setValue(value[0])
            elif isinstance(value, dict):
                # Recursive call for nested structures
                group_box = QWidget(parent)
                group_layout = QVBoxLayout(group_box)

                # Add title with background color
                title_label = QLabel(key)
                title_label.setStyleSheet("background-color: pink;")
                group_layout.addWidget(title_label)

                self.WGarray.append(self.add_title(parent,group_box,'end of group','green'))

                self.create_widgets_from_config(value, parent=group_box)
                self.WGarray.append(group_box)
                continue
            else:
                spin_box.setValue(0)

            spin_box.setAlignment(Qt.AlignRight)
            spin_box.valueChanged.connect(lambda val, k=key: self.update_config(k, val))

            #self.layout.addWidget(label)
            if isinstance(value,str):
                txt_box = QLineEdit()
                txt_box.setText(value)
                self.WGarray.append(txt_box)
            elif isinstance(value,bool):
                checkbox = QCheckBox('Enable Feature')
                checkbox.setChecked(value)
                self.WGarray.append(checkbox)
            else:
                self.WGarray.append(spin_box)
            self.WGarray.append(label)
            #self.layout.addWidget(spin_box)

    def cWFC_after_burn(self):
        for x in reversed(self.WGarray):
            self.layout.addWidget(x)
            if isinstance(x, QWidget):
                # Assuming x is a QWidget, check for QVBoxLayout
                layout = x.layout()
                if isinstance(layout, QVBoxLayout):
                    # Assuming QVBoxLayout is found, check for QLabel with pink background color
                    for i in range(layout.count()):
                        item = layout.itemAt(i)
                        if isinstance(item.widget(), QLabel) and item.widget().styleSheet().strip() == "background-color: pink;":
                            print("pink!")

    def load_config(self):
        if not os.path.exists("config.yaml"):
            self.create_default_config()

        with open("config.yaml", "r") as file:
            config_data = yaml.safe_load(file)
        return config_data

    def create_default_config(self):
        # Call the function to create the default configuration
        create_default_config()


    def update_config(self, key, value):
        print(f"Updating config: {key} - {value}")
        self.config_data[key] = value

    def save_config(self):
        with open("config.yaml", "w") as file:
            yaml.dump(self.config_data, file, default_flow_style=False)

    def backup_config(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_directory = "./.autobackup"
        backup_path = f"{backup_directory}/config{timestamp}.yaml"

        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        shutil.copyfile("config.yaml", backup_path)
        print(f"Backup saved to: {backup_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = ConfigEditor()
    editor.show()
    sys.exit(app.exec_())
