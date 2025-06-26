import paho.mqtt.client as mqtt
import threading

broker = "localhost"
topico = "escola/salas/problemas"

# Quando conecta ao broker
def ao_conectar(cliente, userdata, flags, rc):
    print("✅ Conectado ao broker MQTT")
    cliente.subscribe(topico)

# Quando recebe uma mensagem
def ao_receber_mensagem(cliente, userdata, mensagem):
    print(f"\n📢 Notificação recebida: {mensagem.payload.decode()}")
    print("------------------------------------------------")

# Função que envia problemas (roda em thread separada)
def enviar_problemas(cliente):
    while True:
        sala = input("Digite o número da sala com problema: ")
        problema = input("Descreva o problema: ")
        mensagem = f"Sala {sala} - Problema: {problema}"
        cliente.publish(topico, mensagem)

# Criação e configuração do cliente
cliente = mqtt.Client()
cliente.on_connect = ao_conectar
cliente.on_message = ao_receber_mensagem
cliente.connect(broker, 1883, 60)

# Inicia a thread de envio de problemas
threading.Thread(target=enviar_problemas, args=(cliente,), daemon=True).start()

# Inicia o loop para escutar mensagens
cliente.loop_forever()
