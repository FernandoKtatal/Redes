class Packet(object):
    def __init__(self, ip_origin, ip_destination, data):
        self.ip_origin = ip_origin
        self.ip_destination = ip_destination
        self.data = data 

    def __str__(self):
        return '{0}{1}{2}'.format(self.ip_origin, self.ip_destination, self.data)