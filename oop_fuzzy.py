import sys
from itertools import chain
from datetime import datetime 
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class TitleMatcher():

    def __init__(self,ir_file,title_file):
        self.ir_file = read_file(ir_file)
        self.title_file = read_file(title_file)


    def get_ir_columns(self):
        return list(self.ir_file)


    def get_title_columns(self):
        return list(self.title_file)

    
    def get_title_list(self, ti_colname):
        return list(self.title_file[ti_colname])


    def get_ratio(self, value, ti_colname):
        """
        Returns list of dictorionaries, including title
        and matching ratio and token sort ratio.
        """

        dict_li = []

        for ti in self.get_title_list(ti_colname):
            dict_li.append(
            {'ratio': fuzz.ratio(value, ti),
            'token_sort_ratio': fuzz.token_sort_ratio(value, ti),
            'matching_title': value,
            'original_cat_title': ti})
        
        return dict_li



# functions
def read_file(input_file):
    return pd.read_csv(input_file, sep='\t')