import os, sys
from flask import Flask, request, jsonify, render_template_string
from src.core.watchdog import verify_vault, update_manifest
from src.core.retrieval_engine import LocalRetrievalEngine
from src.core.memory_engine import MemoryEngine
from brain import get_ripple_payload

app = Flask(__name__)

@app.before_request
def guard():
    if not verify_vault():
        return jsonify({"error": "Integrity violation"}), 403

retriever = LocalRetrievalEngine()

@app.route('/ripple', methods=['POST'])
def ripple():
    data = request.get_json(force=True)
    return jsonify(get_ripple_payload(data.get("text", "")))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
