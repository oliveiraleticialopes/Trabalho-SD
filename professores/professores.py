import paho.mqtt.client as mqtt
import threading

broker = "localhost"
mensagens = []

cliente = mqtt.Client()

def ao_conectar(cliente, userdata, flags, rc):
    cliente.subscribe("escola/salas/problemas")
    cliente.subscribe("escola/salas/solucoes")

def ao_receber_mensagem(cliente, userdata, mensagem):
    mensagens.append(mensagem.payload.decode())

def publicar_problema(sala, descricao):
    texto = f"Sala {sala} - Problema: {descricao}"
    cliente.publish("escola/salas/problemas", texto)

def iniciar_mqtt():
    cliente.on_connect = ao_conectar
    cliente.on_message = ao_receber_mensagem
    cliente.connect(broker, 1883, 60)
    threading.Thread(target=cliente.loop_forever, daemon=True).start()
