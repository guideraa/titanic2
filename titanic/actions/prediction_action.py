import json
import os

from flask import request, flash, redirect, url_for, jsonify
from sklearn.externals import joblib

from titanic.models.model import LogisticRegressionModel


class PredictionController:
    @staticmethod
    def predict():
        json_test_data = request.get_data()
        # Convert json serialized object to a Python dictionary object
        json_dict_obj = json.loads(json_test_data)  # dict object
        # Get the serialized model
        if os.path.isfile('titanic/serialized/model.pkl'):
            lr_model = joblib.load("titanic/serialized/model.pkl")
        else:
            flash("Model not found")
            return redirect(url_for('main'))  # go to main page
        if os.path.isfile('titanic/serialized/model_columns.pkl'):
            model_columns = joblib.load('titanic/serialized/model_columns.pkl')
        else:
            flash("Model columns not found")
            return redirect(url_for('main'))  # go to main page
        lr_model_obj = LogisticRegressionModel()
        lr_model_obj.setModel(lr_model)

        list_results = lr_model_obj.predict_with_data(json_dict_obj,
                model_columns)  # ndarray [0, 1, 0, 0] this is the prediction made by the model
        # Convert ndarray to list:
        list_results_aslist = list_results.tolist()

        # MUST PREPARE THE RESULTS FROM THE MODEL TO BE PUT IN JSON FORM.  The model returns a
        # list:  [0, 1, 0, 0].  That list must be put into a json string as a dictionary.
        # Now since results is a list, we must make a dictionary with the label "result"
        result_dictionary = {"result": list_results_aslist}  # dictionary {"result": [0, 1, 0, 0]}
        # make the dictionary into a string
        return_value = json.dumps(result_dictionary)  # String form of dictionary:  '{"result": [0, 1, 0, 0]}'
        # Return the jsonify of the string which is a byte string (serialized json)
        return jsonify(return_value)  # json object b' '{"result": [0, 1, 0, 0]}''