WeChat: cstutorcs
QQ: 749389476
Email: tutorcs@163.com
"""
    Sample code for Receiver
    Python 3
    Usage: python3 receiver.py receiver_port sender_port FileReceived.txt flp rlp
    coding: utf-8

    Notes:
        Try to run the server first with the command:
            python3 receiver_template.py 9000 10000 FileReceived.txt 1 1
        Then run the sender:
            python3 sender_template.py 11000 9000 FileToReceived.txt 1000 1

    Author: Rui Li (Tutor for COMP3331/9331)
"""
# here are the libs you may find it useful:
import datetime, time  # to calculate the time delta of packet transmission
import logging, sys  # to write the log
import socket  # Core lib, to send packet via UDP socket
from threading import Thread  # (Optional)threading will make the timer easily implemented
import random  # for flp and rlp function

BUFFERSIZE = 1024


class Receiver:
    def __init__(self, receiver_port: int, sender_port: int, filename: str, flp: float, rlp: float) -> None:
        '''
        The server will be able to receive the file from the sender via UDP
        :param receiver_port: the UDP port number to be used by the receiver to receive PTP segments from the sender.
        :param sender_port: the UDP port number to be used by the sender to send PTP segments to the receiver.
        :param filename: the name of the text file into which the text sent by the sender should be stored
        :param flp: forward loss probability, which is the probability that any segment in the forward direction (Data, FIN, SYN) is lost.
        :param rlp: reverse loss probability, which is the probability of a segment in the reverse direction (i.e., ACKs) being lost.

        '''
        self.address = "127.0.0.1"  # change it to 0.0.0.0 or public ipv4 address if want to test it between different computers
        self.receiver_port = int(receiver_port)
        self.sender_port = int(sender_port)
        self.server_address = (self.address, self.receiver_port)

        # init the UDP socket
        # define socket for the server side and bind address
        logging.debug(f"The sender is using the address {self.server_address} to receive message!")
        self.receiver_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.receiver_socket.bind(self.server_address)
        pass

    def run(self) -> None:
        '''
        This function contain the main logic of the receiver
        '''
        while True:
            try:
                # try to receive any incoming message from the sender
                incoming_message, sender_address = self.receiver_socket.recvfrom(BUFFERSIZE)
                # logging.debug(f"client{sender_address} send a message: {incoming_message.decode('utf-8')}")

                # 回复ACK的功能
                # reply_message = "ACK"
                # self.receiver_socket.sendto(reply_message.encode("utf-8"), sender_address)

                # 收到SYN，发回一个ACK
                pack_type = int.from_bytes(incoming_message[:2], byteorder='big')
                seq_no = int.from_bytes(incoming_message[2:4], byteorder='big')
                if pack_type == 2:  # 收到一个SYN，发送回一个ACK和seq+1
                    ret_type = 1
                    seq_no = seq_no + 1
                    if seq_no == 65536:  # 如果seq到最大值，回环回0
                        seq_no = 0
                    message = ret_type.to_bytes(2, "big") + seq_no.to_bytes(2, "big")
                    # 发送回一个ACK（STP字段格式）
                    self.receiver_socket.sendto(message.encode("utf-8"), self.sender_address)
            except ConnectionResetError:
                continue  # 不是continue，之后改，应该是覆盖原先已经写过的日志，按照要求中写日志




            # 将收到的mess写入文件
                # with open(self.filename, "wb+") as file:
                    # file.write(incoming_message)

            # 原位置：reply "ACK" once receive any message from sender
            # reply_message = "ACK"
            # self.receiver_socket.sendto(reply_message.encode("utf-8"), sender_address)


if __name__ == '__main__':
    # logging is useful for the log part: https://docs.python.org/3/library/logging.html
    logging.basicConfig(
        # filename="Receiver_log.txt",
        stream=sys.stderr,
        level=logging.DEBUG,
        format='%(asctime)s,%(msecs)03d %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d:%H:%M:%S')

    if len(sys.argv) != 6:
        print(
            "\n===== Error usage, python3 receiver.py receiver_port sender_port FileReceived.txt flp rlp ======\n")
        exit(0)

    receiver = Receiver(*sys.argv[1:])
    receiver.run()
