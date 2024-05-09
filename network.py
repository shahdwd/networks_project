import random
import time
from receiver import RDTReceiver

"""
NOTE: YOU SHOULD NOT MODIFY THIS CLASS
"""


class NetworkLayer:
    """ The network layer that deliver packets and acknowledgments between sender and receiver """

    def __init__(self, reliability=1.0, delay=1.0, pkt_corrupt=True, ack_corrupt=True):
        """ initialize the network layer
        :param reliability: the probability that the network layer will deliver the message correctly
        :param delay: the round trip time for sending a packet and receive a reply
        :param pkt_corrupt: sender packets will be corrupted
        :param ack_corrupt: receiver acknowledgments will be corrupted
        """
        self.reliability = reliability
        self.packet = None
        self.reply = None
        self.delay = delay
        self.pkt_corrupt = pkt_corrupt
        self.ack_corrupt = ack_corrupt
        self.recv = RDTReceiver()  # connect the network layer to the receiver

    def get_network_reliability(self):
        """ show network layer reliability
        :return: a float number represent the current network reliability
        """
        return self.reliability

    def __packet_corruption_probability(self):
        """ calculate the probability that a pocket will be corrupted
        :return: True if the probability greater than the network reliability
        """
        ran = random.uniform(0, 1)
        if ran > self.reliability:
            return True
        return False

    def __corrupt_packet(self):
        """ Corrupt the sender packet, it could corrupt the seq_num, the data or the checksum
        :return: no return value
        """
        ran = random.randint(1, 90)
        if ran < 30:
            self.packet['sequence_number'] = chr(random.randint(ord('2'), ord('9')))
            return
        if ran < 60:
            self.packet['data'] = chr(random.randint(ord('!'), ord('}')))
            return
        if ran < 90:
            self.packet['checksum'] = random.randint(ord('!'), ord('}'))

    def __corrupt_reply(self):
        """ Corrupt the receiver reply (acknowledgments) packet
        :return: no return value
        """
        ran = random.randint(1, 100)
        if ran < 50:
            self.reply['ack'] = chr(random.randint(2, 9))
        else:
            self.reply['checksum'] = random.randint(ord('2'), ord('9'))

    def udt_send(self, frame):
        """ implement the delivery service of the unreliable network layer
        :param frame: a python dictionary represent the a sender's packet or a receiver's reply
        :return: the receiver's reply as a python dictionary returned to the sender
        """

        # TODO: You may add ONLY print statements to this function for debugging purpose
        self.packet = frame
        s_test = self.__packet_corruption_probability()

        if s_test and self.pkt_corrupt:
            self.__corrupt_packet()
            pkt_seq= self.packet['sequence_number']
            pkt_data=self.packet['data']
            pkt_checksum=self.packet['checksum']
            print(f"\033[91m\033[1mNetwork Layer: \033[0m"+ f"\033[91m\033[4m\033[1mCorruption occured\033[0m" + "{"+f" 'sequence_number': "+f'{ pkt_seq}'+f", 'data': "+ f'{pkt_data}' +f", 'checksum': "+ f'{pkt_checksum}' +"}")
        time.sleep(self.delay)

        # bridge|connect the RDT sender and receiver
        self.reply = self.recv.rdt_rcv(self.packet)
       # print( f"\033[91m\033[4m\033[1mYour Colored and Underlined Statement\033[0m")
        r_test = self.__packet_corruption_probability()
        if r_test and self.ack_corrupt:
            self.__corrupt_reply()
            pkt_seq= self.reply['ack']
            pkt_checksum=self.reply['checksum']
            print(f"\033[91m\033[1mNetwork Layer: \033[0m"+ f"\033[91m\033[4m\033[1mCorruption occured\033[0m" + "{"+f" 'ack': "+f'{ pkt_seq}'+f", 'checksum': "+ f'{pkt_checksum}' +"}")

        return self.reply
