import os
import pickle
import sys

import PyQt5
import joblib
import numpy as np
from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPainter, QImage, QPen
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QPushButton, QWidget, QInputDialog, QFileDialog
from matplotlib import pyplot as plt

from downloadDatabase import downloadBase


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selected_model = None
        self.selected_base = None
        self.model = None
        self.fitted = False
        self.mnist = None
        self.X = None
        self.y = None

        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None

        # Create the menu bar
        menubar = self.menuBar()

        # Create the Model menu and add actions to it
        model_menu = menubar.addMenu("Model")
        nowy_action = QAction("Nowy", self)
        zapisz_action = QAction("Zapisz", self)
        wczytaj_action = QAction("Wczytaj", self)
        model_menu.addAction(nowy_action)
        model_menu.addAction(zapisz_action)
        model_menu.addAction(wczytaj_action)

        # Create the Baza menu and add actions to it
        baza_menu = menubar.addMenu("Baza")
        wczytaj_baze_action = QAction("Wczytaj", self)
        pobierz_action = QAction("Pobierz", self)
        baza_menu.addAction(wczytaj_baze_action)
        baza_menu.addAction(pobierz_action)

        # Connect the actions to their respective methods
        nowy_action.triggered.connect(self.nowy_model)
        zapisz_action.triggered.connect(self.zapisz_model)
        wczytaj_action.triggered.connect(self.wczytaj_model)
        pobierz_action.triggered.connect(self.pobierz_baze)
        wczytaj_baze_action.triggered.connect(self.wczytaj_baze)

        # Add to the menu bar dummy buttons with
        # text about selected base and model

        self.selected_model_label = QAction(f"Wybrany model: {self.selected_model}", self)
        self.selected_model_label.setEnabled(False)

        self.selected_base_label = QAction(f"Wybrana baza: {self.selected_base}", self)
        self.selected_base_label.setEnabled(False)

        menubar.addAction(self.selected_model_label)
        menubar.addAction(self.selected_base_label)

        # Set the window properties
        self.setWindowTitle("Projekt SI 2023")
        self.resize(500, 380)
        self.setFixedSize(self.size())

        # Add label for status bar
        self.label = QLabel(self)
        self.label.setText("Gotowy")

        # Create a status bar
        self.status = self.statusBar()
        self.status.addWidget(self.label)

        # Fit button
        self.button_trenuj = QPushButton('Trenuj', self)
        self.button_trenuj.move(100, 330)
        self.button_trenuj.clicked.connect(self.trenuj_model)

        # Predict button
        self.button_predict = QPushButton('Klasyfikuj', self)
        self.button_predict.move(200, 330)
        self.button_predict.clicked.connect(self.klasyfikuj)

        # Clear button
        self.button_clear = QPushButton('Wyczyść', self)
        self.button_clear.move(300, 330)
        self.button_clear.clicked.connect(self.clear)

        # Add text field for predicted value
        self.predicted_value = QLabel(self)
        self.predicted_value.setText("Predicted value: ")
        self.predicted_value.move(325, 25)
        self.predicted_value.resize(170, 300)
        self.predicted_value.setStyleSheet("border: 1px solid black;"
                                           "background-color: white;"
                                           "font-size: 15px;")
        self.predicted_value.setWordWrap(True)

        # Add canvas for drawing
        self.canvas = Canvas(self, width=300, height=300)
        self.canvas.move(5, 25)

    def komunikat(self, text, color="black"):
        self.label.setText(text)
        self.label.setStyleSheet(f"color: {color};")

    def nowy_model(self):
        self.komunikat("Wybrano opcję Nowy")

        if self.selected_base is None:
            self.komunikat("Nie wybrano bazy", color="red")
            return

        # Combobox with models
        model_type, ok_pressed = QInputDialog.getItem(self, "Wybór modelu", "Wybierz model:",
                                                      ("Model_1", "Model_2", "Model_3"), 0, False)

        if ok_pressed:

            if model_type == "Model_1":
                self.model = None
            elif model_type == "Model_2":
                self.model = None
            elif model_type == "Model_3":
                self.model = None

            if self.model is not None:
                self.selected_model = model_type
                self.selected_model_label.setText(f"Wybrany model: {self.selected_model}")
                self.selected_model_label.setEnabled(True)
                self.komunikat(f"Wybrano model {self.selected_model}", color="green")
                self.fitted = False
            else:
                self.komunikat("Model pusty", color="red")
        else:
            self.komunikat("Nie wybrano modelu", color="red")

    def zapisz_model(self):
        self.komunikat("Wybrano opcję Zapisz")

        if self.selected_model is None:
            self.komunikat("Nie wybrano modelu", color="red")
        elif self.model is None:
            self.komunikat("Model pusty", color="red")
        if self.fitted is False:
            self.komunikat("Model nie jest wytrenowany", color="red")
        else:
            pickle.dump(self.model, open(f"{self.selected_model}.pkl", "wb"))
            self.komunikat("Zapisano model", color="green")

    def wczytaj_model(self):
        self.komunikat("Wybrano opcję Wczytaj")

        file_name, ok = QFileDialog.getOpenFileName(self, "Wczytaj model", "", "Plik modelu (*.pkl)")
        if ok:
            self.model = pickle.load(open(file_name, "rb"))
            self.selected_model = file_name.split("/")[-1].split(".")[0]
            self.selected_model_label.setText(f"Wybrany model: {self.selected_model}")
            self.selected_model_label.setEnabled(True)
            self.canvas.clear()
            self.komunikat(f"Wczytano model {self.selected_model}", color="green")
        else:
            self.komunikat("Nie wybrano modelu", color="red")

    def trenuj_model(self):
        self.komunikat("Wybrano opcję Trenuj")

        if self.selected_model is None:
            self.komunikat("Nie wybrano modelu", color="red")
        elif self.selected_base is None:
            self.komunikat("Nie wybrano bazy", color="red")
        else:
            self.komunikat("Trenowanie modelu...", color="green")
            self.fitted = True

            self.model.fit(self.X_train, self.y_train)

            try:
                score = self.model.score(self.X_test, self.y_test)
            except:
                score = self.model.evaluate(self.X_test, self.y_test)[1]

            self.komunikat(f"Model wyćwiczony, wynik: {score}", color="green")

            self.canvas.clear()

    def klasyfikuj(self):
        self.komunikat("Wybrano opcję Klasyfikuj")
        if self.fitted is False:
            self.komunikat("Model niewyćwiczony", color="red")
        else:
            self.komunikat("Klasyfikowanie...", color="green")

            predicted = self.model.predict(self.canvas.getConvertedImage())[0]

            print(f"Predicted: {predicted}")

            try:
                text = "<html><body>"
                value = np.argmax(predicted)

                for i in range(len(predicted)):
                    if i == value:
                        text += f"<b>{i}: {predicted[i]:.5f}</b>\n"
                    else:
                        text += f"{i}: {predicted[i]:.5f}\n"

                text += "</body></html>"
                self.predicted_value.setText(text)
            except:
                self.predicted_value.setText(f"Predicted value: {predicted}")
                value = predicted

            self.canvas.showResult(value)
            self.komunikat(f"Klasyfikacja zakończona, wynik: {value}", color="green")
            self.canvas.clear()

    def pobierz_baze(self):
        self.komunikat("Wybrano opcję Pobierz")

        self.selected_base, ok = QInputDialog.getText(self, "Pobieranie bazy", "Podaj nazwę bazy:")

        if ok:
            self.komunikat(f"Pobieranie bazy {self.selected_base}...")
            downloadBase(self.selected_base)
            self.wczytaj_baze()
        else:
            self.komunikat("Nie podano nazwy bazy", color="red")

    def wczytaj_baze(self):
        self.komunikat("Wybrano opcję Wczytaj Baze")

        # Show file selection dialog
        file_name, ok = QFileDialog.getOpenFileName(self, "Wybierz plik", "", "Pliki joblib (*.joblib)")
        if ok:
            if os.path.exists(f"{file_name}"):
                train_size, ok = QInputDialog.getInt(self, "Wybierz",
                                                     "Podaj rozmiar treningowy (w %):",
                                                     min=1, max=99, step=1, value=80)

                if ok:
                    # From absolute path get only file name without extension
                    self.selected_base = os.path.splitext(os.path.basename(file_name))[0]
                    self.komunikat(f"Wybrano bazę {self.selected_base}", color="green")

                    train_size /= 100
                    self.mnist = joblib.load(f'{self.selected_base}.joblib')
                    self.X = self.mnist.data
                    self.y = self.mnist.target

                    self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y,
                                                                                            train_size=train_size,
                                                                                            random_state=42)
                    self.fitted = False

                    self.canvas.resolution = int(np.sqrt(self.X.shape[1]))

                    self.selected_base_label.setText(
                        f"Wybrana baza: {self.selected_base} {self.canvas.resolution}x{self.canvas.resolution}")
                    self.selected_base_label.setEnabled(True)

                    for i in range(10):
                        plt.subplot(2, 5, i + 1)
                        random = np.random.randint(0, len(self.X))
                        print(self.X[random])
                        plt.imshow(self.X[random].reshape(self.canvas.resolution, self.canvas.resolution), cmap='gray',
                                   vmin=0, vmax=255)
                        plt.axis('off')
                    plt.show()

                    print("Wczytano dane:")
                    print(f"X_train: {self.X_train.shape}")
                    print(f"X_test: {self.X_test.shape}")
                    print(f"y_train: {self.y_train.shape}")
                    print(f"y_test: {self.y_test.shape}")

                    print("X:")
                    print(self.X)
                    print("y:")
                    print(self.y)

                    self.komunikat("Wczytano dane", color="green")

                else:
                    self.komunikat("Anulowano", color="red")
            else:
                self.komunikat("Nie znaleziono pliku", color="red")
        else:
            self.komunikat("Anulowano", color="red")

    def clear(self):
        self.komunikat("Wyczyszczono", color="green")
        self.canvas.clear()

    def exit(self):
        QApplication.quit()


class Canvas(QWidget):
    def __init__(self, parent, width, height, resolution=64):
        super().__init__(parent)
        self.width = width
        self.height = height
        self.setFixedSize(self.width, self.height)
        self.resolution = resolution

        self.converted_image = None

        self.fullresImage = QImage(300, 300, QImage.Format.Format_Grayscale8)
        self.fullresImage.fill(Qt.white)
        self.image = self.fullresImage
        self.resizedImage = self.downsize(self.fullresImage, self.resolution, self.resolution)

        self.drawing = False
        self.last_point = QPoint()

    def paintEvent(self, event):
        # Rysowanie płótna
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        self.drawing = True
        self.last_point = event.pos()

        self.image = self.fullresImage

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.fullresImage)
            painter.setPen(QPen(Qt.black, self.width // self.resolution, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()

            self.update()

    def image_pixel_average(self, image: PyQt5.QtGui.QImage, posX, posY, width, height):
        pixel_sum = 0
        pixels_in_area = 0
        for x in range(posX - width // 4, posX + width // 4):
            if x < 0 or x >= image.width():
                continue
            for y in range(posY - width // 4, posY + height // 4):
                if y < 0 or y >= image.height():
                    continue
                pixel_sum += image.pixel(x, y)
                pixels_in_area += 1
        return int(pixel_sum / pixels_in_area)

    def downsize(self, image: PyQt5.QtGui.QImage, new_width, new_height):
        new_pixel_size = (int(image.width() / new_width), int(image.height() / new_height))
        new_image = QImage(new_width, new_height, QImage.Format_Grayscale8)
        for x in range(new_width):
            for y in range(new_height):
                v = self.image_pixel_average(image, x * new_pixel_size[0], y * new_pixel_size[1], new_pixel_size[0],
                                             new_pixel_size[1])
                new_image.setPixel(x, y, v)

        return new_image

    def mouseReleaseEvent(self, event):
        if self.drawing:
            self.drawing = False
            # Konwersja obrazka na czarno-biały z antyaliasingiem
            self.resizedImage = self.downsize(self.fullresImage, self.resolution, self.resolution)

            width = self.resizedImage.width()
            height = self.resizedImage.height()

            # Wyciągnięcie danych z pikseli i zamiana na macierz numpy
            data = self.resizedImage.bits().asstring(width * height)
            arr = np.frombuffer(data, dtype=np.uint8).reshape((height, width))

            self.image = self.resizedImage
            self.update()
            arr = arr.reshape(1, -1).astype(np.float32)
            self.converted_image = arr

    def clear(self):
        self.fullresImage.fill(Qt.white)
        self.resizedImage.fill(Qt.white)
        self.converted_image = None
        self.update()

    def getConvertedImage(self):
        if self.converted_image is None:
            self.converted_image = np.zeros((1, self.resolution * self.resolution), dtype=np.float32) + 255
        return self.converted_image

    def showResult(self, result):
        try:
            plt.imshow(self.converted_image.reshape(self.resolution, self.resolution), cmap='gray', vmin=0, vmax=255)
            plt.title(f"Rozpoznano: {result}")
            plt.show()
        except:
            print("Nie można wyświetlić obrazka")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
