from flask import Flask, render_template, request
import hashlib

app = Flask(__name__)

def initialize_s_box(key):
    s = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s[i] + key[i % len(key)]) % 256
        s[i], s[j] = s[j], s[i]
    return s

def rc4_algorithm(data, key):
    key = [ord(c) for c in key]
    s = initialize_s_box(key)
    i = j = 0
    result = []

    for char in data:
        i = (i + 1) % 256
        j = (j + s[i]) % 256
        s[i], s[j] = s[j], s[i]
        k = s[(s[i] + s[j]) % 256]
        result.append(chr(ord(char) ^ k))

    return ''.join(result)

def adjust_key_length(key, bits):
    target_length = bits // 8
    if len(key) > target_length:
        return key[:target_length]
    elif len(key) < target_length:
        # Extend and strengthen short keys with SHA-256
        while len(key) < target_length:
            key += hashlib.sha256(key.encode()).hexdigest()
    return key[:target_length]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        operation = request.form['operation']
        key = request.form['key']
        bits = int(request.form['bit'])
        text = request.form['text']
        
        adjusted_key = adjust_key_length(key, bits)
        
        if operation == 'Encrypt':
            result = rc4_algorithm(text, adjusted_key)
        elif operation == 'Decrypt':
            result = rc4_algorithm(text, adjusted_key)
        else:
            result = "Invalid operation!"

        return render_template('index.html', result=result, operation=operation, key=key, bits=bits, text=text)
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)