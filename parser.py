import ply.yacc as yacc
from lexer import tokens

def p_comando_crear_db(p):
    'comando : CREAR DATABASE IDENTIFICADOR PUNTOYCOMA'
    if not p[3].isidentifier() or not p[3][0].isalpha():
        p[0] = f"Identificador inválido '{p[3]}'"
    else:
        p[0] = ('CREAR_DATABASE', p[3])

def p_comando_usar_db(p):
    'comando : USAR DATABASE IDENTIFICADOR PUNTOYCOMA'
    if not p[3].isidentifier() or not p[3][0].isalpha():
        p[0] = f"Identificador inválido '{p[3]}'"
    else:
        p[0] = ('USAR_DATABASE', p[3])

def p_comando_crear_tabla(p):
    'comando : CREAR TABLE IDENTIFICADOR LPAREN columnas RPAREN PUNTOYCOMA'
    if not p[3].isidentifier() or not p[3][0].isalpha():
        p[0] = f"Identificador inválido '{p[3]}'"
    else:
        p[0] = ('CREAR_TABLA', p[3], p[5])

def p_columnas(p):
    'columnas : columnas COMA columna'
    p[0] = p[1] + [p[3]]

def p_columnas_una(p):
    'columnas : columna'
    p[0] = [p[1]]

def p_columna(p):
    'columna : IDENTIFICADOR tipo'
    if not p[1].isidentifier() or not p[1][0].isalpha():
        p[0] = f"Identificador de columna inválido '{p[1]}'"
    else:
        p[0] = (p[1], p[2])

def p_tipo(p):
    '''tipo : INT
            | VARCHAR LPAREN NUMERO RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = f"{p[1]}({p[3]})"

def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        print("Error de sintaxis en EOF")

parser = yacc.yacc()

# Test Parser
if __name__ == "__main__":
    data = 'CREAR DATABASE prueba;'
    result = parser.parse(data, lexer=lexer.lexer)
    print(result)
