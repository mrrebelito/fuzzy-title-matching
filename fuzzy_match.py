import sys, os
from itertools import chain
from datetime import datetime 
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


"""
Fuzzy match titles from two title lists.

Use Python Fuzzywuzzy library. 

Field names are hard coded into script. 
"""


def get_ratio(value,title_list):
    """
    returns list of dictionaries. Including the title and
    matching ratio
    """
    dict_li = []

    for item in title_list:
        dict_li.append(
        {'ratio': fuzz.ratio(value, item),
        'token_sort_ratio': fuzz.token_sort_ratio(value, item),
        'matching_title': value,
        'original_cat_title': item})

    return dict_li

def get_ratio_matches(row,num_val):
    """returns matches that are greater than input num_val arg """

    return [x for x in row if x['ratio'] >= num_val]

def get_token_sort_matches(row, num_val):

    return [x for x in row if x['token_sort_ratio'] >= num_val]


def create_matches_dataframe(df, row_name):
    """
    create new dateframe for titles that match 

    pass dataframe that includes a 'matching column' to
    create a new dataframe.
    """

    df = df.loc[df[
        row_name].str.len() > 0, :]

    return pd.DataFrame(
        list(
        chain.from_iterable(df[row_name]
        .to_list()
        )))


def main(mods_input, ti_input, match_val, output_f):


    mods_df = pd.read_csv(mods_input, sep='\t')
    ti_df = pd.read_csv(ti_input, sep='|')

    ti_df = ti_df[['short_title', 'full_title', 'location_count']] 
    ti_df = ti_df.dropna(subset=['short_title']) 

    # create python list object title list
    ti_list = list(ti_df['short_title'])

    # remove null title
    mods_df = mods_df[mods_df['mods.title'].notnull()]

    # create new columns
    mods_df['title_match'] = mods_df['mods.title'].apply(
        get_ratio,
        args=(ti_list,))


    create matches column
    mods_df['title_ratio'] = mods_df['title_match'].apply(
        get_ratio_matches,
        args=(match_val,)
    )

    # create matches column
    mods_df['title_token_sort'] = mods_df['title_match'].apply(
        get_ratio_matches,
        args=(match_val,)
    )

    match_mods_df = create_matches_dataframe(mods_df, 'title_ratio')
    merge_mods_df = match_mods_df.merge(
        mods_df[['mods.title','PID',
        'mods.type_of_resource',
        'mods.sm_digital_object_identifier']],
        left_on='matching_title',
        right_on='mods.title')

    # merge merge_mods_df with original title df
    merge_ti_df = merge_mods_df.merge(ti_df,
        left_on=['original_cat_title'],
        right_on='short_title')

    # # output file
    merge_ti_df.to_excel(output_f,index=False)


if __name__ == "__main__":
    
    internet_p = os.path.join('internet','matching_titles_%m-%d-%Y.xlsx')
    output_f = datetime.now().strftime(internet_p)

    mods_input = sys.argv[1] # MODs metadata list
    ti_input = sys.argv[2] # title input list
    match_val = int(sys.argv[3]) # match value. Adjust as needed.
    main(mods_input, ti_input ,match_val, output_f)