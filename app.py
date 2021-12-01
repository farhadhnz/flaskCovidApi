import flask 
from flask import request, jsonify
from flask_cors import CORS, cross_origin

from predict import Predict

app = flask.Flask(__name__)
cors = CORS(app)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['Get'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"


@app.route('/api/v1/predict', methods=['Post'])
@cross_origin()
def api_predict():
    if (request.json):
        inputs = request.json
        country = inputs['country']
        str_index = inputs['strIndex']
        variables = inputs['variables']
        pr = Predict()
        pr.generate_csv(variables)
        prediction = pr.predict_cases(country, str_index)
        return jsonify(list(prediction))


app.run()