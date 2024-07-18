import ply.lex as lex

tokens = (
    'CREAR',
    'DATABASE',
    'USAR',
    'TABLE',
    'IDENTIFICADOR',
    'INT',
    'VARCHAR',
    'NUMERO',
    'LPAREN',
    'RPAREN',
    'COMA',
    'PUNTOYCOMA'
)

# Definición de palabras clave
reserved = {
    'CREAR': 'CREAR',
    'DATABASE': 'DATABASE',
    'USAR': 'USAR',
    'TABLE': 'TABLE',
    'INT': 'INT',
    'VARCHAR': 'VARCHAR'
}

# Definición de otros tokens
t_NUMERO = r'\d+'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMA = r','
t_PUNTOYCOMA = r';'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'IDENTIFICADOR')  # upper() para coincidir con palabras clave en mayúsculas
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Test the lexer
if __name__ == "__main__":
    data = 'CREAR DATABASE prueba;'
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Token: {tok}")
