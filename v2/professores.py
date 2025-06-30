import paho.mqtt.client as mqtt
import threading

broker = "localhost"

def ao_conectar(cliente, userdata, flags, rc):
    print("✅ Conectado ao broker MQTT")
    cliente.subscribe("escola/salas/problemas")
    cliente.subscribe("escola/salas/solucoes")

def ao_receber_mensagem(cliente, userdata, mensagem):
    print(f"\n📢 Notificação: {mensagem.payload.decode()}")
    print("--------------------------------------------")

def enviar_problema(cliente):
    while True:
        sala = input("Digite o número da sala com problema: ")
        problema = input("Descreva o problema técnico: ")
        mensagem = f"Sala {sala} - Problema: {problema}"
        cliente.publish("escola/salas/problemas", mensagem)

cliente = mqtt.Client()
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber_mensagem
cliente.connect(broker, 1883, 60)

threading.Thread(target=enviar_problema, args=(cliente,), daemon=True).start()
cliente.loop_forever()
