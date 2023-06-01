import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSpinBox, QPushButton, \
    QDialog, QLabel, QLineEdit, QVBoxLayout, QDialogButtonBox, QHBoxLayout
from io import StringIO
import Jeux
from interface import Ui_MainWindow
from dialogue_joueur import Ui_Dialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dialogues_joueurs = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionCommencer.triggered.connect(self.commencer)
        self.joueurs = []
        self.creature = None
        self.nombre_joueurs = None

    def commencer(self):
        # Afficher le menu pour choisir le nombre de joueurs
        self.menu_joueurs = QWidget()
        layout = QVBoxLayout(self.menu_joueurs)
        label = QLabel("Nombre de joueurs : ", self.menu_joueurs)
        layout.addWidget(label)
        self.spin_box = QSpinBox(self.menu_joueurs)
        self.spin_box.setMinimum(2)
        self.spin_box.setMaximum(7)
        layout.addWidget(self.spin_box)
        button = QPushButton("Valider", self.menu_joueurs)
        button.clicked.connect(self.valider_joueurs)
        layout.addWidget(button)
        self.setCentralWidget(self.menu_joueurs)

    def valider_joueurs(self):
        # Récupérer le nombre de joueurs
        self.nombre_joueurs = self.spin_box.value()

        # Fermer le menu des joueurs
        self.menu_joueurs.close()

        # Ouvrir les boîtes de dialogue pour les noms des joueurs
        self.dialogues_joueurs = []
        self.ouvrir_boite_dialogue_joueur(0, self.nombre_joueurs)

    def ouvrir_boite_dialogue_joueur(self, index, nombre_joueurs):
        if index >= nombre_joueurs:
            # Tous les joueurs ont entré leurs noms, ouvrir la boîte de dialogue pour la créature
            self.ouvrir_boite_dialogue_creature()
            return

        dialog = QDialog(self)
        dialog_ui = Ui_Dialog()
        dialog_ui.setupUi(dialog)

        def enregistrer_nom():
            nom_joueur = dialog_ui.lineEdit.text()
            self.joueurs.append(nom_joueur)
            dialog.close()
            self.ouvrir_boite_dialogue_joueur(index + 1, nombre_joueurs)

        dialog_ui.buttonBox.accepted.connect(enregistrer_nom)
        self.dialogues_joueurs.append(dialog)
        dialog.show()

    def ouvrir_boite_dialogue_creature(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Créature")
        layout = QVBoxLayout(dialog)
        label = QLabel("Qui est la créature ?", dialog)
        layout.addWidget(label)
        line_edit = QLineEdit(dialog)
        layout.addWidget(line_edit)
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
        layout.addWidget(button_box)

        def enregistrer_creature():
            nom_creature = line_edit.text()
            # Faire quelque chose avec le nom de la créature
            self.creature = nom_creature
            dialog.close()
            self.commencer_partie()

        button_box.accepted.connect(enregistrer_creature)
        button_box.rejected.connect(dialog.reject)
        dialog.exec_()

    def commencer_partie(self):
        self.close()
        sys.stdin = StringIO(self.creature)
        Jeu = Jeux.Jeux(self.nombre_joueurs, self.joueurs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
