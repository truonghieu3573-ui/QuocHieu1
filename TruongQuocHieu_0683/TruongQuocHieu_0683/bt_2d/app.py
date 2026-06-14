from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading

app = Flask(__name__, template_folder='ui')
app.config['SECRET_KEY'] = 'secret-dh-aes-key!'
socketio = SocketIO(app, async_mode='threading')

# Lưu trữ kết nối client: sid -> dictionary chứa socket, aes_key
clients = {}

def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode('utf-8')

def receive_from_server(sid, client_socket, aes_key):
    """ Luồng nhận tin nhắn từ server TCP và gửi qua WebSocket tới đúng client """
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            print(f"\n[Client {sid}] Encrypted Message Received (Hex):\n{encrypted_message.hex()}")
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            # Emit tới Web client
            socketio.emit('receive_message', {'message': decrypted_message}, to=sid)
        except Exception as e:
            print(f"Error receiving for {sid}: {e}")
            break

@app.route('/')
def index():
    # Render giao diện từ file ui/mesage.html
    return render_template('mesage.html')

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    try:
        # Khởi tạo socket TCP và kết nối tới server_socket.py
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # Lưu ý: server_socket.py trong thư mục bt_2d hiện tại vẫn đang dùng RSA 
        # để trao đổi khóa AES. Do yêu cầu "không sửa server_socket.py", app.py 
        # bắt buộc phải dùng giao thức tương thích với server_socket.py (RSA).
        
        client_key = RSA.generate(2048)
        server_public_key = RSA.import_key(client_socket.recv(2048))
        client_socket.send(client_key.publickey().export_key(format='PEM'))
        encrypted_aes_key = client_socket.recv(2048)
        cipher_rsa = PKCS1_OAEP.new(client_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)

        clients[sid] = {
            'socket': client_socket,
            'aes_key': aes_key
        }
        
        t = threading.Thread(target=receive_from_server, args=(sid, client_socket, aes_key))
        t.daemon = True
        t.start()

        print(f"Client {sid} connected securely via TCP.")
        print(f"Shared AES Key (Hex): {aes_key.hex()}")
        emit('system_message', {'message': 'Connected securely to Server!'})
    except ConnectionRefusedError:
        emit('system_message', {'message': 'Server TCP is offline. Please start server_socket.py.'})
    except Exception as e:
        print(f"Connection failed for {sid}: {e}")
        emit('system_message', {'message': 'Failed to connect to server.'})


@socketio.on('send_message')
def handle_send_message(data):
    sid = request.sid
    if sid in clients:
        message = data.get('message', '')
        client_socket = clients[sid]['socket']
        aes_key = clients[sid]['aes_key']
        try:
            # Mã hóa AES và gửi qua TCP Server
            encrypted_message = encrypt_message(aes_key, message)
            print(f"\n[Client {sid}] Encrypted Message Sent (Hex):\n{encrypted_message.hex()}")
            client_socket.send(encrypted_message)
        except Exception as e:
            print(f"Error sending message for {sid}: {e}")


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in clients:
        try:
            encrypted_message = encrypt_message(clients[sid]['aes_key'], 'exit')
            clients[sid]['socket'].send(encrypted_message)
            clients[sid]['socket'].close()
        except:
            pass
        del clients[sid]
        print(f"Client {sid} disconnected.")


if __name__ == '__main__':
    print("Starting Web Interface on http://localhost:5000")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
