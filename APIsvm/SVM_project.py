import numpy as np
import pandas as pd

import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler

df = pd.DataFrame(columns=['XP', 'VP', 'XQ', 'VQ', 'XR', 'VR', 'XT', 'VT', 'XSR', 'XTS', 'XPT', 'XQP'])
M = ['A', 'L', 'N', 'R', 'V']
predict_result = {}
unresolved_classes = []


def main_function(file_path):
    global df
    text_file = open(file_path, "r")
    data = text_file.read().splitlines()
    text_file.close()

    data = data[5:]  # data body
    data = np.asarray(data, dtype=np.float)  # read data as float
    df = pd.DataFrame(columns=['XP', 'VP', 'XQ', 'VQ', 'XR', 'VR', 'XT', 'VT', 'XSR', 'XTS', 'XPT', 'XQP'])
    a_features_detector(data)
    l_features_detector(data)
    n_features_detector(data)
    r_features_detector(data)
    v_features_detector(data)

    classifier = joblib.load('rbf_2000_SVM_model2')

    for i in range(0, df.shape[0]):
        pred = classifier.predict_proba(df.iloc[[i]])[0] * 100
        prob_per_class_dict = dict(zip(classifier.classes_, pred))
        predict_result[M[i]] = prob_per_class_dict[M[i]]
    for key, value in predict_result.items():
        predict_result[key] = round(value, 2)

    for m in unresolved_classes:
        predict_result[m] = 0.0
    return predict_result


def n_features_detector(lines):
    try:
        global R_index
        global df
        R = np.amax(lines)
        R_index = np.where(lines == R)[0][0]

        f_part = lines[:R_index]
        l_part = lines[R_index:]

        P = np.amax(f_part[:-15])
        P_index = np.where(f_part[:-15] == P)[0][0]
        Q = np.amin(f_part[-10:])
        Q_index = np.where(f_part[-10:] == Q)[0][0] + len(f_part[:-10])
        S = np.amin(l_part[:10])
        S_index = np.where(l_part[:10] == S)[0][0] + len(f_part)
        T = np.amax(l_part[5:])
        T_index = np.where(l_part[5:] == T)[0][0] + 5 + len(f_part)

        data = {
            'XP': [P_index], 'VP': [P], 'XQ': [Q_index], 'VQ': [Q], 'XR': [R_index], 'VR': [R], 'XT': [T_index],
            'VT': [T],
            'XSR': [R_index - S_index], 'XTS': [T_index - S_index], 'XPT': [T_index - P_index],
            'XQP': [Q_index - P_index]
        }
        df1 = pd.DataFrame(data=data)
        # df1 = df1.loc[:, df1.columns].values
        # print('df1', df1)
        # df2 = StandardScaler().fit_transform(df1)
        # print('df2', df2)
        # df2 = pd.DataFrame(df2, columns=df1.columns)
        # print('df2', df2)
        df = df.append(df1, ignore_index=True)
        # print('df1', df)
    except:
        print('error occur with N features extraction')
        unresolved_classes.append('N')


def r_features_detector(lines):
    try:
        global R_index
        global df
        R = np.amin(lines)
        R_index = np.where(lines == R)[0][0]

        f_part = lines[:R_index]
        l_part = lines[R_index:]

        P = 0
        P_index = 0
        Q = np.amax(f_part[-20:])
        Q_index = np.where(f_part[-20:] == Q)[0][0] + len(f_part[:-20])
        S = np.amax(l_part[:20])
        S_index = np.where(l_part[:20] == S)[0][0] + len(f_part)
        T = np.amin(l_part)
        T_index = np.where(l_part == T)[0][0] + len(f_part)

        data = {
            'XP': [P_index], 'VP': [P], 'XQ': [Q_index], 'VQ': [Q], 'XR': [R_index], 'VR': [R], 'XT': [T_index],
            'VT': [T],
            'XSR': [R_index - S_index], 'XTS': [T_index - S_index], 'XPT': [T_index - P_index],
            'XQP': [Q_index - P_index]
        }
        df1 = pd.DataFrame(data=data)
        # df2 = StandardScaler().fit_transform(df1)
        # df2 = pd.DataFrame(df2, columns=df1.columns)
        df = df.append(df1, ignore_index=True)
    except:
        print('error occur with R features extraction')
        unresolved_classes.append('R')


def a_features_detector(lines):
    try:
        global R_index
        global df
        R = np.amax(lines)
        R_index = np.where(lines == R)[0][0]
        f_part = lines[:R_index]
        l_part = lines[R_index:]

        P = np.amax(f_part[:-10])
        P_index = np.where(f_part[:-10] == P)[0][0]
        Q = np.amin(f_part[-10:])
        Q_index = np.where(f_part[-10:] == Q)[0][0] + len(f_part[:-10])
        S = np.amin(l_part[:10])
        S_index = np.where(l_part[:10] == S)[0][0] + len(f_part)
        T = np.amax(l_part[5:])
        T_index = np.where(l_part[5:] == T)[0][0] + 5 + len(f_part)

        data = {
            'XP': [P_index], 'VP': [P], 'XQ': [Q_index], 'VQ': [Q], 'XR': [R_index], 'VR': [R], 'XT': [T_index],
            'VT': [T],
            'XSR': [R_index - S_index], 'XTS': [T_index - S_index], 'XPT': [T_index - P_index],
            'XQP': [Q_index - P_index]
        }
        df1 = pd.DataFrame(data=data)
        # df2 = StandardScaler().fit_transform(df1)
        # df2 = pd.DataFrame(df2, columns=df1.columns)
        df = df.append(df1, ignore_index=True)
    except:
        print('error occur with A features extraction')
        unresolved_classes.append('A')


def l_features_detector(lines):
    try:
        global R_index
        global df
        R = np.amin(lines)
        R_index = np.where(lines == R)[0][0]

        f_part = lines[:R_index]
        l_part = lines[R_index:]

        Q = np.amax(f_part[-20:])
        Q_index = np.where(f_part[-20:] == Q)[0][0] + len(f_part[:-20])
        P = np.amin(f_part[:Q_index])
        P_index = np.where(f_part == P)[0][0]
        T = np.amax(l_part)
        T_index = np.where(l_part == T)[0][0] + len(f_part)
        S = derivative(l_part[10:T_index])
        S_index = np.where(l_part[10:T_index] == S)[0][0] + len(f_part)

        data = {
            'XP': [P_index], 'VP': [P], 'XQ': [Q_index], 'VQ': [Q], 'XR': [R_index], 'VR': [R], 'XT': [T_index],
            'VT': [T],
            'XSR': [R_index - S_index], 'XTS': [T_index - S_index], 'XPT': [T_index - P_index],
            'XQP': [Q_index - P_index]
        }
        df1 = pd.DataFrame(data=data)
        # df2 = StandardScaler().fit_transform(df1)
        # df2 = pd.DataFrame(df2, columns=df1.columns)
        df = df.append(df1, ignore_index=True)
    except:
        print('error occur with L features extraction')
        unresolved_classes.append('L')


def v_features_detector(lines):
    try:
        global R_index
        global df
        R = np.amax(lines)
        R_index = np.where(lines == R)[0][0]

        f_part = lines[:R_index]
        l_part = lines[R_index:]

        P = np.amax(f_part[:-20])
        P_index = np.where(f_part == P)[0][0]
        Q = np.amin(f_part)
        Q_index = np.where(f_part == Q)[0][0]
        S = np.amin(l_part[:30])
        S_index = np.where(l_part[:30] == S)[0][0] + len(f_part)
        T = np.amax(l_part[30:])
        T_index = np.where(l_part[30:] == T)[0][0] + 30 + len(f_part)

        data = {
            'XP': [P_index], 'VP': [P], 'XQ': [Q_index], 'VQ': [Q], 'XR': [R_index], 'VR': [R], 'XT': [T_index],
            'VT': [T],
            'XSR': [R_index - S_index], 'XTS': [T_index - S_index], 'XPT': [T_index - P_index],
            'XQP': [Q_index - P_index]
        }
        df1 = pd.DataFrame(data=data)
        # df2 = StandardScaler().fit_transform(df1)
        # df2 = pd.DataFrame(df2, columns=df1.columns)
        df = df.append(df1, ignore_index=True)
        unresolved_classes.append('H')
    except:
        print('error occur with V features extraction')
        unresolved_classes.append('V')


def derivative(data):
    for i in range(3, len(data) - 1):
        y = (data[i] - data[i - 3]) / 2
        if y < 0:
            break
    return data[i]
