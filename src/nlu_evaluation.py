import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from os import listdir
from os.path import isfile, join
import re

complexity_one_files = r'^(\d{12})-(\d{6})_(l1)'
complexity_four_files = r'^(\d{12})-(\d{6})_(l4)'
complexity_seven_files = r'^(\d{12})-(\d{6})_(l7)'
all_files = r'^(\d{12})-(\d{6})_(l1|l4|l7)'


def get_labels(list_of_files):
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

    return true_labels, pred_labels


def get_unique_labels(y_true, y_pred):

    list_of_labels = []
    for label in y_true:
        if label not in list_of_labels:
            list_of_labels.append(label)
    
    for label in y_pred:
        if label not in list_of_labels:
            list_of_labels.append(label)
    
    return list_of_labels


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
    
    l1_true, l1_pred = get_labels(complexity_one_list)
    l4_true, l4_pred = get_labels(complexity_four_list)
    l7_true, l7_pred = get_labels(complexity_seven_list)
    overall_true, overall_pred = get_labels(all_complexities)

    all_labels = get_unique_labels(overall_true, overall_pred)
    print(all_labels)

    confusion_df = pd.DataFrame(confusion_matrix(overall_true, overall_pred, labels=all_labels))

    l1_report = pd.DataFrame(classification_report(l1_true, l1_pred, output_dict=True)).transpose()
    l4_report = pd.DataFrame(classification_report(l4_true, l4_pred, output_dict=True)).transpose()
    l7_report = pd.DataFrame(classification_report(l7_true, l7_pred, output_dict=True)).transpose()
    overall_report = pd.DataFrame(classification_report(overall_true, overall_pred, output_dict=True)).transpose()


    l1_report.to_csv('l1_results.csv')
    l4_report.to_csv('l4_results.csv')
    l7_report.to_csv('l7_results.csv')
    overall_report.to_csv('overall_results.csv')
    confusion_df.to_csv('confusion_matrix.csv')

