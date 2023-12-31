from flask import Blueprint, jsonify, render_template
from models.ConsumerState import CONSUMER_STATE, States

controls_bp = Blueprint('control', __name__)


@controls_bp.route('/start', methods=['GET'])
def start():
    # global CONSUMER_STATE
    if CONSUMER_STATE.state != States.stopped:
        return jsonify({'state': CONSUMER_STATE.state.name})

    CONSUMER_STATE.state = States.running
    return jsonify({'state': CONSUMER_STATE.state.name})


@controls_bp.route('/stop', methods=['GET'])
def stop():
    if CONSUMER_STATE.state != States.running:
        return jsonify({'state': CONSUMER_STATE.state.name})

    CONSUMER_STATE.state = States.stopped
    return jsonify({'state': CONSUMER_STATE.state.name})


@controls_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'state': CONSUMER_STATE.state.name})


@controls_bp.route('/', methods=['GET'])
def home():
    return render_template('home.html', state=CONSUMER_STATE.state.name)
