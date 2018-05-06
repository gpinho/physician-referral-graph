import pandas as pd
import numpy as np

def combine_referral_datasets(left_filepath, left_year, list_right_filepath_year, usecols=['Initial Physician NPI', 'Secondary Physician NPI', 'Number Unique Beneficiaries'], dtype={'Initial Physician NPI':str, 'Secondary Physician NPI':str, 'Number Unique Beneficiaries':np.int32}, index_col=['Initial Physician NPI', 'Secondary Physician NPI']):
    print('function starting')
    left_df = pd.read_csv(left_filepath, usecols=usecols, dtype=dtype, index_col=index_col)
    left_df.columns += '_' + left_year
    print(f'year {left_year} loaded')
    for right_file in list_right_filepath_year:
        right_filepath, right_year = right_file
        right_df = pd.read_csv(right_filepath, usecols=usecols, dtype=dtype, index_col=index_col)
        print(f'year {right_year} loaded')
        right_df.columns += '_' + right_year
        left_df = left_df.merge(right_df, how='outer', left_index= True, right_index=True, copy=False)
        print(f'year {right_year} merged')
        left_df.to_csv('physician-shared-patient-patterns-' + left_year + '-' + right_year + '.csv')
        print('dataframe saved to csv')
    return left_df

if __name__ == '__main__':
    
    # feature engineer referral dataset
    initial_referral_dataset = 'https://s3-us-west-1.amazonaws.com/physician-referral-graph/physician-shared-patient-patterns-2009-days180_withHeader.csv'
    initial_referral_year = '2009'
    other_referral_datasets_years = [('https://s3-us-west-1.amazonaws.com/physician-referral-graph/physician-shared-patient-patterns-2010-days180_withHeader.csv', '2010'), ('https://s3-us-west-1.amazonaws.com/physician-referral-graph/physician-shared-patient-patterns-2011-days180_withHeader.csv', '2011'), ('https://s3-us-west-1.amazonaws.com/physician-referral-graph/physician-shared-patient-patterns-2012-days180_withHeader.csv', '2012'), ('https://s3-us-west-1.amazonaws.com/physician-referral-graph/physician-shared-patient-patterns-2013-days180_withHeader.csv', '2013'), ('https://s3-us-west-1.amazonaws.com/physician-referral-graph/physician-shared-patient-patterns-2014-days180_withHeader.csv', '2014'), ('https://s3-us-west-1.amazonaws.com/physician-referral-graph/physician-shared-patient-patterns-2015-days180_withHeader.csv', '2015')]    
    referral_df = combine_referral_datasets(initial_referral_dataset, initial_referral_year, other_referral_datasets_years)
    referral_df.to_csv('physician-shared-patient-patterns-2009-2015-days180_withHeader.csv')
    save_files_to_s3(['physician-shared-patient-patterns-2009-2015-days180_withHeader.csv'], 'physician-referral-graph')
