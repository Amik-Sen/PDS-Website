import pandas as pd
import numpy as np
import glob
import urllib.request
import json
import tensorflow as tf
import matplotlib.pyplot as plt
import datetime
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.callbacks import EarlyStopping
import joblib

def output(window=10,District='Kolkata'):
#   window = (int)(input("Enter number of days to be predicted:"))
#   District = input("Enter District name:")
  t,c = time_series(window, District)
  date_time = t[-window:]
  predicted_cases = c[-window:]

  #print("yes")
  #for i in range(window):
    #print("Date: {}   Predicted Cases: {}".format(
        #date_time[i], predicted_cases[i][0]))
  filename = 'finalized_model.sav'
  joblib.dump(predicted_cases, filename)
  return date_time ,predicted_cases
  
def data_fetcher(District):
  data1 = pd.read_csv('https://api.covid19india.org/csv/latest/districts.csv')
  datanew = data1[data1['District'] == District]
  datanew1 = datanew.reset_index(drop="False")
  datanew2 = datanew1
  datanew2.pop('Other')
  datanew2.pop('State')
  datanew2.pop('District')
  titles = list(datanew2.columns)
  titles[1], titles[3] = titles[3], titles[1]
  titles[3], titles[4] = titles[4], titles[3]
  data = datanew2[titles]
  data['Tested'] = 70000
  data = data.reset_index()
  data = data.drop(["index"], 1)

  return data


def time_series(window, District):
  time_series_wb = data_fetcher(District)
  time_series_wb['Date'] = time_series_wb['Date'].apply(pd.to_datetime)
  time_series_wb.set_index("Date", inplace=True)
  df_new = time_series_wb
  df_new.drop(df_new.columns[[0, 1, 2]], axis=1, inplace=True)
  total_data = time_series_wb.shape[0]

  # No train size
  x = 12
  train_size = total_data - x
  test_size = x
  train = df_new[:train_size]
  test = df_new[train_size:]
  scaler = MinMaxScaler()
  scaler.fit(train)
  scaled_train = scaler.transform(train)
  scaled_test = scaler.transform(test)
  scaled_test, scaled_train

  # how to decide num of inputs ,
  n_input = 5  # number of steps
  # number of features you want to predict (for univariate time series n_features=1)
  n_features = 1
  generator = TimeseriesGenerator(
      scaled_train, scaled_train, length=n_input, batch_size=1)
  x, y = generator[50]

  model = Sequential()
  model.add(LSTM(300, activation="relu", input_shape=(n_input, n_features)))
  # model.add(Dropout(0.2))
  model.add(Dense(75, activation='relu'))
  model.add(Dense(units=1))
  # model.add(Activation('softmax'))
  # model.add(Dense(1))
  model.compile(optimizer="adam", loss="mse")

  validation_set = scaled_test
  validation_set = validation_set.reshape(12, 1)

  n_input = 5
  n_features = 1
  validation_gen = TimeseriesGenerator(
      validation_set, validation_set, length=5, batch_size=1)

  # early_stop = EarlyStopping(
  #     monitor='val_loss', patience=20, restore_best_weights=True)
  # model.fit_generator(generator, validation_data=validation_gen,
  #                     epochs=100, callbacks=[early_stop], steps_per_epoch=10)
  model.fit_generator(generator, validation_data=validation_gen,
                      epochs=15, steps_per_epoch=10)


  # # Convert the model.
  # converter = tf.lite.TFLiteConverter.from_keras_model(model)
  # tflite_model = converter.convert()
  # # Save the model.
  # with open('model.tflite', 'wb') as f:
  #   f.write(tflite_model)

  # holding predictions
  test_prediction = []

  # last n points from training set
  first_eval_batch = scaled_train[-n_input:]
  current_batch = first_eval_batch.reshape(1, n_input, n_features)

  # how far in future we can predict
  for i in range(len(test) + window):
    current_pred = model.predict(current_batch)[0]
    test_prediction.append(current_pred)
    current_batch = np.append(current_batch[:, 1:, :], [
                              [current_pred]], axis=1)

  true_prediction = scaler.inverse_transform(test_prediction)

  time_series_array = test.index
  for k in range(0, window):
    time_series_array = time_series_array.append(
        time_series_array[-1:] + pd.DateOffset(1))

  return time_series_array, true_prediction



if __name__ == '__main__':
  d,p = output()
  print(d)
  print(p)

  filename = 'finalized_model.sav'
  joblib.dump(p,filename)