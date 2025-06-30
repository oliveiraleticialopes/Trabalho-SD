from flask import Flask, render_template, request, redirect
import paho.mqtt.client as mqtt
import threading

app = Flask(__name__)

broker = "localhost"
mensagens = []

def ao_conectar(cliente, userdata, flags, rc):
    cliente.subscribe("escola/salas/solucoes")
    cliente.subscribe("escola/salas/problemas")

def ao_receber_mensagem(cliente, userdata, mensagem):
    mensagens.append(mensagem.payload.decode())

cliente = mqtt.Client()
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber_mensagem
cliente.connect(broker, 1883, 60)

threading.Thread(target=cliente.loop_forever, daemon=True).start()

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        sala = request.form['sala']
        problema = request.form['problema']
        departamento = request.form['departamento']
        curso = request.form['curso']
        msg = f"Curso: {curso} | Depto: {departamento} | Sala {sala} - Problema: {problema}"
        cliente.publish("escola/salas/problemas", msg)
        return redirect('/')
    return render_template('index.html', mensagens=mensagens)

@app.route('/notificacoes')
def notificacoes():
    return render_template('notificacoes.html', mensagens=mensagens)

if __name__ == '__main__':
    app.run(debug=True)
