import paho.mqtt.client as mqtt
import threading

broker = "localhost"
problemas_recebidos = []

cliente = mqtt.Client(protocol=mqtt.MQTTv311)

def ao_conectar(cliente, userdata, flags, rc):
    cliente.subscribe("escola/salas/problemas")

def ao_receber_mensagem(cliente, userdata, mensagem):
    problema = mensagem.payload.decode()
    if problema not in problemas_recebidos:
        problemas_recebidos.append(problema)

def publicar_solucao(sala):
    texto = f"✅ Problema resolvido na sala {sala}."
    cliente.publish("escola/salas/solucoes", texto)

def iniciar_mqtt():
    cliente.on_connect = ao_conectar
    cliente.on_message = ao_receber_mensagem
    cliente.connect(broker, 1883, 60)
    threading.Thread(target=cliente.loop_forever, daemon=True).start()
