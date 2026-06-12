from flask import Flask, render_template, request
from ex01.cipher.caesar import CaesarCipher
from ex01.cipher.vigenere import VigenereCipher
from ex01.cipher.railfence import RailFenceCipher
from ex01.cipher.playfair import PlayFairCipher
from ex01.cipher.transposition import TranspositionCipher

app = Flask(__name__)


# =========================
# HOME PAGE
# =========================
@app.route("/")
def home():
    return render_template("index.html")


# =========================
# CAESAR CIPHER
# =========================
@app.route("/caesar")
def caesar():
    return render_template("caesar.html")


@app.route("/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])

    cipher = CaesarCipher()
    encrypted_text = cipher.encrypt_text(text, key)

    return render_template(
        "caesar.html",
        plain_text=text,
        plain_key=key,
        encrypted_text=encrypted_text
    )


@app.route("/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])

    cipher = CaesarCipher()
    decrypted_text = cipher.decrypt_text(text, key)

    return render_template(
        "caesar.html",
        cipher_text=text,
        cipher_key=key,
        decrypted_text=decrypted_text
    )


# =========================
# VIGENERE CIPHER
# =========================
@app.route("/vigenere")
def vigenere():
    return render_template("vigenere.html")


@app.route("/vigenere/encrypt", methods=["POST"])
def vigenere_encrypt():
    text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]

    cipher = VigenereCipher()
    encrypted_text = cipher.vigenere_encrypt(text, key)

    return render_template(
        "vigenere.html",
        plain_text=text,
        plain_key=key,
        encrypted_text=encrypted_text
    )


@app.route("/vigenere/decrypt", methods=["POST"])
def vigenere_decrypt():
    text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]

    cipher = VigenereCipher()
    decrypted_text = cipher.vigenere_decrypt(text, key)

    return render_template(
        "vigenere.html",
        cipher_text=text,
        cipher_key=key,
        decrypted_text=decrypted_text
    )


# =========================
# RAIL FENCE CIPHER
# =========================
@app.route("/railfence")
def railfence():
    return render_template("railfence.html")


@app.route("/railfence/encrypt", methods=["POST"])
def railfence_encrypt():
    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])

    cipher = RailFenceCipher()
    encrypted_text = cipher.rail_fence_encrypt(text, key)

    return render_template(
        "railfence.html",
        plain_text=text,
        plain_key=key,
        encrypted_text=encrypted_text
    )


@app.route("/railfence/decrypt", methods=["POST"])
def railfence_decrypt():
    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])

    cipher = RailFenceCipher()
    decrypted_text = cipher.rail_fence_decrypt(text, key)

    return render_template(
        "railfence.html",
        cipher_text=text,
        cipher_key=key,
        decrypted_text=decrypted_text
    )


# =========================
# PLAYFAIR CIPHER
# =========================
@app.route("/playfair")
def playfair():
    return render_template("playfair.html")


@app.route("/playfair/creatematrix", methods=["POST"])
def playfair_create_matrix():
    key = request.form["inputMatrixKey"]

    cipher = PlayFairCipher()
    playfair_matrix = cipher.create_playfair_matrix(key)

    return render_template(
        "playfair.html",
        matrix_key=key,
        playfair_matrix=playfair_matrix
    )


@app.route("/playfair/encrypt", methods=["POST"])
def playfair_encrypt():
    text = request.form["inputPlainText"]
    key = request.form["inputKeyPlain"]

    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    encrypted_text = cipher.playfair_encrypt(text, matrix)

    return render_template(
        "playfair.html",
        plain_text=text,
        plain_key=key,
        encrypted_text=encrypted_text,
        matrix_key=key,
        playfair_matrix=matrix
    )


@app.route("/playfair/decrypt", methods=["POST"])
def playfair_decrypt():
    text = request.form["inputCipherText"]
    key = request.form["inputKeyCipher"]

    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    decrypted_text = cipher.playfair_decrypt(text, matrix)

    return render_template(
        "playfair.html",
        cipher_text=text,
        cipher_key=key,
        decrypted_text=decrypted_text,
        matrix_key=key,
        playfair_matrix=matrix
    )


# =========================
# TRANSPOSITION CIPHER
# =========================
@app.route("/transposition")
def transposition():
    return render_template("transposition.html")


@app.route("/transposition/encrypt", methods=["POST"])
def transposition_encrypt():
    text = request.form["inputPlainText"]
    key = int(request.form["inputKeyPlain"])

    cipher = TranspositionCipher()
    encrypted_text = cipher.encrypt(text, key)

    return render_template(
        "transposition.html",
        plain_text=text,
        plain_key=key,
        encrypted_text=encrypted_text
    )


@app.route("/transposition/decrypt", methods=["POST"])
def transposition_decrypt():
    text = request.form["inputCipherText"]
    key = int(request.form["inputKeyCipher"])

    cipher = TranspositionCipher()
    decrypted_text = cipher.decrypt(text, key)

    return render_template(
        "transposition.html",
        cipher_text=text,
        cipher_key=key,
        decrypted_text=decrypted_text
    )


# =========================
# MAIN FUNCTION
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)