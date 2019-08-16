import os

from flask import Flask, request, jsonify, render_template, url_for, redirect, session, json, flash
from sklearn.externals import joblib

from titanic.actions.application_initialize import InitApplicationManager
from titanic.actions.submit_actions import SubmitController
from titanic.models.model import LogisticRegressionModel

# Your API definition
app = Flask(__name__)


@app.route('/')
def main():
    """Entry point; the view for the main page"""
    # Get stored values to load into ui
    controller_manager = InitApplicationManager()
    all_columns = controller_manager.get_all_column_names()
    selected_columns = controller_manager.get_selected_columns()
    dependent_variable_list = controller_manager.get_dependent_variable_list()

    return render_template('main.html', all_columns_option_list=all_columns,
            selected_columns_option_list=selected_columns, dependent_var_option = dependent_variable_list )


@app.route('/action_controller', methods=['GET','POST'])
def action_controller():
    """This url responds to the 'Do Selected Action' button.
        There are two kinds of action that this button initiates depending on which radio button is active when the
        action button is pressed.  The SubmitController() class determines which radio button is active and activates
        the appropriate methods to carry out the action.

        Notice that this function returns a redirect() to the URL that is associated with the function main().
        This redirect has the effect that the main page is refreshed with the appropriate page components displayed.
    """
    controller = SubmitController()
    controller.submit_action()
    return redirect(url_for('main'))  # go to main page



@app.route('/prediction', methods=['GET','POST'])
def prediction():
    # This function is called from an asynchronous request made by the "Do Action" button in the main page.
    # Get data in the request.  This data is a serialized form of the json that was passed in the request.
    # NOTE:  Serialized json data is a byte string with no structure
    # Notice that this function does not do a redirect() or a render_template() call.  The data that this function
    # returns is returned to and used by javascript to put the results into HTML and to render that HTML into
    # a specific UI <div> where it is displayed.
    json_test_data = request.get_data()
    print("Serialized json object: {}".format( json_test_data))
    # Convert json serialized object to a Python dictionary object
    json_dict_obj = json.loads(json_test_data)  # dict object
    # Get the serialized model
    lr_model = None
    model_columns = None
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

    list_results = lr_model_obj.predict_with_data(json_dict_obj, model_columns) # ndarray [0, 1, 0, 0] this is the prediction made by the model
    # Convert ndarray to list:
    list_results_aslist = list_results.tolist()

    # MUST PREPARE THE RESULTS FROM THE MODEL TO BE PUT IN JSON FORM.  The model returns a
    # list:  [0, 1, 0, 0].  That list must be put into a json string as a dictionary.
    # Now since results is a list, we must make a dictionary with the label "result"
    result_dictionary = {"result": list_results_aslist} # dictionary {"result": [0, 1, 0, 0]}
    # make the dictionary into a string
    return_value = json.dumps(result_dictionary) # String form of dictionary:  '{"result": [0, 1, 0, 0]}'
    # Return the jsonify of the string which is a byte string (serialized json)
    return jsonify(return_value) # json object b' '{"result": [0, 1, 0, 0]}''


if __name__ == '__main__':
    """
    In order to run this app from the command line:
     1)  cd to the directory where app.py is located
     2) Execute the command:  python app.py
    """
    print ("starting app........")

    app.secret_key = 'prunknurp'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(port=5001, debug=True)