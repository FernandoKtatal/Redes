import Util as Util
from Constants import *
import DataLink as DataLink
import time

class Network(object):

    def __init__(self, ip, TYPE):
        Util.log(self, 'IP [{0}] / TYPE [{1}] Network layer has started'.format(ip,TYPE), WARNING)
        self.ip = ip
        self.type = TYPE
        self.route_table = {
            MACHINE_A: MACHINE_D,
            MACHINE_B: MACHINE_D,
            MACHINE_C: MACHINE_D,
            MACHINE_D: MACHINE_D
        }

    def send_packet(self, packet):
        if(packet.ip_destination=='11'):
            packet.ip_destination = '00'
        elif (packet.ip_destination=='01'):
            packet.ip_destination = '10'

        DataLink.DataLink().send_packet(packet)

    def route(self, packet):
        ip = packet.ip_destination
        data = packet.data

        if(''.join(ip) == self.ip):
            Util.log(self,"Message {} received".format(''.join(data)), SUCCESS)
        elif(self.type == ROUTER):

            if(ip == '00'):
                packet.ip_destination = '11'
            elif (ip == '10'):
                packet.ip_destination = '01'
            
            Util.log(self, 'Routing [{}] from [{}] to [{}] inside router '.format(data, ip, packet.ip_destination), INFO)
            time.sleep(1)
            DataLink.DataLink().send_packet(packet)
        else:
            Util.log(self,"[{}] Message {} discarded".format(type(self).__name__,''.join(data)), FAIL)
