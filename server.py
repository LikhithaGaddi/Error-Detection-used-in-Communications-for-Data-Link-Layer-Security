import socket
import pickle
import numpy as np
from _thread import *


numbers_to_alphabtes = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J', 11: 'K', 12: 'L',
                        13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'v', 23: 'W', 24: 'X',
                        25: 'Y', 26: 'Z', 27: ' '}


aplhabets_to_numbers = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12,
                        'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
                        'Y': 25, 'Z': 26, ' ': 27}


A_inverse = np.array([[1, 0, 1], [4, 4, 3], [-4, -3, -3]])


s = socket.socket()
print("Socket successfully created")

port = 45360

s.bind(('', port))
print("socket binded to %s" % (port))

s.listen(10)
print("socket is listening")


def get_binary_from_array(T):
    b = ''
    for i in T:
        b += (bin(i).replace("0b", ""))
    return b


def xor(a, b):
    ans = ''
    while (a > 0 and b > 0):
        ans = str(int(a % 10) ^ int(b % 10)) + ans
        a //= 10
        b //= 10
    if (a != 0 or b != 0):
        ans = str(int(a % 10) ^ int(b % 10)) + ans
    return ans


def crc_helper(original, index, temp, key):
    if (index >= len(original)):
        return temp
    temp += original[index]
    if(temp[0] == '1'):
        temp = xor(int(temp), int(key))
    temp = temp[1:]
    return crc_helper(original, index+1, temp, key)


def convert_to_matrix(msg):
    m = []
    try:
        for i in range(0, len(msg)):
            m.append(aplhabets_to_numbers[msg[i].upper()])
        return m
    except:
        print("Incorrect message")


def get_crc(msg, key):
    T = convert_to_matrix(msg)
    # print(T)
    original = get_binary_from_array(T)
    # original+="101"
    # print(original)
    return crc_helper(original, len(key) - 1, original[:len(key) - 1], key)


def decode_data(c):
    matrix, crc = pickle.loads(c.recv(1024))
    return matrix, crc


def decrypt_data(m):
    m = np.matmul(A_inverse, m)
    m = np.transpose(m)
    msg = ""
    try:
        for i in range(len(m)):
            for j in range(len(m[0])):
                msg += numbers_to_alphabtes[m[i][j]]
        return msg
    except:
        print("Keyerror found")


def communicate_with_client(c,addr):
    while True:
        key = '1010'
        matrix, crc = decode_data(c)
        message = decrypt_data(matrix)
        # message+="heyya"
        crc_verified = get_crc(message, key)
        # print(crc)
        # print(crc_verified)
        if (crc != crc_verified):
            print("CRC not matched")
            c.sendall("ERROR DETECTED: CRC not matched".encode("utf-8"))
        else:
            print("From client " + str(addr)+" : "+str(message.lower()))
            c.sendall("success".encode("utf-8"))

    c.close()

while True:
    c, addr = s.accept()
    print('Got connection from', addr)
    start_new_thread(communicate_with_client, (c,addr[1] ))
    

s.close()