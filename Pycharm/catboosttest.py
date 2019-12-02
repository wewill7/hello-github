import pandas as pd
import numpy as np
from catboost import CatBoostRegressor

filename='C:/Users/Administrator/Desktop/ARIMA/ARIMA/entireTime1.xlsx'
data=pd.read_excel(filename, sheet_name=1, index_col=0,dtype={'数量': float})
# data.drop(data.tail(4).index,inplace=True)


def create_data(data, lookback):
    '''
    制造数据集

    data：原始数据
    idx：哪一个发电站
    skip：跳空多少分钟
    lookback：用前多少分钟的数据训练
    '''

    # train_data = data.sort_values(['date']).reset_index(drop=True)

    # min_max_scaler = MinMaxScaler()
    # train_data['value'] = min_max_scaler.fit_transform(train_data['value'].values.reshape(-1, 1))

    # print(train_data.shape)

    # if train_data.value.nunique()<5:
    #    return None

    # print(train_data.head())
    '''
    dataX, dataY = [], []
    for i in range(lookback, (train_data.shape[0] - skip-1), lookforward):
        x = train_data['value'][(i - lookback) : i].values
        dataX.append(x)
        y = train_data['value'][(i + skip):(i + skip + lookforward)].values
        dataY.append(y)

    dataX = np.array(dataX)
    dataY = np.array(dataY)

    #数据维度变成[samples,时间步长, 特征数量]
    dataX = np.reshape(dataX, (dataX.shape[0], dataX.shape[1], 1))
    dataY = np.reshape(dataY, (dataY.shape[0], dataY.shape[1]))
    '''
    data = data['数量'].values

    # print(train_data.shape)

    dataX, dataY = [], []
    testX, testY = [], []
    for i in range(lookback, len(data)-10):
        dataX.append(data[(i - lookback): i])
        dataY.append(data[i])

    for i in range(len(data)-10, len(data)):
        testX.append(data[(i - lookback): i])
        testY.append(data[i])

    dataX = np.array(dataX)
    dataY = np.array(dataY)
    testX = np.array(testX)
    testY = np.array(testY)

    # print(dataX.shape,dataY.shape)

    return dataX, dataY, testX, testY

dataX, dataY, testX, testY=  create_data(data,12)
dataX = pd.DataFrame(dataX)
print(testY)

model = CatBoostRegressor(iterations=100, depth=6, learning_rate=0.1, loss_function='RMSE')
model.fit(dataX,dataY,eval_set=(testX, testY))
preds = model.predict(testX)
print(preds)

