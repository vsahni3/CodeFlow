import cohere
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
import autofaiss



api_key = os.environ["OPENAI_API_KEY"]
co = cohere.Client(api_key)



def summarize_code(file_code: str):
    prompt = f'''
    Summarize the following code briefly.
    {file_code}
    '''
    # past_info = load_messages(email)
    # past_prompt = ''
    # for data in past_info:
    #     past_prompt += data[0] + '\n' + data[1] + '\n--'
    # training_prompt += '--' + past_prompt
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=100,
        temperature=0.8,
        stop_sequences=["--"],
        return_likelihoods='NONE',
        truncate='START')
    return response.generations[0].text.strip('-').strip('\n').strip(' ')


def find_file(summaries, question):
    list_summary = list(summaries.keys())

    combined_values = [question] + list_summary
    embeddings = np.array(co.embed(combined_values).embeddings)

    index, stats = autofaiss.build_index(embeddings)
    dist, idx = index.search(np.array([embeddings[0]]), k=3)

    return [summaries[combined_values[i]] for i in idx[0][1:]]



def reply(file, question):
    sample_file_qs = ['what file', 'which file', 'file path', 'what folder', 'which folder']
    for file_q in sample_file_qs:
        if file_q in question.lower():
            return file
    prompt = f'Use the below code to answer the question {question}\n\n'
    file_code = 'get_file_code(file)'
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=100,
        temperature=0.8,
        stop_sequences=["--"],
        return_likelihoods='NONE',
        truncate='START')
    return response.generations[0].text.strip('-').strip('\n').strip(' ')


main1_code = '''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

met_df = pd.read_csv('https://student-datasets-bucket.s3.ap-south-1.amazonaws.com/whitehat-ds-datasets/meteorite-landings/meteorite-landings.csv')

correct_years_df = met_df[(met_df['year'] >= 860) & (met_df['year'] <= 2016)]

correct_long_df = correct_years_df[(correct_years_df['reclong'] >= -180) & (correct_years_df['reclong'] <= 180)]


correct_lat_long_df = correct_long_df[~((correct_long_df['reclat'] == 0 ) & (correct_long_df['reclong'] == 0))]


row_indices = correct_lat_long_df[correct_lat_long_df['mass'].isnull() == True].index


median_mass = correct_lat_long_df['mass'].median()
correct_lat_long_df.loc[row_indices, 'mass'] = median_mass

correct_lat_long_df.loc[:, 'year'] = correct_lat_long_df.loc[:, 'year'].astype('int')
'''
main2_code = '''
import seaborn as sns
from data_cleaning import *
import matplotlib.pyplot as plt

def between_1970_2000_annotated_sns_histogram():
    plt.figure(figsize=(10,20))
    my_hist = sns.distplot(correct_lat_long_df.loc[(correct_lat_long_df['year'] >= 1970) & (correct_lat_long_df['year'] < 2001), 'year'], bins=6, kde=False)
    for i in my_hist.patches:
        my_hist.annotate(str(int(i.get_height())), xy=(i.get_x() + i.get_width() / 2, i.get_height()), ha='center', va='bottom')


def between_1970_2000_annotated_plt_histogram():
    plt.figure(figsize=(20, 20))
    my_new = plt.hist(correct_lat_long_df.loc[(correct_lat_long_df['year'] >= 1970) & (correct_lat_long_df['year'] < 2001), 'year'], bins=6)
    for i in my_new[2]:
        plt.annotate(str(int(i.get_height())), xy=(i.get_x() + i.get_width() / 2, i.get_height()), ha='center', va='bottom')
    plt.grid()

# count of each type of meterorite in decreasing order
met_class_counts = correct_lat_long_df['recclass'].value_counts()

# histograms for top 10 most frequent meteroite types
def top_10_met_type_histograms():
    for c in met_class_counts[:10].index:
        plt.figure(figsize=(20, 5))
        plt.title(c) # The 'title()' function adds a title to the graph. Here, we are providing the meteorite class as a title.
        plt.hist(correct_lat_long_df.loc[(correct_lat_long_df['recclass'] == c) & (correct_lat_long_df['year'] > 1900), 'year'], bins=50)
        plt.grid()
        plt.show()

top_10_met_type_histograms()
'''
code = {
    summarize_code(main1_code): 'src/folder1/main1.py',
    summarize_code(main2_code): 'src/folder2/main2.py'
}
print(find_file(code, 'Help me with data cleaning'))
#print(summarize_code(main2_code))

