from flask import request, flash, redirect, session, url_for
from sklearn.externals import joblib
import os

from titanic.datamanagement.data_manager import DataManager
from titanic.models.model import LogisticRegressionModel


class SubmitController():
    """
    Handles the submits generated by the "Do Selected Actions" button in the UI. In particular it handles:
    (1) Submit when radio button 1 is active.  Action is to collect and store column names that user has selcted.
        Then clean the data.
    (2) Submit when radio button 2 is active.  Action is to retrieve dependent variable name (label) and to
        then to build and train the model.
    """
    def submit_action(self):
        radio_selected = request.form['actionradio']
        # Select columns and clean data
        if radio_selected == "1":
            self.select_columns()
            flash("Columns successfully selected")
            return
        else:
            #  Build and train model
            if radio_selected == "2":
                dependent_variable = request.form.get('dependent_var')
                session['session_dependent_variable'] = dependent_variable
                joblib.dump(dependent_variable, 'titanic/serialized/dependent_var.pkl')
                retval, model = self.build_train_model(dependent_variable)
                if retval:
                    flash("Model was successfully built and trained")
                else:
                    flash("Must do a 'Select Columns and Clean Data' first")
                return

            else:
                # This code is never executed since we use ajax to predict with datamanagement and there is no form submit
                #  Radio button 3 is never active when "Do Selected Actions" button is pressed.
                if radio_selected == "3":
                    return redirect(url_for('main')) # go to main page

    def select_columns(self):
        """
        Get a list of the user selected columns from the UI and return them. Also store the OHE version of the
        DataFrame.
        :return: A list of all columns(string) in the dataframe, a list of all column(string) to be included in model
        """
        included_columns = request.form.getlist('selected_columns') # list of str

        all_columns = session['session_all_columns'] # list of str
        data_manager = DataManager()
        data_manager.set_included_columns(included_columns)
        session['selected_columns'] = included_columns
        dataframe_ohe = data_manager.get_df_ohe()
        # Note:  we do not put a dataframe into the session.  It is much too large. Store in .pkl file
        joblib.dump(dataframe_ohe, 'titanic/serialized/df_ohe.pkl')

        return all_columns, included_columns  # Both are lists of string


    def build_train_model(self, dependent_variable):
        """
        Build and train model. Use DataFrame OHE if it is found in .pkl file.  Once the model has been trained,
        write it to a .pkl file.  If no DataFrame OHE is found, return error message.
        :param dependent_variable: string name of label column
        :return: Two values:  bool(), and LogisticRegression object that has been trained.
            If first returned object is True, second object will be LogisticRegression object.  If first returned object
            is False, second object will be a string error message.
        """
        dataframe_ohe = None
        if os.path.isfile('titanic/serialized/df_ohe.pkl'):
            dataframe_ohe = joblib.load('titanic/serialized/df_ohe.pkl') # DataFrame that is OHE
        else:
            return bool(False), "No OHE DataFrame has been created"
        lr_model_object = LogisticRegressionModel(dataframe_ohe, dependent_variable) # LogisticRegressionModel object
        lr_model, model_cols = lr_model_object.build_model() # LogisticRegression object, list of str
        # Serialize model and model columns (includes ohe columns)
        joblib.dump(lr_model, "titanic/serialized/model.pkl")
        joblib.dump(model_cols, "titanic/serialized/model_columns.pkl")
        return bool(True), lr_model # bool designating success, LogisticRegression object