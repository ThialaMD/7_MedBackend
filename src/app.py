"""
Exercise 07: Backend Service for Medical Data Collection.
This module provides a Flask-based REST API to manage experiments and patient data.
"""

import json
import logging
import os
from flask import request, Flask, jsonify, make_response

# First-party imports
import datastructure

app = Flask(__name__)

def load_environment():
    """
    Loads the environment configuration from a JSON file.
    Returns:
        dict: The configuration values.
    """
    try:
        env_var = os.environ['WORKING_ENV']
    except KeyError:
        # Sucht die Datei im selben Ordner wie diese app.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        env_var = os.path.join(base_dir, 'dev_env.json')

    # TASK 7: Assertion zur Absicherung der Config-Datei
    assert os.path.exists(env_var), f"Fehler: Datei {env_var} fehlt!"

    with open(env_var, 'r', encoding='utf-8') as f:
        env_values = json.loads(f.read())

    return env_values


@app.route('/', methods=['GET'])
def index():
    """Simple method to get some information about the software"""
    return json.dumps({
        'name': 'David',
        'mail': 'fhnw@roche.ch',
        'System': 'Digital Biomarker Course Project',
        'Server Component': 'v1_0_0',
        'Date': '7-Apr-2026'
    })


@app.route('/experiment', methods=['POST', 'GET'])
def experiment_action():
    """Handles creating and retrieving experiments."""
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        experiment_obj = datastructure.Experiment(name)
        ds.add_experiment(experiment_obj)
        return jsonify(experiment_obj.__dict__)

    if request.method == 'GET':
        exp_id = request.args.get('id')
        result = ds.get_experiment(exp_id)
        if result is None:
            return make_response(jsonify('experiment not found'), 404)
        return make_response(jsonify(result.__dict__), 200)
    return make_response(jsonify('Method not allowed'), 405)


@app.route('/patient', methods=['POST', 'GET'])
def patient_action():
    """Handles creating and retrieving patient records."""
    ds = datastructure.DataStorage()

    # TASK 6: Medical Audit Log
    logging.info("AUDIT: Patient endpoint accessed via %s", request.method)

    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        patient_obj = datastructure.Patient(name)
        ds.add_patient(patient_obj)
        return jsonify(patient_obj.__dict__)

    if request.method == 'GET':
        patient_id = request.args.get('id')
        result = ds.get_patient(patient_id)
        if result is None:
            return make_response(jsonify('patient not found'), 404)
        return make_response(jsonify(result.__dict__), 200)
    return make_response(jsonify('Method not allowed'), 405)


@app.route('/patients', methods=['GET'])
def patients_action():
    """Returns all registered patients."""
    ds = datastructure.DataStorage()
    return json.dumps(ds.patients, cls=datastructure.PatientEncoder)


@app.route('/experiments', methods=['GET'])
def experiments_action():
    """Returns all registered experiments."""
    ds = datastructure.DataStorage()
    return json.dumps(ds.experiments, cls=datastructure.ExperimentEncoder)


@app.route('/store', methods=['POST'])
def store_data():
    """Triggers persistent storage of collected data."""
    ds = datastructure.DataStorage()
    ds.store_data()
    return make_response(jsonify("True"), 200)


@app.route('/upload', methods=['POST'])
def upload_data():
    """Handles uploading data points for patients and experiments."""
    ds = datastructure.DataStorage()
    if request.method == 'POST':
        body = request.get_json()
        patient_id = body['patientId']
        experiment_id = body['experimentId']
        data_obj = datastructure.DataPoint(patient_id, experiment_id, body)
        ds.add_data(data_obj)
        return make_response('', 200)
    return make_response(jsonify('Method not allowed'), 405)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[
            logging.FileHandler("backendservice.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logging.debug('Starting service...')

    env_variables = load_environment()

    ds_init = datastructure.DataStorage()
    ds_init.load_data()

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)