from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def inicio():
    # Esta es la primera orden de FRIDAY: Mostrar el tablero
    return render_template('interfaz.html')

if __name__ == '__main__':
    app.run(debug=True)