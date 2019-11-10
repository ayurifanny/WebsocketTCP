from base64 import b64encode
from hashlib import sha1

GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

# belom dipake
handshake = (
        "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
        "Upgrade: WebSocket\r\n"
        "Connection: Upgrade\r\n"
        "WebSocket-Origin: %(origin)s\r\n"
        "WebSocket-Location: ws://%(bind)s:%(port)s/\r\n"
        "Sec-Websocket-Accept: %(accept)s\r\n"
        "Sec-Websocket-Origin: %(origin)s\r\n"
        "Sec-Websocket-Location: ws://%(bind)s:%(port)s/\r\n"
        "\r\n"
    )

def get_response_key(key):
    hashed = sha1(key.encode() + GUID.encode())
    response_key = b64encode(hashed.digest()).strip()
    return response_key.decode('ASCII')

def parse_http_header(header):
        headers = {}
        # first line should be HTTP GET
        get_method = header.split(' ')
        other_header = header.split("\n")
        
        # remaining should be headers
        for x in other_header[1:]:
            # print(x)
            head_value = x.split(':')
            # print(head_value)
            # print(other_header)
            try:
                sth = head_value[1]
            except IndexError:
                break

            headers[head_value[0].lower().strip()] = head_value[1].strip()
        return headers, get_method[0]

def req_handshake(request):
    headers, get_method = parse_http_header(request)
    try:
        assert headers['upgrade'].lower() == 'websocket'
    except AssertionError:
        response = handshake_response_failed(request)
            # request.keep_alive = False
    if (get_method.upper().startswith('GET')):
        try:
            key = headers['sec-websocket-key']
            response = handshake_response_success(request, key)
        except KeyError:
            print("NO KEY AW")
            # request.keep_alive = False
            response = handshake_response_failed(request)
    return response

def handshake_response_success(request, key):
    hashed = sha1(key.encode() + GUID.encode())
    response_key = b64encode(hashed.digest()).strip()
    return \
        'HTTP/1.1 101 Switching Protocols\r\n'\
        'Upgrade: websocket\r\n'              \
        'Connection: Upgrade\r\n'             \
        'Sec-WebSocket-Accept: %s\r\n'        \
        '\r\n' % response_key.decode('ASCII')

def handshake_response_failed(request):
    return "HTTP/1.1 400 Bad Request"

