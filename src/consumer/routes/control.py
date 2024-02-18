from flask import Blueprint, jsonify, render_template
from models import STATE_MACHINE

controls_bp = Blueprint('control', __name__)


@controls_bp.route('/', methods=['GET'])
def home():
    return render_template('home.html', state=STATE_MACHINE.state)


@controls_bp.route('/start', methods=['GET'])
def start():
    if STATE_MACHINE.may_start():
        STATE_MACHINE.start()
    return jsonify({'state': STATE_MACHINE.state})


@controls_bp.route('/stop', methods=['GET'])
def stop():
    if STATE_MACHINE.may_stop():
        STATE_MACHINE.stop()
    return jsonify({'state': STATE_MACHINE.state})


@controls_bp.route('/status', methods=['GET'])
def status():
    return jsonify({'state': STATE_MACHINE.state})
