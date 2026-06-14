from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading

app = Flask(__name__, template_folder='ui')
app.config['SECRET_KEY'] = 'secret-aes-rsa-key!'
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
        # 1. Khởi tạo socket TCP và kết nối tới server (như client_1.py)
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))

        # 2. Tạo cặp khóa RSA
        client_key = RSA.generate(2048)

        # 3. Nhận public key của server
        server_public_key = RSA.import_key(client_socket.recv(2048))

        # 4. Gửi public key của client cho server
        client_socket.send(client_key.publickey().export_key(format='PEM'))

        # 5. Nhận khóa AES đã mã hóa từ server
        encrypted_aes_key = client_socket.recv(2048)

        # 6. Giải mã khóa AES bằng private key của client
        cipher_rsa = PKCS1_OAEP.new(client_key)
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)

        # 7. Lưu lại kết nối và bắt đầu luồng nhận tin nhắn
        clients[sid] = {
            'socket': client_socket,
            'aes_key': aes_key
        }
        
        t = threading.Thread(target=receive_from_server, args=(sid, client_socket, aes_key))
        t.daemon = True
        t.start()

        print(f"Client {sid} connected securely via TCP.")
        emit('system_message', {'message': 'Connected securely to AES-RSA Socket Server!'})
    except ConnectionRefusedError:
        emit('system_message', {'message': 'Server TCP is offline. Please start server_1.py.'})
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
            client_socket.send(encrypted_message)
        except Exception as e:
            print(f"Error sending message for {sid}: {e}")


@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in clients:
        try:
            # Gửi tin nhắn 'exit' để server TCP biết và đóng kết nối
            encrypted_message = encrypt_message(clients[sid]['aes_key'], 'exit')
            clients[sid]['socket'].send(encrypted_message)
            clients[sid]['socket'].close()
        except:
            pass
        del clients[sid]
        print(f"Client {sid} disconnected.")


if __name__ == '__main__':
    # Chạy server Flask trên cổng 5000 (mặc định)
    print("Starting Web Interface on http://localhost:5000")
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
