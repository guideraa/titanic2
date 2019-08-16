import os
from flask import session
from sklearn.externals import joblib
from titanic.datamanagement.data_manager import DataManager


class InitApplicationManager():

    def __init__(self):
        self.all_columns = None  # a list of all the column names in the datamanagement
        self.selected_columns = None  # columns that were selected to be included in the model
        self.dependent_variable = None  # the dependent variable
        self.dependent_variable_list = list()
        self.initialize()

    def initialize(self):
        data_manager = DataManager()
        # Check if columns are in the session if so, retrieve from session.
        # If not in session, retrieve from data_manager and store in session
        if 'session_all_columns' in session:
            self.all_columns = session['session_all_columns']
        else:
            self.all_columns = data_manager.get_all_columns()
            session['session_all_columns'] = self.all_columns

        # Check if selected columns are in session and retrieve.  If not in session, retrieve from pkl storage
        if 'session_selected_columns' in session:
            self.selected_columns = session['session_selected_columns']
        else:
            if os.path.isfile('titanic/serialized/included_columns.pkl'):
                self.selected_columns = joblib.load('titanic/serialized/included_columns.pkl')
                session['selected_columns'] = self.selected_columns

        # Check if dependent variable is in session and retrieve.  If not in session, retrieve from pkl storage
        if 'session_dependent_variable' in session:
            self.dependent_variable = session['session_dependent_variable']
            self.dependent_variable_list.append(self.dependent_variable)
        else:
            if os.path.isfile('titanic/serialized/dependent_var.pkl'):
                self.dependent_variable = joblib.load('titanic/serialized/dependent_var.pkl')
                self.dependent_variable_list.append(self.dependent_variable)

    def get_all_column_names(self):
        return self.all_columns

    def get_selected_columns(self):
        return self.selected_columns

    def get_dependent_variable_list(self):
        return self.dependent_variable_list
