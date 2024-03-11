import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QSpinBox, QPushButton
from PyQt5.QtCore import Qt
import yaml
import os
import shutil
from datetime import datetime

class ConfigEditor(QMainWindow):
    def __init__(self):
        super(ConfigEditor, self).__init__()

        self.setWindowTitle("Config Editor")
        self.setGeometry(100, 100, 400, 400)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.config_data = self.load_config()

        for key, value in self.config_data.items():
            label = QLabel(key)
            spin_box = QSpinBox()

            if isinstance(value, int):
                spin_box.setValue(value)
            elif isinstance(value, list) and all(isinstance(v, int) for v in value):
                spin_box.setValue(value[0])
            else:
                spin_box.setValue(0)

            spin_box.setAlignment(Qt.AlignRight)
            spin_box.valueChanged.connect(lambda val, k=key: self.update_config(k, val))

            self.layout.addWidget(label)
            self.layout.addWidget(spin_box)

        self.backup_button = QPushButton("Backup")
        self.backup_button.clicked.connect(self.backup_config)
        self.layout.addWidget(self.backup_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_config)
        self.layout.addWidget(self.save_button)

        self.central_widget.setLayout(self.layout)

    def load_config(self):
        if not os.path.exists("config.yaml"):
            self.create_default_config()

        with open("config.yaml", "r") as file:
            config_data = yaml.safe_load(file)
        return config_data

    def create_default_config(self):
        default_config = {
            "seed": 1234,
            "trainer": {
                "gpus": 1,
                "overfit_batches": 0.0,
                "check_val_every_n_epoch": 1,
                "fast_dev_run": False,
                "max_epochs": 1,
                "min_epochs": 1,
                "num_sanity_val_steps": 0,
                "auto_lr_find": False,
                "checkpoint_callback": True
            },
            "callbacks": {
                "model_checkpoint": {
                    "save_top_k": 1,
                    "save_weights_only": True,
                    "mode": "min",
                    "monitor": "val/loss",
                    "filename": "{epoch}-{val/loss:.2f}-{val/cer:.2f}"
                },
                "early_stopping": {
                    "patience": 3,
                    "mode": "min",
                    "monitor": "val/loss",
                    "min_delta": 0.001
                }
            },
            "data": {
                "batch_size": 32,
                "num_workers": 4,
                "pin_memory": False
            },
            "lit_model": {
                "lr": 0.001,
                "weight_decay": 0.0001,
                "milestones": [10],
                "gamma": 0.5,
                "d_model": 128,
                "dim_feedforward": 256,
                "nhead": 4,
                "dropout": 0.3,
                "num_decoder_layers": 3,
                "max_output_len": 150
            },
            "logger": {
                "project": "image-to-latex"
            }
        }

        with open("config.yaml", "w") as file:
            yaml.dump(default_config, file, default_flow_style=False)


    def update_config(self, key, value):
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
