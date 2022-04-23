from tkinter import *
from random import shuffle
from threading import Thread
from time import sleep


class Player:

    def __init__(self, window, number, default_stack, x, y, bet_x, bet_y):

        """НАСТРОЙКА СВОЙСТВ КЛАССА"""
        self.window = window
        self.number = number
        self.defaultStack = default_stack
        self.x = x
        self.y = y
        self.betX = bet_x
        self.betY = bet_y
        self.gainX = 600
        self.gainY = 100 + ((self.number - 1) * 20)

        self.inGame = True
        self.gotStatus = False
        self.pocket = []

        """ВИДЖЕТЫ"""
        self.seat = BooleanVar(value=True)  # Флаг наличия игрока за столом. По умолчанию True.
        self.showSeat = Checkbutton(self.window,
                                    relief='solid',
                                    bd=1,
                                    text=f'Player {self.number}',
                                    font=('', '9', 'bold'),
                                    variable=self.seat,
                                    onvalue=True,
                                    offvalue=False,
                                    command=self.seat_highlighter)
        self.showSeat.place(x=self.x, y=self.y, anchor=CENTER)

        self.icon = PhotoImage(file=r'images\player.png')
        self.showIcon = Label(self.window,
                              bg='LimeGreen',
                              height=63,
                              image=self.icon)
        self.showIcon.place(x=self.x, y=self.y - 45, anchor=CENTER)

        self.range = IntVar(value=0)
        self.showRange = Label(self.window,
                               relief='solid',
                               bd=1,
                               anchor=CENTER,
                               textvariable=self.range,
                               font=('', '9', 'bold'))
        self.showRange.place(x=self.x - 35, y=self.y - 11, width=23, height=23, anchor=NE)

        self.stackLegend = Label(self.window,
                                 relief='solid',
                                 bd=1,
                                 anchor=W,
                                 text=' $',
                                 font=('', '9', 'bold'))
        self.stackLegend.place(x=self.x, y=self.y + 20, width=72, anchor=CENTER)

        self.stack = DoubleVar(value=self.defaultStack)
        self.showStack = Label(self.window,
                               bd=0,
                               textvariable=self.stack,
                               font=('', '9', 'bold'))
        self.showStack.place(x=self.x - 22, y=self.y + 20, width=57, anchor=W)

        self.pocketValue = StringVar(value=self.pocket)  # Список карт в колоде.
        self.showPocket = Label(self.window,
                                bd=0,
                                bg='LimeGreen',
                                textvariable=self.pocketValue,
                                font=('', '10', 'bold'))
        self.showPocket.place(x=self.x, y=self.y - 18, height=11, anchor=CENTER)

        self.betValue = DoubleVar(value=100.01)
        self.showBet = Label(self.window,
                             bd=0,
                             textvariable=self.betValue,
                             font=('', '9', 'bold'))
        self.showBet.place(x=self.x+self.betX, y=self.y+self.betY, anchor=CENTER)

        self.dealerIcon = PhotoImage(file=r'images\dealer.png')
        self.showDealerIcon = Label(self.window,
                                    bg='LimeGreen',
                                    image=self.dealerIcon)

        self.gainLegend = Label(self.window,
                                bg='LimeGreen',
                                text=f'PLAYER {self.number} - ',
                                font=('', '9', 'bold'))
        self.gainLegend.place(x=self.gainX, y=self.gainY, anchor=NE)

        self.gain = DoubleVar(value=0)
        self.showGain = Label(self.window,
                              bg='LimeGreen',
                              textvariable=self.gain,
                              font=('', '9', 'bold'))
        self.showGain.place(x=self.gainX + 5, y=self.gainY, anchor=NW)

        self.currencyLegend = Label(self.window,
                                    bg='LimeGreen',
                                    text='$',
                                    font=('', '9', 'bold'))
        self.currencyLegend.place(x=self.gainX - 6, y=self.gainY, anchor=NW)

    def dealer_highlighter(self):
        self.showDealerIcon.place(x=self.x + 36, y=self.y + 10)

    def seat_highlighter(self):
        if self.seat.get():
            self.currencyLegend['text'] = '$'
            self.gain.set(0)
            self.showGain.place(x=self.gainX + 5, y=self.gainY, anchor=NW)
            self.showRange.place(x=self.x - 35, y=self.y - 11, width=23, height=23, anchor=NE)
            self.showIcon.place(x=self.x, y=self.y - 45, anchor=CENTER)
            self.stackLegend.place(x=self.x, y=self.y + 20, width=72, anchor=CENTER)
            self.showStack.place(x=self.x - 22, y=self.y + 20, width=57, anchor=W)
            self.stack.set(self.defaultStack)
            self.showPocket.place(x=self.x, y=self.y - 18, height=11, anchor=CENTER)
            self.pocketValue.set(self.pocket)
        else:
            self.showGain.place_forget()
            self.currencyLegend['text'] = 'SITTING OUT'
            self.showRange.place_forget()
            self.showIcon.place_forget()
            self.stackLegend.place_forget()
            self.showStack.place_forget()
            self.showPocket.place_forget()


class App:
    """Класс Графического интерфейса, который задаёт логику взаимодействия визуальных элементов приложения."""

    def __init__(self):
        """Конструктор класса Графического приложения.

        НАСТРОЙКА ГЛАВНОГО ОКНА"""
        self.window = Tk()  # Создание экземпляра класса Tk для отображения Окна Интерфейса.
        self.window.wm_attributes('-topmost', 1)  # Поверх всех окон.
        self.window.geometry('700x500+620+80')  # Геометрия и размещение на экране.
        self.window.resizable(False, False)  # Запрет на изменение размера.
        self.window.configure(bg='LimeGreen', highlightthickness=1, highlightcolor='white')
        self.window.iconbitmap(r'images\icon.ico')  # Иконка Приложения.
        self.window.title('Hermes')  # Титульная надпись.
        self.window.protocol('WM_DELETE_WINDOW', self.closer)

        """ВИДЖЕТЫ"""
        self.deckLegend = Label(self.window,
                                bg='LimeGreen',
                                text='--- Deck ---',
                                font=('', '13', 'bold'))
        self.deckLegend.pack()

        self.deckDict = {'A\u2666': 14, 'A\u2665': 14, 'A\u2660': 14, 'A\u2663': 14,
                         'K\u2666': 13, 'K\u2665': 13, 'K\u2660': 13, 'K\u2663': 13,
                         'Q\u2666': 12, 'Q\u2665': 12, 'Q\u2660': 12, 'Q\u2663': 12,
                         'J\u2666': 11, 'J\u2665': 11, 'J\u2660': 11, 'J\u2663': 11,
                         'T\u2666': 10, 'T\u2665': 10, 'T\u2660': 10, 'T\u2663': 10,
                         '9\u2666': 9, '9\u2665': 9, '9\u2660': 9, '9\u2663': 9,
                         '8\u2666': 8, '8\u2665': 8, '8\u2660': 8, '8\u2663': 8,
                         '7\u2666': 7, '7\u2665': 7, '7\u2660': 7, '7\u2663': 7,
                         '6\u2666': 6, '6\u2665': 6, '6\u2660': 6, '6\u2663': 6,
                         '5\u2666': 5, '5\u2665': 5, '5\u2660': 5, '5\u2663': 5,
                         '4\u2666': 4, '4\u2665': 4, '4\u2660': 4, '4\u2663': 4,
                         '3\u2666': 3, '3\u2665': 3, '3\u2660': 3, '3\u2663': 3,
                         '2\u2666': 2, '2\u2665': 2, '2\u2660': 2, '2\u2663': 2}

        self.deck = list(self.deckDict.keys())

        self.deckValue = StringVar(value=self.deck)  # Список карт в колоде.
        self.showDeck = Label(self.window,
                              bg='LimeGreen',
                              textvariable=self.deckValue,
                              font=('', '12', 'bold'),
                              wraplength=630)
        self.showDeck.pack()

        self.gameModeLegend = Label(self.window,
                                    bg='LimeGreen',
                                    text='GAME MODE :',
                                    font=('', '9', 'bold'))
        self.gameModeLegend.place(x=10, y=80, anchor=NW)

        self.gameModeValue = StringVar(value='A')
        self.gameModeValues = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')
        self.showGameMode = Spinbox(self.window,
                                    relief='solid',
                                    # must be flat, groove, raised, ridge, solid, or sunken
                                    width=2,
                                    justify=CENTER,
                                    font=('', '9', 'bold'),
                                    state='readonly',
                                    value=self.gameModeValues,
                                    textvariable=self.gameModeValue,
                                    wrap=True,
                                    command=self.mode_tuner)
        self.showGameMode.place(x=91, y=83, height=16, anchor=NW)

        self.rakeLegend = Label(self.window,
                                bg='LimeGreen',
                                text='RAKE    $',
                                font=('', '9', 'bold'))
        self.rakeLegend.place(x=10, y=100, anchor=NW)

        self.rakeValue = DoubleVar(value=0.02)
        self.rakeValues = (0.02, 0.03, 0.07, 0.15, 0.3, 0.6, 1.5, 3, 10)
        self.showRake = Label(self.window,
                              bg='LimeGreen',
                              font=('', '9', 'bold'),
                              textvariable=self.rakeValue)
        self.showRake.place(x=62, y=100, anchor=NW)

        self.sbLegend = Label(self.window,
                              bg='LimeGreen',
                              text='SB         $',
                              font=('', '9', 'bold'))
        self.sbLegend.place(x=10, y=120, anchor=NW)

        self.sbValue = DoubleVar(value=0.05)
        self.sbValues = (0.05, 0.1, 0.25, 0.5, 1, 2, 5, 10, 50)
        self.showSb = Label(self.window,
                            bg='LimeGreen',
                            font=('', '9', 'bold'),
                            textvariable=self.sbValue)
        self.showSb.place(x=62, y=120, anchor=NW)

        self.bbLegend = Label(self.window,
                              bg='LimeGreen',
                              text='BB         $',
                              font=('', '9', 'bold'))
        self.bbLegend.place(x=10, y=140, anchor=NW)

        self.bbValue = DoubleVar(value=0.1)
        self.bbValues = (0.1, 0.25, 0.5, 1, 2, 4, 10, 20, 100)
        self.showBb = Label(self.window,
                            bg='LimeGreen',
                            font=('', '9', 'bold'),
                            textvariable=self.bbValue)
        self.showBb.place(x=62, y=140, anchor=NW)

        self.stackLegend = Label(self.window,
                                 bg='LimeGreen',
                                 text='STACK $',
                                 font=('', '9', 'bold'))
        self.stackLegend.place(x=10, y=160, anchor=NW)

        self.stackValue = IntVar(value=1)
        self.stackValues = (1, 2, 4, 8, 16, 32, 80, 160, 1000)
        self.showStack = Label(self.window,
                               bg='LimeGreen',
                               font=('', '9', 'bold'),
                               textvariable=self.stackValue)
        self.showStack.place(x=62, y=160, anchor=NW)

        self.speedLegend = Label(self.window,
                                 bg='LimeGreen',
                                 text='SPEED :',
                                 font=('', '9', 'bold'))
        self.speedLegend.place(x=10, y=180, anchor=NW)

        self.speedValue = IntVar(value=1)
        self.showSpeed = Spinbox(self.window,
                                 relief='solid',
                                 width=2,
                                 justify=CENTER,
                                 font=('', '9', 'bold'),
                                 state='readonly',
                                 from_=0, to_=10,
                                 textvariable=self.speedValue,
                                 wrap=True)
        self.showSpeed.place(x=60, y=183, height=16, anchor=NW)

        self.playersGainLegend = Label(self.window,
                                       bg='LimeGreen',
                                       text='PLAYERS GAIN :',
                                       font=('', '9', 'bold'))
        self.playersGainLegend.place(x=650, y=80, anchor=NE)

        self.playButtonIcon = PhotoImage(file=r'images\play.png')
        self.pauseButtonIcon = PhotoImage(file=r'images\pause.png')
        self.playButton = Button(self.window,
                                 bg='Teal',
                                 activebackground='Teal',
                                 width=30, height=30,
                                 relief='solid',  # must be flat, groove, raised, ridge, solid, or sunken
                                 image=self.playButtonIcon,
                                 command=self.game_starter)
        self.playButton.place(x=650, y=450)

        """ДИНАМИЧНЫЕ ПЕРЕМЕННЫЕ"""
        self.gameRunning = False
        self.roundRunning = True
        self.getPocket = False
        self.dealerTurn = 4
        self.turn = None

        """ЭКЗЕМПЛЯРЫ КЛАССА Player"""
        self.player1 = Player(self.window, 1, self.stackValue.get(), x=150, y=310, bet_x=90, bet_y=0)
        self.player2 = Player(self.window, 2, self.stackValue.get(), x=350, y=210, bet_x=0, bet_y=60)
        self.player3 = Player(self.window, 3, self.stackValue.get(), x=550, y=310, bet_x=-90, bet_y=0)
        self.player4 = Player(self.window, 4, self.stackValue.get(), x=350, y=450, bet_x=0, bet_y=-110)

        """БЕСКОНЕЧНЫЙ ЦИКЛ ГЛАВНОГО ОКНА"""
        self.window.mainloop()

    def mode_tuner(self):
        i = self.gameModeValues.index(self.gameModeValue.get())
        self.rakeValue.set(self.rakeValues[i])
        self.sbValue.set(self.sbValues[i])
        self.bbValue.set(self.bbValues[i])
        self.stackValue.set(self.stackValues[i])

    def time_holder(self):
        sleep(self.speedValue.get())

    def game_starter(self):
        if self.gameRunning:
            self.playButton['image'] = self.playButtonIcon
            self.gameRunning = False
        else:
            self.playButton['image'] = self.pauseButtonIcon
            self.gameRunning = True
            Thread(target=self.game_loop, daemon=True).start()

    def deck_shuffler(self):
        shuffle(self.deck)
        self.deckValue.set(self.deck)

    def dealer(self):
        return self.__dict__[f'player{self.dealerTurn}']

    def dealer_selector(self):
        self.dealerTurn += 1
        if self.dealerTurn == 5:
            self.dealerTurn = 1
        if not self.dealer().seat.get():
            self.dealer_selector()

    def game_loop(self):
        """Цикл Раунда. Каждая итерация цикла - это один раунд игры."""
        while self.gameRunning:
            self.deck_shuffler()
            self.time_holder()
            self.dealer().showDealerIcon.place_forget()
            self.dealer_selector()
            self.dealer().dealer_highlighter()
            self.time_holder()

            self.turn = self.dealerTurn
            self.round_loop()

    def player(self):
        return self.__dict__[f'player{self.turn}']

    def turn_selector(self):
        self.turn += 1
        if self.turn == 5:
            self.turn = 1
        if not self.player().inGame:
            self.turn_selector()

    def round_loop(self):
        while self.roundRunning:
            self.turn_selector()

            if not self.player().gotStatus:
                if not self.player().seat.get():
                    self.player().inGame = False
                self.player().gotStatus = True

            if not self.getPocket and self.player().inGame:
                if len(self.player().pocket) > 1:
                    self.getPocket = True
                else:
                    self.player().pocket.append(self.deck.pop(0))
                    self.deckValue.set(self.deck)
                    self.player().pocketValue.set(self.player().pocket)
                    self.time_holder()

    # Метод, который закрывает программу.
    def closer(self):
        self.gameRunning = False
        self.window.destroy()


app = App()
app.game_loop()
"""Создание экземпляра класса App - точка запуска окна графического интерфейса."""
