import pandas as pd
from sklearn.linear_model import LogisticRegression


class LogisticRegressionModel():

    def __init__(self, data_frame = None, dependent_variable = None):
        """

        :param data_frame: pandas DataFrame that contains the training data
        :param dependent_variable: data column name of the label
        :param model_columns: data column names of the features
        """
        self.lr_model = LogisticRegression()
        self.data_frame = data_frame
        self.dependent_variable = dependent_variable

    def build_model(self):
        """
            Builds a LogisticRegression model using values that are data members of this class.
            The data members used are data_frame which is a training pandas DataFrame that has been OHE,
            dependent_variable which is a string representing the model's label.
        :return: sklearn.linear_model.LogisticRegression object, list of string which is a list of
                the feature columns
        """
        # Get all the columns that are not the dependent_variable
        x = self.data_frame[self.data_frame.columns.difference([self.dependent_variable])]
        y = self.data_frame[self.dependent_variable]
        self.lr_model.fit(x, y)
        model_columns = list(x.columns)
        return self.lr_model, model_columns

    def predict_with_data(self, json_test_data, model_columns):
        """
        :param model_columns: list of str
        :param json_test_data: dictionary
        :return: prediction values ( 0 or 1 )
        :rtype: ndarray
        """
        # Convert the json data (dictionary) into a pandas DataFrame
        test_dataframe = pd.DataFrame(json_test_data)  # DataFrame
        # OHE the category columns in the test data
        ohe_dataframe = pd.get_dummies(test_dataframe) # DataFrame
        # Make sure that all the columns in the model are included in the test data.
        query = ohe_dataframe.reindex(columns=model_columns, fill_value=0)
        prediction = self.lr_model.predict(query)  # ndarray, not list

        return prediction

    def getModel(self):
        return self.lr_model

    def setModel(self,lr_model):
        self.lr_model = lr_model

