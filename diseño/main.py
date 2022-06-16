#librerias para las funcionaledades de diseño, y datos de las canciones
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl, QPoint
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaMetaData
#librerias de la grafica
import pyqtgraph as pg
import numpy as np

#clase principal, archivo de diseño
class ReproductorMusica(QMainWindow):
    def __init__(self):
        super(ReproductorMusica,self).__init__()
        loadUi('diseño.ui',self)
        #variables
        self.clic_posicion= QPoint()#control de la ventana
        self.estado=True#verifica y esta en play o pausa la cancion
        self.play_lista=[]#canciones importadas
        self.posicion= 0#posicion de la cancion cuando esta sonando
        self.indice= ''#fila donde estan las canciones
        self.num= 0#actualizar la grafica
        #control de botones
        self.bt_abrir.clicked.connect(self.abrir_archivo)#selecionar la carpeta
        self.bt_pausa.hide()
        self.bt_volumen_0.hide()
        self.bt_volumen_100.hide()
        self.bt_play.setEnabled(False)#false porque al inicio no hay una cancion para reproducir
        #objeto player
        self.player= QMediaPlayer()#permite controlar los botones
        self.player.setVolume(50)
        #control de los comandos
        self.slider_tiempo.sliderMoved.connect(lambda x: self.player.setPosition(x))#se coloca la posicion para que se mueva solo el slider
        self.slider_volumen.valueChanged.connect(self.variar_volumen)#nosotros movemos el slider del volumen
        self.player.positionChanged.connect(self.posicion_cancion)#identificar posicion
        self.player.durationChanged.connect(self.duracion_cancion)#identificar duracion
        self.player.stateChanged.connect(self.estado_tiempo)#en que tiempo se encuentra la cancion
        #control de la musica
        self.bt_play.clicked.connect(self.reproducir_musica)#ejecicion de metodos
        self.bt_pausa.clicked.connect(self.pausar_musica)#ejecicion de metodos
        self.bt_anterior.clicked.connect(self.retroceder_musica)#ejecicion de metodos
        self.bt_siguiente.clicked.connect(self.adelantar_musica)#ejecicion de metodos
        #configuracion de clicks para la lista
        self.lista_musica.doubleClicked.connect(self.reproducir_musica)
        self.lista_musica.clicked.connect(self.seleccion_canciones)
        #eliminar/opacidad barra de titulo
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(0.95)#cuando es 0 es transtarente
        #grafica
        self.graphWidget = pg.PlotWidget(title= 'SPECTRUM')
        self.grafica_layout.addWidget(self.graphWidget)
        self.espectrum_grafica()
        self.update_datos()#actualizar datos random
        
    #metodo abrir archivo
    def abrir_archivo(self):
        if len(self.play_lista)>0:#longitud de la lista mayor a 0
            self.play_lista.clear()
            self.lista_musica.clear()#eliminar lista para poder seleccionar otra
            self.bt_play.setEnabled(False)#desabilitar boton
            
        archivo= QFileDialog()#abrir ventana para seleccionar archivos
        archivo.setFileMode(QFileDialog.ExistingFiles)
        nombre= archivo.getOpenFileNames(self, 'Abrir archivos de audio',filter='Audio Files(*.mp3 *.ogg *.wav)')#se obtienen las canciones
        
        self.musica= nombre[0]#obtener musica
        nombres_musica= []
        #excepcion por si no hay nada en la lista
        try:
            #se elimina la direccion de la cancion y solo se deja el nombre
            for music in self.musica:
                direccion= music.split('/')
                nombre_cancion= direccion.pop()#nos retorna solo el nombre de la cancion
                nombres_musica.append(nombre_cancion)
            self.dir= ','.join(direccion).replace(',','/')
            self.lista_musica.addItems(nombres_musica)#agregamos el nombre de la cancion a la lista
        except UnboundLocalError:
            pass
    #metodo de reproduccion
    def reproducir_musica(self):
        if self.estado:
            self.estado= True#en falso se reproduce
            self.bt_play.hide()#ocultando boton play
            self.bt_pausa.show()#mostrando boton pausa
            self.indice= self.lista_musica.currentRow().__index__()#indice de lista
            path= self.lista_musica.currentItem().text()#seleccionar cancion
            
            cancion_x= f'{self.dir}/{path}'#recuperamos direccion
            
            url= QUrl.fromLocalFile(cancion_x)
            content= QMediaContent(url)#direccion
            self.player.setMedia(content)
            #self.player.setPosition(self,posicion)#optenemos posicion
            self.play_lista.append(path)#agregando nombre de las canciones a la lista
            #si la lista tiene mas de 2 canciones se la eliminando la primera cancio y la que sigue queda como posicion 0
            if len (self.play_lista)>2:
                self.play_lista.pop(0)
                if self.lista_musica.currentItem().text() != self.play_lista[0]:
                    self.pocision= 0
                    self.player.setPosition(self.posicion)
                self.player.play()
            #si no se cumple la musica se pasa
            else:
                self.pausar_musica()
                self.estado= True
                
    #metadatos de las canciones
    def metadata_cancion(self):
        if self.player.isMetaDataAvailable():#condicion si estan disponibles
            titulo= self.player.metaData(QMediaMetaData.Title)
            artista= self.player.metaData(QMediaMetaData.Artist)
            album= self.player.metaData(QMediaMetaData.Album)
            numero= str(self.player.metaData(QMediaMetaData.Num))
            #settext para ponerlo en la ventana
            self.titulo_cancion.setText(f'TITULO: {titulo}')
            self.artista_cancion.setText(f'ARTISTA: {artista}')
            self.album_cancion.setText(f'ALBUM: {album}')
            self.numero_cancion.setText(f'NUMERO: {numero}')
            
    #metodo pausa
    def pausar_musica(self):
        if self.estado:#condicion si el estado esta en falso
            self.estado= False
            self.player.pause()
            self.posicion= self.player.position()
            self.bt_play.show()#mostramos el boton play 
            self.bt_pausa.hide()#ocultamos el boton pausa
            
    #metodo seleccionar canciones
    def seleccion_canciones(self):
            self.estado= True
            self.bt_play.show()#mostramos el boton play 
            self.bt_pausa.hide()#ocultamos el boton pausa
            self.bt_play.setEnabled(True)#se activa
            
    #metodo siguiente cancion
    def adelantar_musica(self):
            self.estado= True#cuando se adelanta automaticamente se reproduce la cancion
            try:
                self.lista_musica.setCurrentRow(self.indice+1)#se aumenta la cancion
                self.play_musica()#se reproduce
            except AttributeError:
                pass
            
    #metodo anterior cancion
    def retroceder_musica(self):
            self.estado= True#cuando se retrocede automaticamente se reproduce la cancion
            try:
                self.lista_musica.setCurrentRow(self.indice-1)#se disminuye la cancion
                self.play_musica()#se reproduce
            except AttributeError:
                pass
            
    #metodo estado del tiempo
    def estado_tiempo(self, estado):#verificar posicion en la que esta la cancion
        if self.player.state()==QMediaPlayer.PlayingState:
            self.bt_play.hide()#ocultar el boton play 
            self.bt_pausa.show()#mostramos el boton pausa
            self.estado= True
        #si no cumple realizar esto
        else:
            self.bt_play.show()
            self.bt_pausa.hide()
            self.estado= False
        #condicion para cunado la cancion este al final
        if self.player.position()==self.player.duration()and not self.player.position()==0:
            try:
                self.estado= True#reproducir
                self.lista_musica.setCurrentRow(self.indice+1)#reproducir la siguiente
                self.play_musica()
            except:
                pass
            
    #metodo duracion
    def duracion_cancion(self, t):
        self.slider_tiempo.setRange(0,t)#rango del tiempo del slider de 0 a t que es la duracion de la cancion
        m, s= (divmod(t*0.001,60))#minutos y segundos
        self.indicador_tiempo.setText(str(f'{int(m)}:{int(s)}'))#formato

    #metodo posicion
    def posicion_cancion(self, t):
        self.slider_tiempo.setValue(t)#posicion de la cancion
        m, s= (divmod(t*0.001,60))#minutos y segundos
        self.indicador_tiempo.setText(str(f'{int(m)}:{int(s)}'))#formato

    #metodo slider volumen
    def variar_volumen(self, valor):
        self.player.setVolume(valor)
        self.indicador_volumen.setText(str(valor))
        #cuando el volumen es 0 se muestra una imagen
        if valor==0:
            self.bt_volumen_0.show()
            self.bt_volumen_50.hide()
            self.bt_volumen_100.hide()
        #cuando esta entre 1 y 50 se muestra otra
        elif valor>0 and valor<50:
            self.bt_volumen_0.hide()
            self.bt_volumen_50.show()
            self.bt_volumen_100.hide()
        #y cuando es arrriba de 50 es otra
        elif valor>=50:
            self.bt_volumen_0.hide()
            self.bt_volumen_50.hide()
            self.bt_volumen_100.show()
    
    #metodo de la grafica
    def espectrum_grafica(self):
        x= np.linspace(0, 100, 10)
        self.data= np.random.normal(size= (10,100))
        #se crea una curva y se configura su diseño
        self.curva= self.graphWidget.plot(x, np.sin(x), symbol='o',
                    color= '#9074ff', pen= '#9074ff', width=2, brush='g',
                    symbolBrush= '#9074ff', symbolPen= '#9074ff',symbolSize= 10)
        self.graphWidget.hideAxis('left')#se ocultan los ejes
        self.graphWidget.hideAxis('bottom')#se ocultan los ejes
        
    #metodo de datos
    def update_datos(self):
        self.metadata_cancion()#se cambia con forme se cambia la cancion
        self.curva.setData(self.data[self.num%10])#variable que se incrementa entre 10
        if self.num == 0:
            self.graphWidget.enableAutoRange('xy',False)
        self.num +=1
        QtCore.QTimer.singleShot(100,self.update_datos)#se actualiza constantemente
            
#condicion para ejecutar
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mi_app = ReproductorMusica()
    mi_app.show()
    sys.exit(app.exec_())









