from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, QMessageBox, QDialog, QVBoxLayout, QLineEdit, QLabel)
import sys
from plansza import game

#Klasa odpowiedzialna za logikę gry oraz GUI.
class MainWindow(QWidget):
    #Konstruktor, w którym domyślnym graczem jest krzyżyk.
    def __init__(self):
        super().__init__()
        self.gra = game()
        self.player_now = 1
        self.main()

    #Definicja głównego okna oraz przycisków, a także przypisanie im funkcji.
    def main(self):
        #Definicja głównego okna
        self.setFixedSize(300, 300)
        self.setWindowTitle("Tic-Tac-Toe") 
        QWidget.setStyleSheet(self, 'background-color: black')

        #definicja przycisków.
        grid = QGridLayout()
        self.setLayout(grid)
        self.buttons = {}
        cord = []
        temp = {}
        for i in range(9):
            cord.append(i)

        licz = 0
        for i in range(3):
            temp = 0
            for j in range(3):
                self.buttons[(licz+j)] = QPushButton()
                grid.addWidget(self.buttons[(licz+j)],i,j)
                temp = j
            licz += temp +1

        #Ustawienie domyślnych przycisków (białych)
        for i in range(9):
            self.buttons[(i)].setFixedSize(80,80)
            self.buttons[(i)].setStyleSheet('border-radius:80px; background-image: url(default.jpg)')
            self.buttons[(i)].clicked.connect(lambda state, con=cord[i]: self.button_move(con))

        self.show()

    #Funkcja zamykająca okno gry.
    def close_window(self):
        self.close()

    #Funkcja zapisująca statystyki gry.
    def save_stats(self):
        self.file = open('stats.txt', 'r+')
        self.stats = self.file.read()
        characters = 0
        for i in self.stats:
            characters += 1
        if characters >= 10:
            self.file.truncate(0)
        self.file.close()

        self.file = open('stats.txt', 'a')
        self.file.write(str(self.gra.get_wynik()))
        self.file.close()


    #Funkcja wypiująca statystyki gry.
    def print_stats(self):        
        self.file = open('stats.txt', 'r')
        pstats = QDialog()
        pstats.setWindowTitle('Statystyki gier')
        pstats.setFixedSize(150, 400)
        pstats.setStyleSheet('background-color: black; color: white; line-height: 3.6')
        pstats.layout = QVBoxLayout()
        self.stats = self.file.read()

        j = 0
        for i in reversed(self.stats):
            if (i == '0'): 
                #print(j+1, '. Remis')
                self.stats_j = i
                pstats.label_j = QLabel('Remis')
                pstats.layout.addWidget(pstats.label_j)
                j+=1
            elif (i == '1'): 
                #print(j+1, '. Wygrał krzyżyk')
                self.stats_j = i
                pstats.label_j = QLabel('Wygrał krzyżyk')
                pstats.layout.addWidget(pstats.label_j)
                j+=1
            elif (i == '2'): 
                #print(j+1, '. Wygrało kółko')
                self.stats_j = i
                pstats.label_j = QLabel('Wygrało kółko')
                pstats.layout.addWidget(pstats.label_j)
                j+=1

        self.file.close()
        pstats.setLayout(pstats.layout)
        pstats.exec()


    #Definicja działania przycisków oraz sprawdzenie tury. 
    def button_move(self,tup_cord):
        stan = self.gra.get_board()[tup_cord]
        #Wywołanie funkcji dla krzyżyka oraz sprawdzenie wyniku po ruchu.
        if self.player_now == 1:
            if self.gra.get_board()[tup_cord] == 0:
                self.gra.get_board()[tup_cord] = 1
                self.buttons[tup_cord].setStyleSheet('border-radius:80px; background-image: url(x.jpg)')
                result = self.gra.check_win(self.player_now)
                if (result == 1):
                    self.gra.set_wynik(result)
                    self.save_stats()
                    self.dialog()
                    return
                elif (result == 0):
                    self.gra.set_wynik(0)
                    self.save_stats()
                    self.dialog()
                    return
                if self.gra.get_board()[tup_cord] != stan:
                    self.player_now = 2
        #Wywołanie funkcji dla kółka oraz sprawdzenie wyniku po ruchu.
        else:
            if self.gra.get_board()[tup_cord] == 0:
                self.gra.get_board()[tup_cord] = 2
                self.buttons[tup_cord].setStyleSheet('border-radius:80px; background-image: url(o.jpg)')
                result = self.gra.check_win(self.player_now)
                if (result == 2):
                    self.gra.set_wynik(2)
                    self.save_stats()
                    self.dialog()
                    return
                elif (result == 0):
                    self.gra.set_wynik(0)
                    self.save_stats()
                    self.dialog()
                    return
                if self.gra.get_board()[tup_cord] != stan:
                    self.player_now = 1


    #Definicja okna dialogowego oraz działania poszczególnych przycisków.
    def dialog(self):
        dial = QDialog()
        dial.setWindowTitle("Wynik") 
        dial.setFixedSize(250, 150)
        dial.layout = QVBoxLayout()

        if (self.gra.get_wynik() == 1):
            dial.label = QLabel("Wygrał krzyżyk!")
        elif (self.gra.get_wynik() == 2):
            dial.label = QLabel("Wygrało kółko!")
        elif (self.gra.get_wynik() == 0):
            dial.label = QLabel("Remis!")

        dial.zagraj = QPushButton("Zagraj ponownie")
        dial.zagraj.clicked.connect(MainWindow)
        dial.zagraj.clicked.connect(self.close_window)
        dial.zagraj.clicked.connect(dial.close)

        dial.wyniki = QPushButton("Statystyki")
        dial.wyniki.clicked.connect(self.print_stats)

        dial.wyjdz = QPushButton("Wyjdź z gry")
        dial.wyjdz.clicked.connect(self.close_window)
        dial.wyjdz.clicked.connect(dial.close)

        dial.layout.addWidget(dial.label)
        dial.layout.addWidget(dial.zagraj)
        dial.layout.addWidget(dial.wyniki)
        dial.layout.addWidget(dial.wyjdz)

        dial.setLayout(dial.layout)

        dial.exec()

#Definicja oraz wywołanie gry.
app = QApplication(sys.argv)
wind = MainWindow()
sys.exit(app.exec_())