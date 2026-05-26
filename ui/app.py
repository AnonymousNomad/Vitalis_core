from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.insert(0, os.path.expanduser("~/vitalis_core"))
from core.brain import VitalisBrain
from core.talker import VitalisTalker

app = Flask(__name__)
brain = VitalisBrain()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    tier = data.get('tier', 'basic')
    user_input = data.get('input', '')
    talker = VitalisTalker(tier)
    response = brain.process(user_input)
    return jsonify({
        'response': response,
        'tier': tier
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
