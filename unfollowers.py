import sys
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QMessageBox
)

class FollowerComparator(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Instagram Unfollowers Checker")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label1 = QLabel("Selecciona el archivo ANTIGUO (.csv)")
        layout.addWidget(self.label1)

        self.btn1 = QPushButton("Cargar archivo antiguo")
        self.btn1.clicked.connect(self.load_old_file)
        layout.addWidget(self.btn1)

        self.label2 = QLabel("Selecciona el archivo NUEVO (.csv)")
        layout.addWidget(self.label2)

        self.btn2 = QPushButton("Cargar archivo nuevo")
        self.btn2.clicked.connect(self.load_new_file)
        layout.addWidget(self.btn2)

        self.compare_btn = QPushButton("Comparar followers")
        self.compare_btn.clicked.connect(self.compare_files)
        layout.addWidget(self.compare_btn)

        self.setLayout(layout)

        self.old_file = None
        self.new_file = None

    def load_old_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo antiguo", "", "CSV Files (*.csv)")
        if file:
            self.old_file = file
            self.label1.setText(f"Antiguo: {file}")

    def load_new_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Selecciona archivo nuevo", "", "CSV Files (*.csv)")
        if file:
            self.new_file = file
            self.label2.setText(f"Nuevo: {file}")

    def compare_files(self):
        if not self.old_file or not self.new_file:
            QMessageBox.warning(self, "Error", "Debes seleccionar ambos archivos.")
            return

        df_old = pd.read_csv(self.old_file)
        df_new = pd.read_csv(self.new_file)

        old_usernames = set(df_old["Username"].str.lower())
        new_usernames = set(df_new["Username"].str.lower())

        unfollowers = sorted(old_usernames - new_usernames)
        new_followers = sorted(new_usernames - old_usernames)

        message = f"👋 Unfollowers detectados: {len(unfollowers)}\n"
        message += "\n".join(unfollowers[:10])  # Muestra solo los primeros 10
        if len(unfollowers) > 10:
            message += f"\n... y {len(unfollowers) - 10} más"

        QMessageBox.information(self, "Resultado", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FollowerComparator()
    window.show()
    sys.exit(app.exec_())
