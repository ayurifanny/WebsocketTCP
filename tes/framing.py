import codecs
import struct

# WebSocket frame structure
'''
Frame format:  
​​
      0                   1                   2                   3
      0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
     +-+-+-+-+-------+-+-------------+-------------------------------+
     |F|R|R|R| opcode|M| Payload len |    Extended payload length    |
     |I|S|S|S|  (4)  |A|     (7)     |             (16/64)           |
     |N|V|V|V|       |S|             |   (if payload len==126/127)   |
     | |1|2|3|       |K|             |                               |
     +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
     |     Extended payload length continued, if payload len == 127  |
     + - - - - - - - - - - - - - - - +-------------------------------+
     |                               |Masking-key, if MASK set to 1  |
     +-------------------------------+-------------------------------+
     | Masking-key (continued)       |          Payload Data         |
     +-------------------------------- - - - - - - - - - - - - - - - +
     :                     Payload Data continued ...                :
     + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
     |                     Payload Data continued ...                |
     +---------------------------------------------------------------+
'''

# convert int to ASCII (bytes)
def intToBytes(num):
	decode = codecs.getdecoder("hex_codec")
	num = str(hex(num))[2:].zfill(2)

	return decode(num)[0]

# decode payload with mask
def unmask(payload, key):
	result = b''
	
	for i in range(len(payload)):
		result += intToBytes(payload[i] ^ key[i % 4])

	return result

# frame parsing, seperating each sector in frame structure
def parse(frame):
    fin = frame[0] >> 7
    rsv1 = (frame[0] & 0x40) >> 6
    rsv2 = (frame[0] & 0x20) >> 5
    rsv3 = (frame[0] & 0x10) >> 4
    opcode = frame[0] & 0x0f

    mask = frame[1] >> 7
    pay_len = frame[1] & 0x7f

    if (pay_len <= 125):
        payload_len = pay_len
    elif (pay_len == 126):
        payload_len = int(frame[2:4].hex(), 16) 
    else:
        payload_len = int(frame[2:10].hex(), 16)

    # check mask, if available then unmask
    masking_key = None
    if (mask == 1):
        if(pay_len <= 125):
            masking_key = frame[2:6]
            payload_data = unmask(frame[6:], masking_key)
        elif(pay_len == 126):
            masking_key = frame[4:8]
            payload_data = unmask(frame[8:], masking_key)
        else:
            masking_key = frame[10:14]
            payload_data = unmask(frame[14:], masking_key)
    else:
        if(pay_len <= 125):
            payload_data = frame[2:]
        elif(pay_len == 126):
            payload_data = frame[4:]
        else:
            payload_data = frame[10:]

    result = {
        "FIN": fin,
        "RSV1": rsv1,
        "RSV2": rsv2,
        "RSV3": rsv3,
        "OPCODE": opcode,
        "MASK": mask,
        "PAYLOAD_LEN": payload_len,
        "MASKING_KEY": masking_key,
        "PAYLOAD": payload_data,
    }

    return result

def build(frame, command):
    packet = bytearray()
    packet.append(frame['FIN'] << 7 | frame['OPCODE'])
    
    length = frame['PAYLOAD_LEN']
    if (command == "echo"):
        length -= 6

    if (length <= 125):
        packet.append(length)
    elif (length > 125 and length <= 65535):
        packet.append(126)
        packet.extend(struct.pack(">H", length))
    elif (length < 18446744073709551616):
        packet.append(127)
        packet.extend(struct.pack(">Q", length))
    else:
        raise Exception("Message too big")

    if (command == "echo"):
        phrase = frame['PAYLOAD'].decode().split(" ", 1)
        packet.extend(phrase[1].encode())
        print(packet)
    elif (command == "submission"):
        pass
    elif (command == "file"):
        pass
    else:
        packet.extend(frame['PAYLOAD'])

    return packet