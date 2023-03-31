import pandas as pd
from sklearn.metrics import classification_report
from os import listdir
from os.path import isfile, join
import re

complexity_one_files = r'^(\d{12})-(\d{6})_(l1)'
complexity_four_files = r'^(\d{12})-(\d{6})_(l4)'
complexity_seven_files = r'^(\d{12})-(\d{6})_(l7)'
all_files = r'^(\d{12})-(\d{6})_(l1|l4|l7)'


def calculate_report(list_of_files):

    pred_labels = []
    true_labels = []
    log_directory = "output/rasa_logs/"
    for item in list_of_files:
        path = log_directory + item
        df = pd.read_json(path)
        df = df.loc[(df['event'] == 'user')]
        data = list(df['parse_data'])
        for intent in data:
            pred_labels.append(intent['intent']['name'])
            true_labels.append(intent['intent']['true_label'])

    return classification_report(true_labels, pred_labels, output_dict=True)


def find_files(regex):

    selected_files = []
    onlyfiles = [f for f in listdir('output/rasa_logs') if f.endswith('.json')]
    for file in onlyfiles:
        if re.search(regex, file):
            selected_files.append(file)
    
    return selected_files


if __name__ == "__main__":
    complexity_seven_list = find_files(complexity_seven_files)
    complexity_four_list = find_files(complexity_four_files)
    complexity_one_list = find_files(complexity_one_files)
    all_complexities = find_files(all_files)



    l1_report = pd.DataFrame(calculate_report(complexity_one_list)).transpose()
    l4_report = pd.DataFrame(calculate_report(complexity_four_list)).transpose()
    l7_report = pd.DataFrame(calculate_report(complexity_seven_list)).transpose()
    overall_report = pd.DataFrame(calculate_report(all_complexities)).transpose()


    l1_report.to_csv('l1_results.csv')
    l4_report.to_csv('l4_results.csv')
    l7_report.to_csv('l7_results.csv')
    overall_report.to_csv('overall_results.csv')

