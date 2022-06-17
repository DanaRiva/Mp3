from luma.core.interface.serial import i2c, spi, pcf8574
from luma.core.interface.parallel import bitbang_6800
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106, ws0010
from PyQt5 import QtCore, QtGui, QtWidgets
import time, serial
import sys, pygame
from random import randint
from pygame.constants import *
from pygame import mixer
import multitasking
import signal

class Ui_MainWindow(object):

    def __init__(self):
        self.playlist=[["Mon Amour(Remix)", "zzoilo, Aitana", "000.wav","000.png"],
        ["Aleman", "Bizarrap, Aleman", "001.wav","001.png"],
        ["Mi Tio Snoop", "Aleman", "002.wav","002.png"],
        ["Anuel", "Bizarrap, Anuel", "003.wav","003.png"],
        ["¿Que nos paso?", "Anuel AA", "004.wav","004.png"],
        ["Despues de la Playa", "Bad Bunny", "005.wav","005.png"],
        ["Titi me pregunto", "Bad Bunny", "006.wav","006.png"],
        ["DAKITI", "Bad Bunny", "007.wav","007.png"],
        ["Yonaguni", "Bad Bunny", "008.wav","008.png"],
        ["Voodoo", "Badshash,J Balvin, Tainy", "009.wav","009.png"],
        ["Bailando(Turreo Edit)", "DJ Mutha", "010.wav","010.png"],
        ["boy x", "Tate McRae", "011.wav","011.png"],
        ["NO MIENTEN (Tiësto Remix)", "Becky G, Tiësto", "012.wav","012.png"],
        ["PUFF", "Bhavi, Bizarrap", "013.wav","013.png"],
        ["BLESSED X RYAN CASTRO", "BLESSED HECHO EN MEDELLIN", "014.wav","014.png"],
        ["Hecha Pa' Mi", "Boza", "015.wav","015.png"],
        ["One Kiss", "Calvin Harris, Dua Lipa", "016.wav","016.png"],
        ["Bam Bam", "Camilla Cabello", "017.wav","017.png"],
        ["Cayo la noche", "LaPanteraBby", "018.wav","018.png"],
        ["La Llevo Al Cielo", "Chris Jedi, Anuel AA, Chencho Corleone, Ñengo Flow", "019.wav","019.png"],
        ["love nwantiti", "CKay", "020.wav","020.png"],
        ["Una noche en Medellin", "Cris Mj", "021.wav","021.png"],
        ["Demasiadas mujeres", "C. Tangana", "022.wav","022.png"],
        ["METELE AL PERREO", "Daddy Yankee", "023.wav","023.png"],
        ["PROBLEMA (Lunytunes Version)", "Daddy Yankee", "024.wav","024.png"],
        ["BOMBON", "Daddy Yankee, El Alfa, Lil Jon", "025.wav","025.png"],
        ["DANI", "Bizarrap, DANI", "026.wav","026.png"],
        ["Fuera del mercado", "Danny Ocean", "027.wav","027.png"],
        ["Se Le Ve", "Dimelo Flow, Sech, Dalex", "028.wav","028.png"],
        ["SG", "DJ Snake, Ozuna, Megan Thee Stalion, LISA", "029.wav","029.png"],
        ["Kiss Me More", "Doja Cat, SZA", "030.wav","030.png"],
        ["Efecto", "Bad Bunny, Benito Antonio Martinez Ocasio", "031.wav","031.png"],
        ["Eladio", "Bizarrap, Eladio Carrion", "032.wav","032.png"],
        ["Gogo Dance", "El Alfa", "033.wav","033.png"],
        ["Tamo Chelo (Remix)", "EL NOBA, Callejero Fino, Juanka", "034.wav","034.png"],
        ["Pepas", "Farruko", "035.wav","035.png"],
        ["El Incomprendido", "Farruko, Victor Cardenas, Dj Adoni", "036.wav","036.png"],
        ["FRIKI", "Feid, KAROL G", "037.wav","037.png"],
        ["Peru", "Fireboy DML, Ed Sheeran", "038.wav","038.png"],
        ["Una Vaina Loca", "Fuego, Manuel Turizo, Duki", "039.wav","039.png"],
        ["Paris", "Ingratax", "040.wav","040.png"],
        ["Poblado(Remix)", "J Balvin, KAROL G, Nicky Jam", "041.wav","041.png"],
        ["In Da Getto", "J Balvin, Skrillex", "042.wav","042.png"],
        ["Cambia el Paso", "Jennifer Lopez, Rauw Alejandro", "043.wav","043.png"],
        ["Ley Seca", "Jhay Cortez, Anuel AA", "044.wav","044.png"],
        ["Sensual Bebe", "Jhay Cortez", "045.wav","045.png"],
        ["Cochinae", "Juliano Sosa", "046.wav","046.png"],
        ["Loco", "Justin Quiles, Chimbala, Zion & Lennox", "047.wav","047.png"],
        ["BICHOTA", "KAROL G", "048.wav","048.png"],
        ["PROVENZA", "KAROL G", "049.wav","049.png"],
        ["SEJODIOTO", "KAROL G", "050.wav","050.png"],
        ["L-Gante", "Bizarrap, L-Gante", "051.wav","051.png"],
        ["Industry Baby", "Lil Nas X, Jack Harlow", "052.wav","052.png"],
        ["MONTERO", "Lil Nas X", "053.wav","053.png"],
        ["ESTILAZO", "Marshmello, Tokischa", "054.wav","054.png"],
        ["Sigo Esperando Que Vuelvas", "MC Davo, Santa Fe Klan, Eirian Music", "055.wav","055.png"],
        ["Sweetest Pie", "Megan Thee Stalion, Dua Lipa", "056.wav","056.png"],
        ["Morad", "Bizarrap, Morad", "057.wav","057.png"],
        ["Paris", "Morat, Duki", "058.wav","058.png"],
        ["Experimento", "Myke Towers", "059.wav","059.png"],
        ["Brillo", "Natanael Cano", "060.wav","060.png"],
        ["Nataaoki", "Natanel Cano, Steve Aoki", "061.wav","061.png"],
        ["Nathy Peluso", "Bizarrap, Nathy Peluso", "062.wav","062.png"],
        ["Wow BB", "Natti Natasha, El Alfa, Chimbala", "063.wav","063.png"],
        ["Nicki Nicole", "Nicki Nicole, Bizarrap", "064.wav","064.png"],
        ["Nicky Jam", "Bizarrap, Nicky Jam", "065.wav","065.png"],
        ["AM Remix", "Nio Garcia, J Balvin, Bad Bunny", "066.wav","066.png"],
        ["Ojitos Lindos", "Bad Bunny", "067.wav","067.png"],
        ["good 4 you", "Olivia Rodrigo", "068.wav","068.png"],
        ["Perdóname", "La Factoria", "069.wav","069.png"],
        ["Deprimida", "Ozuna", "070.wav","070.png"],
        ["Paulo Londra", "Bizarrap, Paulo Londra", "071.wav","071.png"],
        ["ULTRA SOLO", "Polima Westcoast, Pilita", "072.wav","072.png"],
        ["PITAZETA", "Twenty BeatZ's", "073.wav","073.png"],
        ["Cnv Sound, Vol.14", "Pure Negga", "074.wav","074.png"],
        ["Que Me Contas", "Dimelo Flow, Sech, J Balvin", "075.wav","075.png"],
        ["Desesperados", "Rauw Alejandro, Chencho Corleone", "076.wav","076.png"],
        ["Residente", "Bizarrap, Residente", "078.wav","078.png"],
        ["Sus Huellas", "Romeo Santos", "079.wav","079.png"],
        ["SAOKO", "ROSALIA", "080.wav","080.png"],
        ["Nostalgico", "Rvssian, Rauw Alejandro, Chris Brown", "081.wav","081.png"],
        ["Jordan", "Ryan Castro", "082.wav","082.png"],
        ["Tacones Rojos", "Sebastian Yatra, John Legend", "083.wav","083.png"],
        ["Sal y Perrea (Remix)", "Sech, Daddy Yankee, J Balvin", "084.wav","084.png"],
        ["Baila Conmigo", "Selena Gomez, Rauw Alejandro", "085.wav","085.png"],
        ["Te Felicito", "Shakira, Rauw Alejandro", "086.wav","086.png"],
        ["Snow Tha Product", "Bizarrap, Snow Tha Product", "087.wav","087.png"],
        ["Pegate", "Standly", "088.wav","088.png"],
        ["Save Your Tears", "The Weeknd", "089.wav","089.png"],
        ["Take My Breath (Single Version)", "The Weeknd", "090.wav","090.png"],
        ["TIAGO PZK", "Bizarrap", "091.wav","091.png"],
        ["Don't Be Shy", "Tiësto, KAROL G", "092.wav","092.png"],
        ["The Business", "Tiësto", "093.wav","093.png"],
        ["Trueno", "Bizarrap, Trueno", "094.wav","094.png"],
        ["DANCE CRIP", "Trueno", "095.wav","095.png"],
        ["Villano Antillano", "Bizarrap, Villano Antillano", "096.wav","096.png"],
        ["Fiel", "Los Legendarios, Wisin, Jhay Cortez", "097.wav","097.png"],
        ["Emojis de Corazones", "Wisin, Jhay Cortez, Ozuna", "098.wav","098.png"],
        ["Mi Niña(Remix)", "Wisin, Myke Towers, Maluma", "099.wav","099.png"],
        ["YSY A", "Bizarrap, YSY A", "100.wav","100.png"]]
        signal.signal(signal.SIGINT, multitasking.killall)
        self.ser=serial.Serial(port='/dev/ttyACM0', baudrate=19200, timeout=1)
        self.oled = i2c(port=1, address=0x3C)
        mixer.init()
        self.timerSong = QtCore.QTimer()
        self.timerSong.setInterval(1000)
        self.timerSong.timeout.connect(self.taskTime)
        self.barValue = 0
        self.num = 0
        mixer.music.load(self.playlist[self.num][2])
        mixer.music.play()
        mixer.music.pause()
        self.taskTime()

    def window(self, MainWindow):
        MainWindow.resize(800, 600)
        widgets = QtWidgets.QWidget(MainWindow)

        box = QtWidgets.QTextBrowser(widgets)
        box.setGeometry(QtCore.QRect(10, 10, 385, 580))
        data = []
        for row in self.playlist:
            data.append(' '.join(row))
        box.setText('\n'.join(data))

        fondo = QtWidgets.QLabel(widgets)
        fondo.setGeometry(QtCore.QRect(527, 10, 241, 241))
        fondo.setPixmap(QtGui.QPixmap("../botones/abrir.png"))
 
        nextSongBtn = QtWidgets.QPushButton(widgets)
        nextSongBtn.setGeometry(QtCore.QRect(405, 330, 120, 125))
        nextSongBtn.setStyleSheet("image: url(../botones/anterior.png)")
        nextSongBtn.clicked.connect(self.nextSong)
        
        prevSongBtn = QtWidgets.QPushButton(widgets)
        prevSongBtn.setGeometry(QtCore.QRect(670, 330, 120, 125))
        prevSongBtn.setStyleSheet("image: url(../botones/siguiente.png)")
        prevSongBtn.clicked.connect(self.prevSong)
        
        randomBtn = QtWidgets.QPushButton(widgets)
        randomBtn.setGeometry(QtCore.QRect(535, 330, 125, 125))
        randomBtn.setStyleSheet("image: url(../botones/aleatorio.png)")
        randomBtn.clicked.connect(self.random)
        
        playBtn = QtWidgets.QPushButton(widgets)
        playBtn.setGeometry(QtCore.QRect(450, 465, 125, 125))
        playBtn.setStyleSheet("image: url(../botones/play.png)")
        playBtn.clicked.connect(self.play)

        pauseBtn = QtWidgets.QPushButton(widgets)
        pauseBtn.setGeometry(QtCore.QRect(620, 465, 125, 125))
        pauseBtn.setStyleSheet("image: url(../botones/pausa.png)")
        pauseBtn.clicked.connect(self.pause)

        self.progressBar = QtWidgets.QSlider(widgets)
        self.progressBar.setGeometry(QtCore.QRect(405, 280, 385, 40))
        self.progressBar.setOrientation(1)
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(120)

        MainWindow.setCentralWidget(widgets)

    def stepTime(self):
        self.progressBar.setValue(mixer.music.get_pos()//1000)

    def pause(self):
        mixer.music.pause()

    def play(self):
        mixer.music.unpause()

    def random(self):
        self.num = randint(0,99)
        mixer.music.load(self.playlist[self.num][2])
        mixer.music.play()
        device = ssd1306(self.oled)
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "\n".join([self.playlist[self.num][0], self.playlist[self.num][1]]), fill="white")

    def nextSong(self):
        self.num = (self.num+1)%100
        mixer.music.load(self.playlist[self.num][2])
        mixer.music.play()
        device = ssd1306(self.oled)
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "\n".join([self.playlist[self.num][0], self.playlist[self.num][1]]), fill="white")

    def prevSong(self):
        self.num = (self.num or 100) -1
        mixer.music.load(self.playlist[self.num][2])
        mixer.music.play()
        device = ssd1306(self.oled)
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 10), "\n".join([self.playlist[self.num][0], self.playlist[self.num][1]]), fill="white")

    @multitasking.task
    def taskTime(self):
        while True:
            data = self.ser.readline()
            self.stepTime()
            if data == b'' or data == b'\n':
                pass
            elif (data==b'A\n'):
                self.pause()
            elif (data==b'B\n'):
                self.play()
            elif (data==b'C\n'):
                self.nextSong()
            elif (data==b'D\n'):
                self.prevSong()
            elif (data==b'#\n'):
                self.random()
            elif (data==b'*\n'):
                exit()
            else:
                self.num = int(data.decode('utf-8')[:-1])
                mixer.music.load(self.playlist[self.num][2])
                mixer.music.play()
                device = ssd1306(self.oled)
                with canvas(device) as draw:
                    draw.rectangle(device.bounding_box, outline="white", fill="black")
                    draw.text((10, 10), "\n".join([self.playlist[self.num][0], self.playlist[self.num][1]]), fill="white")

#Marien <3
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.window(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    exit()
