from Constants import *
from Network import * 
import Physical as Physical
import Util as Util
from Packet import *

class DataLink(object):
    def __init__(self):
        Util.log(self,"DataLink layer has started",WARNING)
        self.network_layer = Network(MACHINE_B, ROUTER)
        self.motives = {
            self.validate_bits : VALIDATE_BITS,
            self.validate_control_bits : VALIDATE_CONTROL_BITS,
            self.validate_message_lenght : VALIDATE_MESSAGE_LENGHT
        }
    
    def handle_message(self, message):
        validations = [self.validate_control_bits, self.validate_message_lenght , self.validate_bits]
        validated = True

        for validation in validations:
            if(validation(message) == False):
                validated = False
                reason = self.motives[validation]
                break

        if validated:
            message = message[1:-1]
            ip = message[0:2]
            packet = Packet(ip_origin=None, ip_destination=ip, data = message[2::])

            Util.log(self, "Message [{}] for the ip [{}] is validated".format(''.join(message[2::]),ip), SUCCESS)
            self.network_layer.route(packet)
        else:
            Util.log(self, "Message [{}] not validated due to [{}]".format(''.join(message), reason), FAIL)
            
    def send_packet(self, packet):
        physical_layer = Physical.Physical()
        messages = Util.split(packet.data,DATA_SIZE)
        for msg in messages:
            string = '{control}{ip}{data}{control}'.format(control=NOISE,ip=packet.ip_destination,data=msg)
            physical_layer.send(string)


    def validate_bits(self, message):
        return all([ a == '0' or a =='1' for a in message ])

    def validate_control_bits(self, message):
        return message[0] == '1' and message[-1] == '1'

    def validate_message_lenght(self, message):
        return len(message) == MESSAGE_SIZE