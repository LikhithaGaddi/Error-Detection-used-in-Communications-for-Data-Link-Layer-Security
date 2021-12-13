import socket
import numpy as np
import pickle

s = socket.socket()

port = 45360

s.connect(('127.0.0.1', port))

A = np.array([[-3, -3, -4], [0, 1, 1], [4, 3, 4]])
aplhabets_to_numbers = {'A': 1,'B': 2,'C': 3,'D': 4,'E': 5,'F': 6,'G': 7,'H': 8,'I': 9,'J': 10,'K': 11,'L': 12,
                        'M': 13,'N': 14,'O': 15,'P': 16,'Q': 17,'R': 18,'S': 19,'T': 20,'U': 21,'V': 22,'W': 23,'X': 24,
                        'Y': 25,'Z': 26,' ':27 }


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
    if (index == len(original)):
        return temp
    temp += original[index]
    if(temp[0] == '1'):
        temp = xor(int(temp), int(key))
    temp = temp[1:]
    return crc_helper(original, index+1, temp, key)

def convert_to_matrix(msg):
    m = []
    for i in range(0, len(msg)):
        m.append(aplhabets_to_numbers[msg[i].upper()])
    return m

def get_crc(msg, key):
    T = convert_to_matrix(msg)
    # print(T)
    original = get_binary_from_array(T)
    # print(original)
    return crc_helper(original, len(key) - 1, original[:len(key) - 1], key)

def encode_data(a, b):
    return pickle.dumps([a, b])

def encrypt_data(msg,key):
    while len(msg) % 3 != 0:
        msg += " "
    
    m = convert_to_matrix(msg)
    cols = len(msg) // 3
    T_matrix = np.reshape(m, (cols, 3))
    T_matrix = np.transpose(T_matrix)
    EncData = np.matmul(A, T_matrix)
    crc_value = get_crc(msg, key)
    send_data = encode_data(EncData, crc_value)
    return send_data

while True:
    key = '1010'
    msg = input("Enter message: ")
    send_data = encrypt_data(msg,key)
    s.sendall(send_data)
    print("Status: ",s.recv(1024).decode("utf-8"))


s.close()