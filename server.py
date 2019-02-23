from flask import Flask, request, jsonify
import predictions
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def delete_empty_messages(messages):
  filtered_messages = {}
  for key, message in messages.items():
    if message.strip():
      filtered_messages[key] = message
  return filtered_messages

@app.route('/api', methods=['POST'])
def predict():
  messages = request.get_json(force=True)
  messages = delete_empty_messages(messages)
  keys = list(messages.keys())
  values = [messages[key] for key in keys]
  if values:
    toxicity = predictions.predict(values)
    toxic_messages = {keys[index]: float(toxic) for index, toxic in enumerate(toxicity)}
    return jsonify(toxic_messages)
  else:
    return jsonify([])

if __name__ == '__main__':
  predictions.init()
  app.run(port=5000, debug=True)
