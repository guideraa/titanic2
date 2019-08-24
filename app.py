from flask import Flask, render_template, url_for, redirect

from titanic.actions.application_initialize import InitApplicationManager
from titanic.actions.prediction_action import PredictionController
from titanic.actions.submit_actions import SubmitController

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
    """
    Note there is no call to render_template() or redirect() because /prediction is an asynchronous call to the server
    where client side javascript captures this return value and builds HTML that is rendered on the client's web page.
    :return: # json serialized object.  For example:   b' '{"result": [0, 1, 0, 0]}''
    """
    return PredictionController.predict()


if __name__ == '__main__':
    """
    In order to run this app from the command line:
     1)  cd to the directory where app.py is located
     2) Execute the command:  python app.py
    """

    app.secret_key = 'prunknurp'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(port=5001, debug=True)