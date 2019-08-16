import pandas as pd
import csv
from sklearn.externals import joblib


class DataManager():
    """
    This class manages the data.  It reads the original data specified in the data_url parameter of the constructor.
    It keeps track of the column names that will be included as model features.  The method get_df_ohe() uses
    the cols_to_include and produces a pandas DataFrame that has been one hot encoded.
    """
    def __init__(self, data_url = "titanic/external_data/titanic2data.csv"):
        """
        Sets the data member data_url to the specified url passed as a parameter.
        :param data_url: URL of the data source
        """
        # self.all_columns = all_columns
        self.cols_to_include = None
        self.data_url = data_url

    def get_df_ohe(self):
        """
        Read the data from the URL source and create a pandas DataFrame.  Then retrieve the feature column names and
        create and store a one hot encoded DataFrame in a .pkl file
        :return: pandas.DataFrame that has been one hot encoded.
        """
        # These are the category columns that need to be converted into numeric values
        # They will eventually be converted to numeric values by One Hot Encoding (pd.get_dummies())
        categoricals = []
        data_frame = pd.read_csv(self.data_url)
        df_included_cols = data_frame[self.cols_to_include]
        # This loop accomplishes two things:  (1) Collect the categorical columns, (2) Replace NaNs with 0
        for col, col_type in df_included_cols.dtypes.iteritems():
            if col_type == 'O':
                categoricals.append(col)
            else:
                df_included_cols[col].fillna(0, inplace=True)
        # DataFrame with One Hot Encoding
        df_ohe: pd.DataFrame = pd.get_dummies(df_included_cols, columns=categoricals, dummy_na=True)
        joblib.dump(df_ohe, 'titanic/serialized/df_ohe.pkl')
        return df_ohe

    def get_all_columns(self):
        """
        Get a list of all the columns in the original data
        :return: list of string representing all column names in the data
        """
        with open(self.data_url, "rt") as csv_file:
            reader = csv.reader(csv_file)
            all_columns = next(reader)
        return all_columns

    def set_included_columns(self, json_columns):
        """
        Get a list of all the selected columns (features) that will be used in the model
        :param json_columns:
        :return: list of string representing all the column names to be included in the model.
        """
        self.cols_to_include = json_columns
        joblib.dump(json_columns, 'titanic/serialized/included_columns.pkl')
