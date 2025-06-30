from flask import Flask, render_template, request, redirect
import paho.mqtt.client as mqtt
import threading

app = Flask(__name__)

broker = "localhost"
problemas = []

def ao_conectar(cliente, userdata, flags, rc):
    cliente.subscribe("escola/salas/problemas")

def ao_receber_mensagem(cliente, userdata, mensagem):
    problema = mensagem.payload.decode()
    if problema not in problemas:
        problemas.append(problema)

cliente = mqtt.Client()
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber_mensagem
cliente.connect(broker, 1883, 60)

threading.Thread(target=cliente.loop_forever, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        departamento = request.form['departamento']
        curso = request.form['curso']
        sala = request.form['sala']
        confirmacao = f"✅ Problema resolvido - Curso: {curso}, Depto: {departamento}, Sala: {sala}"
        cliente.publish("escola/salas/solucoes", confirmacao)
        return redirect('/notificacoes')
    return render_template('index.html', problemas=problemas)

@app.route('/resolver', methods=['GET', 'POST'])
def resolver():
    if request.method == 'POST':
        sala = request.form['sala']
        departamento = request.form['departamento']
        curso = request.form['curso']
        confirmacao = f"✅ Problema resolvido - Curso: {curso}, Depto: {departamento}, Sala: {sala}"
        cliente.publish("escola/salas/solucoes", confirmacao)
        return redirect('/')
    return render_template('resolver_problema.html', problemas=problemas)

@app.route('/notificacoes')
def notificacoes():
    return render_template('notificacoes.html', problemas=problemas)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
