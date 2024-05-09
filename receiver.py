class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(packet):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted"""
        pkt_checksum= packet['checksum']
        data_checksum=ord(packet['data'])
        if pkt_checksum!= data_checksum:
          return True
        # TODO provide your own implementation
        return False
        pass

    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # TODO provide your own implementation
        pkt_seq= rcv_pkt['sequence_number']
    
        if pkt_seq==exp_seq:
            return True
        return False
        pass


    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    def rdt_rcv(self, rcv_pkt):
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """
        print(f"\033[94m\033[1mReceiver \033[0m"+ f"\033[94m\033[4m\033[1mexpecting seq num:\033[0m"+f'{self.sequence}')
        # TODO provide your own implementation
        if RDTReceiver.is_expected_seq(rcv_pkt,self.sequence)==True and RDTReceiver.is_corrupted(rcv_pkt)==False :
            reply_pkt= RDTReceiver.make_reply_pkt(self.sequence,ord(self.sequence))
            if self.sequence=='0':
                self.sequence='1'
            else:
                self.sequence='0'
            ReceiverProcess.deliver_data(rcv_pkt['data'])
        else:
            if self.sequence=='0':
                last_arrived_seq='1'
            else:
                last_arrived_seq='0'
            reply_pkt=RDTReceiver.make_reply_pkt(last_arrived_seq, ord(last_arrived_seq))
        pkt_seq= reply_pkt['ack']
        pkt_checksum=reply_pkt['checksum']
        print(f"\033[94m\033[1mReceiver \033[0m"+ f"\033[94m\033[4m\033[1mreply with:\033[0m" + "{"+f" 'ack': "+f'{ pkt_seq}'+f", 'checksum': "+ f'{pkt_checksum}' +"}")

        # deliver the data to the process in the application layer
        #reply_pkt = RDTReceiver.make_reply_pkt()
        return reply_pkt
