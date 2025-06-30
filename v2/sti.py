import paho.mqtt.client as mqtt
import threading

broker = "localhost"

def ao_conectar(cliente, userdata, flags, rc):
    print("✅ STI conectado ao broker")
    cliente.subscribe("escola/salas/problemas")

def ao_receber_mensagem(cliente, userdata, mensagem):
    print(f"\n📥 Novo problema recebido: {mensagem.payload.decode()}")
    sala = input("Digite a sala resolvida (ou pressione Enter para ignorar): ")
    if sala:
        confirmacao = f"✅ Problema resolvido na sala {sala}."
        cliente.publish("escola/salas/solucoes", confirmacao)

cliente = mqtt.Client()
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber_mensagem
cliente.connect(broker, 1883, 60)
cliente.loop_forever()
