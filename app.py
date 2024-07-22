from flask import Flask, request, jsonify
from flask_cors import CORS
import lexer
import parser as my_parser  # Importar con alias para evitar conflicto con el módulo parser
import ply.yacc as yacc
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
CORS(app)

# Inicializar Firebase Admin SDK
cred = credentials.Certificate('credentials/compiladores-f45fd-firebase-adminsdk-b17c4-c64692aa7d.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Definir las reglas del parser
parser = yacc.yacc(module=my_parser)

@app.route('/procesar_comando', methods=['POST'])
def procesar_comando():
    data = request.json
    comando = data.get('comando', '')

    # Separar los comandos por el delimitador ';'
    comandos = [cmd.strip() + ';' for cmd in comando.split(';') if cmd.strip()]

    resultado_lexico = []
    resultado_sintactico = []
    resultado_semantico = []

    for comando in comandos:
        # Analizador léxico
        lexer.lexer.input(comando)
        lexico_resultado = []
        while True:
            tok = lexer.lexer.token()
            if not tok:
                break
            lexico_resultado.append({
                'type': tok.type,
                'value': tok.value,
                'lineno': tok.lineno,
                'lexpos': tok.lexpos
            })

        # Imprimir tokens léxicos para depuración
        print("Tokens léxicos:", lexico_resultado)

        # Analizador sintáctico y semántico
        try:
            sintactico_resultado = parser.parse(comando, lexer=lexer.lexer)
            if isinstance(sintactico_resultado, str) and sintactico_resultado.startswith("Identificador inválido"):
                semantico_resultado = 'Inválido'
            else:
                semantico_resultado = 'Válido'

                # Lógica para crear base de datos o tabla en Firebase
                if sintactico_resultado[0] == 'CREAR_DATABASE':
                    nombre_db = sintactico_resultado[1]
                    db.collection('databases').document(nombre_db).set({})
                elif sintactico_resultado[0] == 'CREAR_TABLA':
                    nombre_tabla = sintactico_resultado[1]
                    columnas = sintactico_resultado[2]
                    columnas_dict = {col[0]: col[1] for col in columnas}  # Convertir lista de tuplas a diccionario
                    db.collection('tables').document(nombre_tabla).set({
                        'columns': columnas_dict
                    })
        except Exception as e:
            sintactico_resultado = str(e)
            semantico_resultado = 'Inválido'

        # Imprimir resultado sintáctico para depuración
        print("Resultado sintáctico:", sintactico_resultado)

        resultado_lexico.append(lexico_resultado)
        resultado_sintactico.append(sintactico_resultado)
        resultado_semantico.append(semantico_resultado)

    response = {
        'lexico': resultado_lexico,
        'sintactico': resultado_sintactico,
        'semantico': resultado_semantico
    }
    return jsonify(response), 200

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
    app.run(host='0.0.0.0', port=5000, debug=True)
