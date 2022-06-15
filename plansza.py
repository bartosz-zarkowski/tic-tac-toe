import numpy as np


#Klasa generująca z pomocą numpy tablicę wypełnioną zerami. W konstruktorze funkcji grę zaczyna domyślnie krzyżyk. Zmienna wynik (domyślnie zero) przechowuje wynik rozgrywki.
class game:                
    #Konstruktor klasy przechowujący tablicę numpy, aktualną turę oraz końcowy wynik
    def __init__(self):
        self.board = np.zeros(9, dtype=int)
        self.tura = 1
        self.__wynik = 0

    #funkcja sprawdzająca wynik (wszystkie 9 kombinacji)
    def check_win(self, player):
        #Sprawdzenie poszczególnych wierszy.
        for i in range(0,9,3):
            if self.board[i] == player and self.board[i+1] == player and self.board[i+2] == player:
                return player
        #Sprawdzenie poszczególnych kolumn.
        for i in range(0,3,1):
            if self.board[i] == player and self.board[i+3] == player and self.board[i+6] == player:
               return player
        #Sprawdzenie przekątnych.
        for i in range(0,3,2):
            if self.board[i] == player and self.board[4] == player and self.board[8-i] == player:
               return player

        #Sprawdzenie warunku remisu
        remis = 0
        for i in range(0,9):
            if self.board[i] != 0:
                remis += 1
        if remis == 9:
            return 0


    def print_board(self):
        print(self.board)

    def move(self, player, x):
        self.board[x] = player

    def get_board(self):
        return self.board

    def set_wynik(self, result):
        self.__wynik = result 

    def get_wynik(self):
        return self.__wynik
