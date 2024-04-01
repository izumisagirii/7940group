# probes.py
from flask import jsonify


def startup_probe():
    is_ready = True
    if is_ready:
        return jsonify({'status': 'started'}), 200
    else:
        return jsonify({'status': 'starting'}), 503


def readiness_probe():
    is_database_ready = True
    is_filesystem_ready = True
    if is_database_ready and is_filesystem_ready:
        return jsonify({'status': 'ready'}), 200
    else:
        return jsonify({'status': 'not ready'}), 503


def liveness_probe():
    is_system_stable = True
    if is_system_stable:
        return jsonify({'status': 'alive'}), 200
    else:
        return jsonify({'status': 'dead'}), 503
