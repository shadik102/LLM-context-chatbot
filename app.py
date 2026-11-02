
from flask import Flask, render_template, request, jsonify
from chatbot import (
    create_conversation,
    send_message,
    get_conversation_history
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/new-chat", methods=["POST"])
def new_chat():
    try:
        conversation_id = create_conversation()
        return jsonify({
            "conversation_id": conversation_id,
            "success": True
        })
    except Exception as error:
        app.logger.exception("New chat error")
        return jsonify({"error": str(error)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}

        conversation_id = data.get("conversation_id")
        message = data.get("message")

        if not conversation_id:
            return jsonify({
                "error": "Conversation ID is missing. Please start a new chat."
            }), 400

        if not message or not str(message).strip():
            return jsonify({"error": "Please enter a message."}), 400

        answer = send_message(conversation_id, str(message))

        return jsonify({
            "success": True,
            "answer": answer,
            "response": answer,
            "reply": answer
        })

    except Exception as error:
        app.logger.exception("Chat API error")
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/api/history/<conversation_id>", methods=["GET"])
def history(conversation_id):
    try:
        messages = get_conversation_history(conversation_id)
        return jsonify({
            "success": True,
            "history": messages
        })
    except Exception as error:
        app.logger.exception("History error")
        return jsonify({"error": str(error)}), 404


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
