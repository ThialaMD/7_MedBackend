import json
from flask import request, Flask, jsonify, make_response

import datastructure
import idgenerator

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return json.dumps({'name' : 'David',
  'mail' : 'david.herzig@roche.com',
  'System' : 'Digital Biomarker Course Project',
  'Server Component' : 'v1_0_0',
  'Date' : '7-Apr-2025'})

@app.route('/experiment', methods=['POST', 'GET'])
def experiment_action():
  ds = datastructure.DataStorage()
  if request.method == 'POST':
    body = request.get_json()
    name = body['name']
    experiment_obj = datastructure.Experiment(name)
    ds.add_experiment(experiment_obj)
    return jsonify(experiment_obj.__dict__)
  if request.method == 'GET':
    id = request.args.get('id')
    result = ds.get_experiment(id)
    if result == None:
      return make_response(jsonify('experiment not found'), 404)
    else:
      return make_response(jsonify(result.__dict__), 200)
  
@app.route('/patient', methods=['POST', 'GET'])
def patient_action():
  ds = datastructure.DataStorage()
  if request.method == 'POST':
    body = request.get_json()
    name = body['name']
    patient_obj = datastructure.Patient(name)
    ds.add_patient(patient_obj)
    return jsonify(patient_obj.__dict__)
  if request.method == 'GET':
    id = request.args.get('id')
    result = ds.get_patient(id)
    if result == None:
      return make_response(jsonify('patient not found'), 404)
    else:
      return make_response(jsonify(result.__dict__), 200)

@app.route('/patients', methods=['GET'])
def patients_action():
  ds = datastructure.DataStorage()
  return json.dumps(ds.patients, cls=datastructure.PatientEncoder)
  
@app.route('/experiments', methods=['GET'])
def experiments_action():
  ds = datastructure.DataStorage()
  return json.dumps(ds.experiments, cls=datastructure.ExperimentEncoder)
  
@app.route('/store', methods=['POST'])
def store_data():
  ds = datastructure.DataStorage()
  ds.store_data()
  return make_response(jsonify("True"), 200)
  
@app.route('/upload', methods=['POST'])
def upload_data():
  ds = datastructure.DataStorage()
  if request.method == 'POST':
    body = request.get_json()
    patient_id = body['patient_id']
    experiment_id = body['experiment_id']
    data = body['data']
    data_obj = datastructure.DataPoint(patient_id, experiment_id, data)
    ds.add_data(data_obj)
    return make_response('', 200)
  
if __name__ == '__main__':
  print('Starting service...')
  
  # check if there are data files for patients and experiments available
  ds = datastructure.DataStorage()
  ds.load_data()
  
  app.run(host='0.0.0.0', debug=True)