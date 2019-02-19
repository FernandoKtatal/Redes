import pyaudio
import audioop
from threading import Thread
import time
from datetime import datetime
import Util as Util
from Constants import *
import sys
import multiprocessing
from DataLink import *
 
class Physical(object):
    
    def __init__(self):
        # Variaveis globais para serem manipuladas dentro do loop de mensageria
        Util.log(self,"Physical layer has started", WARNING)
        self.buffer = []
        self.is_transmitting = False
        self.datalink_layer = DataLink()
    
    def manager(self, seconds):
        #print("Iniciou o timer")
        time.sleep(seconds)
        #print("Finalizou o timer")
        copy_of_buffer = self.buffer.copy()
        #print("copy lenght",len(copy_of_buffer))
        self.is_transmitting = False
        Util.log(self, 'Ending comunication..', INFO)
        message = []

        # Task 1: Agrupar por segundos
        i = 0
        while i in range(len(copy_of_buffer)):
            #print(i)
            #print("len", len(copy_of_buffer))
            if i == len(copy_of_buffer):
                break

            if i is not 0:
                (data, miliseconds) = copy_of_buffer[i]
                diff = miliseconds - (copy_of_buffer[i-1][TIME_ATT])
                #print(diff)
                if diff < 1000:
                    del copy_of_buffer[i] 
                    i = i - 1  
            i += 1
            #print("copy", copy_of_buffer)

        # Task 2: Incluir os zeros na mensagem -> [10]
        
        for i in range(len(copy_of_buffer)):
            #a partir do segundo
            if i is not 0:
                (data, miliseconds) = copy_of_buffer[i]
                diff = miliseconds - (copy_of_buffer[i-1][TIME_ATT])
                #adicionando zeros entre os noises
                
                message.extend([SILENCE]*(int)((diff / 1000) - 1))
                #adicionando o noise
                message.append(copy_of_buffer[i][0])
                #print('message: ', message)
            #append do primerio 1 de controle
            else:
                message.append(copy_of_buffer[i][0])

        Util.log(self, 'Sending [{}] to DataLink layer'.format(''.join(message)), INFO)
        self.datalink_layer.handle_message(''.join(message))

    def receive(self):
        p = pyaudio.PyAudio()
        
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        # Loop de mensageria
        while True:
            #print("escutando...")
            #validacoes iniciais
            data = stream.read(CHUNK, exception_on_overflow = False)
            
            if data:
                
                volume_of_data = Util.getVol(data)
                
                # Ouviu um 1
                if volume_of_data > THRESHOLD:
                    #print("leu 1")
                    #inserindo no buffer da mensagem
                    if self.is_transmitting:
                        #print("lendo...")
                        self.buffer.append((NOISE,Util.timestamp()))
                        #inicializa um novo buffer e starta a thread
                    else:
                        self.buffer = []
                        #inserindo o bit de controle inicial
                        self.buffer.append((NOISE,Util.timestamp()))
                        self.is_transmitting = True
                        Util.log(self, 'Starting comunication..', INFO)
                        Thread(target = self.manager, args = (SECONDS, )).start()

    def send(self, message):
        Util.log(self, 'Sending [{}] to the environment'.format(''.join(message)), INFO)
        aux = []
        for bit in message:
            if bit == NOISE:
                aux.append(NOISE)
                sys.stdout.write('\r{}'.format(''.join(aux)))
                sys.stdout.flush()
                Util.playBeep()        
            else:
                aux.append(SILENCE)
                sys.stdout.write('\r{}'.format(''.join(aux)))
                sys.stdout.flush()
                time.sleep(SLEEP_TIME)
        print('\n')