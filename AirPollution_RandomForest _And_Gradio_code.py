# -*- coding: utf-8 -*-
"""Machine Learning(RR).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1v6Rt6M2YmoDPhTk2C0aJ7EtU4VW1GBcD
"""

#importing libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_log_error
#from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
train_data = pd.read_csv('/content/drive/MyDrive/Machine Learning/train.csv')
test_data = pd.read_csv('/content/drive/MyDrive/Machine Learning/test.csv')
#op_data = pd.read_csv('sample_submission.csv')

train_data.head()

test_data.head()

#op_data.head()

train_data.info()

features = ['deg_C', 'relative_humidity', 'absolute_humidity', 'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5']
target = ['target_carbon_monoxide', 'target_benzene', 'target_nitrogen_oxides']

from google.colab import drive
drive.mount('/content/drive')

X_train, X_val, y_train, y_val = train_test_split(train_data[features], train_data[target], test_size=0.2, random_state=42)

rf_carbon_monoxide = RandomForestRegressor(n_estimators=100, random_state=42)
rf_carbon_monoxide.fit(X_train, y_train['target_carbon_monoxide'])
carbon_monoxide_preds = rf_carbon_monoxide.predict(X_val)

rf_benzene = RandomForestRegressor(n_estimators=100, random_state=42)
rf_benzene.fit(X_train, y_train['target_benzene'])
benzene_preds = rf_benzene.predict(X_val)

rf_nitrogen_oxides = RandomForestRegressor(n_estimators=100, random_state=42)
rf_nitrogen_oxides.fit(X_train, y_train['target_nitrogen_oxides'])
nitrogen_oxides_preds = rf_nitrogen_oxides.predict(X_val)

from sklearn.metrics import mean_squared_log_error

rmsle_carbon_monoxide = np.sqrt(mean_squared_log_error(y_val['target_carbon_monoxide'], carbon_monoxide_preds))
rmsle_benzene = np.sqrt(mean_squared_log_error(y_val['target_benzene'], benzene_preds))
rmsle_nitrogen_oxides = np.sqrt(mean_squared_log_error(y_val['target_nitrogen_oxides'], nitrogen_oxides_preds))
overall= rmsle_carbon_monoxide + rmsle_benzene + rmsle_nitrogen_oxides

print('RMSLE for carbon monoxide:', rmsle_carbon_monoxide)
print('RMSLE for benzene:', rmsle_benzene)
print('RMSLE for nitrogen oxides:', rmsle_nitrogen_oxides)
print("Overall: ",overall/3)
carbon_monoxide_test_preds = rf_carbon_monoxide.predict(test_data[features])
benzene_test_preds = rf_benzene.predict(test_data[features])
nitrogen_oxides_test_preds = rf_nitrogen_oxides.predict(test_data[features])

submission = pd.DataFrame({
    'date_time': test_data['date_time'],
    'target_carbon_monoxide': carbon_monoxide_test_preds,
    'target_benzene': benzene_test_preds,
    'target_nitrogen_oxides': nitrogen_oxides_test_preds
})

submission.to_csv('submission.csv', index=False)

!pip install -q gradio
import gradio as gr

def airpollution(deg_C,relative_humidity,absolute_humidity,sensor_1,sensor_2,sensor_3,sensor_4,sensor_5):
    df = pd.DataFrame.from_dict({'deg_C': [deg_C], 'relative_humidity': [relative_humidity], 'absolute_humidity': [absolute_humidity],'sensor_1':[sensor_1],'sensor_2':[sensor_2],'sensor_3':[sensor_3],'sensor_4':[sensor_4],'sensor_5':[sensor_5]})

    pred = rf_carbon_monoxide.predict(df)[0]
    pred2 = rf_benzene.predict(df)[0]
    pred3 =rf_nitrogen_oxides.predict(df)[0]
    print(pred,pred2,pred3)
    return pred,pred2,pred3


deg_C = gr.inputs.Textbox( label="deg_C")
relative_humidity= gr.inputs.Textbox(label="relative_humidity")
absolute_humidity= gr.inputs.Textbox(label="absolute_humidity")
sensor_1= gr.inputs.Textbox(label="sensor_1")
sensor_2= gr.inputs.Textbox(label="sensor_2")
sensor_3= gr.inputs.Textbox(label="sensor_3")
sensor_4= gr.inputs.Textbox(label="sensor_4")
sensor_5= gr.inputs.Textbox(label="sensor_5")
# CarbonMonoxide= gr.outputs.Textbox(label="CarbonMonoxide")
# Benzene = gr.outputs.Textbox(label="Benzene")
# NitrogenOxide = gr.outputs.Textbox(label="NitrogenOxide")
output = [gr.outputs.Textbox(label="CarbonMonoxide"),gr.outputs.Textbox(label="Benzene"), gr.outputs.Textbox(label="NitrogenOxide")]
gr.Interface(airpollution,[deg_C,relative_humidity,absolute_humidity,sensor_1,sensor_2,sensor_3,sensor_4,sensor_5],output).launch();