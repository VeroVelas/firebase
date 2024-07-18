from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    ip = data.get('ip')
    password = data.get('password')

    # Aquí puedes agregar la lógica para verificar el IP y la contraseña
    # Por ahora, solo vamos a simular una respuesta exitosa

    if ip == "192.168.10.56" and password == "password_correcto":
        return jsonify({"message": "Login exitoso"}), 200
    else:
        return jsonify({"error": "IP o contraseña incorrecta"}), 400

if __name__ == '__main__':
    app.run(debug=True)
