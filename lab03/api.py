from flask import Flask, request, jsonify
from cipher.rsa import RSACipher

app = Flask(__name__)
rsa_cipher = RSACipher()

@app.route('/api/rsa/generate_keys', methods=['GET'])
def generate_keys():
    rsa_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/rsa/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    private_key, public_key = rsa_cipher.load_keys()
    encrypted = rsa_cipher.encrypt(data['message'], public_key)
    return jsonify({'encrypted_message': encrypted.hex()})

@app.route('/api/rsa/decrypt', methods=['POST'])
def decrypt():
    data = request.json

    ciphertext_hex = data.get('ciphertext')
    if not ciphertext_hex:
        return jsonify({'error': 'ciphertext is missing or empty'}), 400

    try:
        ciphertext_bytes = bytes.fromhex(ciphertext_hex)
    except ValueError:
        return jsonify({'error': 'ciphertext must be a hex string'}), 400

    private_key, _ = rsa_cipher.load_keys()

    try:
        decrypted = rsa_cipher.decrypt(ciphertext_bytes, private_key)
    except Exception as e:
        return jsonify({'error': f'Decryption failed: {str(e)}'}), 400

    return jsonify({'decrypted_message': decrypted})

@app.route('/api/rsa/sign', methods=['POST'])
def sign():
    data = request.json
    private_key, _ = rsa_cipher.load_keys()
    signature = rsa_cipher.sign(data['message'], private_key)
    return jsonify({'signature': signature.hex()})

@app.route('/api/rsa/verify', methods=['POST'])
def verify():
    data = request.json
    _, public_key = rsa_cipher.load_keys()
    is_verified = rsa_cipher.verify(
        data['message'],
        bytes.fromhex(data['signature']),
        public_key
    )
    return jsonify({'is_verified': is_verified})

if __name__ == "__main__":
    app.run(debug=True)
