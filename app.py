from flask import Flask, request, jsonify
from azure.messaging.webpubsubservice import WebPubSubServiceClient

app = Flask(__name__)


# prevent cors error
@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST")
    return response


connection_string = "<connection-string>"
hub_name = "Hub"

# Inicializa el cliente de Azure Web PubSub
client = WebPubSubServiceClient.from_connection_string(
    connection_string=connection_string, hub=hub_name
)


# Ruta para generar una URL de conexión para los usuarios del chat
@app.route("/negotiate", methods=["GET"])
def negotiate():
    user_id = request.args.get("user")
    url = client.get_client_access_token(client_protocol="Default", user_id=user_id)
    return jsonify({"url": url["url"]})


# Ruta para recibir y enviar mensajes entre los usuarios
@app.route("/send", methods=["POST"])
def send_message():
    message_data = request.get_json()
    from_user = message_data["from"]
    to_user = message_data["to"]
    message = message_data["message"]

    # Envía el mensaje solo al destinatario específico
    client.send_to_user(user_id=to_user, message=message, content_type="text/plain")
    return jsonify({"status": "Message sent"})


if __name__ == "__main__":
    app.run(debug=True)
