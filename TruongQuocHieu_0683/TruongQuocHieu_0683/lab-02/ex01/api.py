from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

caesar_cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailFenceCipher()
playfair_cipher = PlayFairCipher()
transposition_cipher = TranspositionCipher()


# =========================
# HOME API
# =========================
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Advanced Information Security Practice API",
        "status": "running"
    })


# =========================
# CAESAR API
# =========================
@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    try:
        data = request.get_json()

        plain_text = data.get("plain_text", "")
        key = int(data.get("key", 0))

        encrypted_text = caesar_cipher.encrypt_text(plain_text, key)

        return jsonify({
            "plain_text": plain_text,
            "key": key,
            "encrypted_text": encrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    try:
        data = request.get_json()

        cipher_text = data.get("cipher_text", "")
        key = int(data.get("key", 0))

        decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)

        return jsonify({
            "cipher_text": cipher_text,
            "key": key,
            "decrypted_text": decrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =========================
# VIGENERE API
# =========================
@app.route("/api/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    try:
        data = request.get_json()

        plain_text = data.get("plain_text", "")
        key = data.get("key", "")

        encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)

        return jsonify({
            "plain_text": plain_text,
            "key": key,
            "encrypted_text": encrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/api/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    try:
        data = request.get_json()

        cipher_text = data.get("cipher_text", "")
        key = data.get("key", "")

        decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)

        return jsonify({
            "cipher_text": cipher_text,
            "key": key,
            "decrypted_text": decrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =========================
# RAIL FENCE API
# =========================
@app.route("/api/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    try:
        data = request.get_json()

        plain_text = data.get("plain_text", "")
        key = int(data.get("key", 0))

        encrypted_text = railfence_cipher.rail_fence_encrypt(plain_text, key)

        return jsonify({
            "plain_text": plain_text,
            "key": key,
            "encrypted_text": encrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/api/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    try:
        data = request.get_json()

        cipher_text = data.get("cipher_text", "")
        key = int(data.get("key", 0))

        decrypted_text = railfence_cipher.rail_fence_decrypt(cipher_text, key)

        return jsonify({
            "cipher_text": cipher_text,
            "key": key,
            "decrypted_text": decrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =========================
# PLAYFAIR API
# =========================
@app.route("/api/playfair/create-matrix", methods=["POST"])
def playfair_create_matrix():
    try:
        data = request.get_json()

        key = data.get("key", "")
        matrix = playfair_cipher.create_playfair_matrix(key)

        return jsonify({
            "key": key,
            "matrix": matrix
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/api/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    try:
        data = request.get_json()

        plain_text = data.get("plain_text", "")
        key = data.get("key", "")

        matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(plain_text, matrix)

        return jsonify({
            "plain_text": plain_text,
            "key": key,
            "matrix": matrix,
            "encrypted_text": encrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/api/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    try:
        data = request.get_json()

        cipher_text = data.get("cipher_text", "")
        key = data.get("key", "")

        matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, matrix)

        return jsonify({
            "cipher_text": cipher_text,
            "key": key,
            "matrix": matrix,
            "decrypted_text": decrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =========================
# TRANSPOSITION API
# =========================
@app.route("/api/transposition/encrypt", methods=["POST"])
def transposition_encrypt():
    try:
        data = request.get_json()

        plain_text = data.get("plain_text", "")
        key = int(data.get("key", 0))

        encrypted_text = transposition_cipher.encrypt(plain_text, key)

        return jsonify({
            "plain_text": plain_text,
            "key": key,
            "encrypted_text": encrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


@app.route("/api/transposition/decrypt", methods=["POST"])
def transposition_decrypt():
    try:
        data = request.get_json()

        cipher_text = data.get("cipher_text", "")
        key = int(data.get("key", 0))

        decrypted_text = transposition_cipher.decrypt(cipher_text, key)

        return jsonify({
            "cipher_text": cipher_text,
            "key": key,
            "decrypted_text": decrypted_text
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 400


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)