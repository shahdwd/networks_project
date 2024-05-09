from re import ASCII


class SenderProcess:
    """ Represent the sender process in the application layer  """

    __buffer = list()

    @staticmethod
    def set_outgoing_data(buffer):
        """ To set the message the process would send out over the network
        :param buffer:  a python list of characters represent the outgoing message
        :return: no return value
        """
        SenderProcess.__buffer = buffer
        return

    @staticmethod
    def get_outgoing_data():
        """ To get the message the process would send out over the network
        :return:  a python list of characters represent the outgoing message
        """
        return SenderProcess.__buffer


class RDTSender:
    """ Implement the Reliable Data Transfer Protocol V2.2 Sender Side """

    def __init__(self, net_srv):
        """ This is a class constructor
            It initialize the RDT sender sequence number  to '0' and the network layer services
            The network layer service provide the method udt_send(send_pkt)
        """
        self.sequence = '0'
        self.net_srv = net_srv

    @staticmethod
    def get_checksum(data):
        """ Calculate the checksum for outgoing data
        :param data: one and only one character, for example data = 'A'
        :return: the ASCII code of the character, for example ASCII('A') = 65
        """
        # TODO provide your own implementation
        checksum =ord(data) # you need to change that
        return checksum

    @staticmethod
    def clone_packet(packet):
        """ Make a copy of the outgoing packet
        :param packet: a python dictionary represent a packet
        :return: return a packet as python dictionary
        """
        pkt_clone = {
            'sequence_number': packet['sequence_number'],
            'data': packet['data'],
            'checksum': packet['checksum']
        }
        return pkt_clone

    @staticmethod
    def is_corrupted(reply):
        """ Check if the received reply from receiver is corrupted or not
        :param reply: a python dictionary represent a reply sent by the receiver
        :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        # TODO provide your own implementation
        expected_checksum=reply['checksum']
        msg_checksum= ord(reply['ack'])
        if expected_checksum != msg_checksum:
            return True
        return False
        pass

    @staticmethod
    def is_expected_seq(reply, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
        :param reply: a python dictionary represent a reply sent by the receiver
        :param exp_seq: the sender expected sequence number '0' or '1' represented as a character
        :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # TODO provide your own implementation
        msg_seq= reply['ack']
        return msg_seq==exp_seq

    @staticmethod
    def make_pkt(seq, data, checksum):
        """ Create an outgoing packet as a python dictionary
        :param seq: a character represent the sequence number of the packet, the one expected by the receiver '0' or '1'
        :param data: a single character the sender want to send to the receiver
        :param checksum: the checksum of the data the sender will send to the receiver
        :return: a python dictionary represent the packet to be sent
        """
        packet = {
            'sequence_number': seq,
            'data': data,
            'checksum': checksum
        }
        return packet

    def rdt_send(self, process_buffer):
        """ Implement the RDT v2.2 for the sender
        :param process_buffer:  a list storing the message the sender process wish to send to the receiver process
        :return: terminate without returning any value
        """

        # for every character in the buffer
        for data in process_buffer:
            checksum = self.get_checksum(data)
            pkt = self.make_pkt(self.sequence, data, checksum)
            pkt_clone= RDTSender.clone_packet(pkt)
            
            print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1mexpecting seq num: \033[0m" +f'{self.sequence}')
            pkt_seq= pkt['sequence_number']
            pkt_data=pkt['data']
            pkt_checksum=pkt['checksum']
            print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1msending:\033[0m" + "{"+f" 'sequence_number': "+f'{ pkt_seq}'+f", 'data': "+ f'{pkt_data}' +f", 'checksum': "+ f'{pkt_checksum}' +"}")
            reply = self.net_srv.udt_send(pkt_clone)
            reply_seq= reply['ack']
            reply_checksum=reply['checksum']
            print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1mreceived:\033[0m" + "{"+f" 'ack': "+f'{ reply_seq}'+f", 'checksum': "+ f'{reply_checksum}' +"}")
            #print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1mexpecting seq num: \033[0m" +f'{self.sequence}')
            while RDTSender.is_corrupted(reply)==True  or  RDTSender.is_expected_seq(reply,self.sequence)==False:
                pkt_clone= RDTSender.clone_packet(pkt)
                print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1mexpecting seq num: \033[0m" +f'{self.sequence}')
                clone_seq= pkt_clone['sequence_number']
                clone_data=pkt_clone['data']
                clone_checksum=pkt_clone['checksum']
                print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1msending:\033[0m" + "{"+f" 'sequence_number': "+f'{clone_seq}'+f", 'data': "+ f'{clone_data}' +f", 'checksum': "+ f'{clone_checksum}' +"}")
                reply = self.net_srv.udt_send(pkt_clone)
                reply_seq= reply['ack']
                reply_checksum=reply['checksum']
                print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1mreceived:\033[0m" + "{"+f" 'ack': "+f'{ reply_seq}'+f", 'checksum': "+ f'{reply_checksum}' +"}")
                #print(f"\033[95m\033[1mSender \033[0m"+ f"\033[95m\033[4m\033[1mexpecting seq num: \033[0m" +f'{self.sequence}')
            # if self.is_corrupted(reply)==True  or  self.is_expected_seq(reply,self.sequence)==False :
            #    while True:
            #        pkt_clone= self.clone_packet(pkt)
            #        reply = self.net_srv.udt_send(pkt_clone)
            #        if (self.is_corrupted(reply)==False )and self.is_expected_seq(reply,self.sequence)==True :
            #            break
            if self.sequence=='1':
                self.sequence= '0'
            else :
                self.sequence='1'       
        print(f'Sender Done!')
        return
