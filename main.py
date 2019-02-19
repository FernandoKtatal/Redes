import Physical as Physical
import DataLink as DataLink
from Packet import *
import Network as Network
from Constants import *

if __name__ == '__main__':
    
    #Example of sender
    station = Network.Network('01',STATION)
    packet = Packet(ip_origin = '01', ip_destination= '11', data='10100101')
    station.send_packet(packet)
    
    #Example of receiver
    # router = Network.Network(MACHINE_C,ROUTER)
    
    # datalink = DataLink.DataLink()
    # datalink.network_layer = router

    # physical = Physical.Physical()
    # physical.datalink_layer = datalink
    
    # physical.receive()
    
    

