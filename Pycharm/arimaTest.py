import numpy as np
import pandas as pd
import pylab as p
import matplotlib.pyplot as plt
from collections import Counter
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.tsa.seasonal import seasonal_decompose
plt.rcParams['font.sans-serif'] = ['SimHei']    #定义使其正常显示中文字体黑体
plt.rcParams['axes.unicode_minus'] = False      #用来正常显示表示负号

filename='C:/Users/Administrator/Desktop/ARIMA/bianma/ARIMA/19010002009.xlsx'
data=pd.read_excel(filename, sheet_name=1, index_col=0,dtype={'数量': float})
data.plot()
plt.title('Time Series')
plt.show()
print(u'原始序列的ADF检验结果为：',ADF(data[u'数量']))

testdata = data.tail(12)
plotdata = data.tail(36)

#训练data 去除测试数据
data.drop(data.tail(4).index,inplace=True)
data2=data.copy(deep=True)
data.drop(data.tail(4).index,inplace=True)
data1=data.copy(deep=True)
data.drop(data.tail(4).index,inplace=True)

###去除前面的零行
while(data.head(1).values==0):
    data.drop(data.head(1).index, inplace=True)
data.plot()
plt.title('Time Series')
plt.show()
print(u'原始序列的ADF检验结果为：',ADF(data[u'数量']))
# decomposition = seasonal_decompose(data[u'数量'])
#
# trend = decomposition.trend
# seasonal = decomposition.seasonal
# residual = decomposition.resid
#
# decomposition.plot()
# #############
from statsmodels.tsa.stattools import acf, pacf

# lag_acf = acf(data, nlags=100)
# lag_pacf = pacf(data, nlags=100, method='ols')
#
# plt.subplot(1, 1, 1)
# plt.plot(lag_acf)
#
# plt.axhline(y=0, linestyle='--', color='g')
# plt.title('Autocorrelation Function')
# plt.show()
#
#
# plt.subplot(1, 1, 1)
# plt.plot(lag_pacf)
#
# plt.axhline(y=0, linestyle='--', color='g')
# plt.title('Partial Autocorrelation Function')
# plt.show()
#########
# 协相关绘图
########
# from statsmodels.graphics.tsaplots import plot_acf
# from statsmodels.graphics.tsaplots import plot_pacf
# D_data=data.diff(1).dropna()
# D_data.columns=[u'数量差分']
# D_data.plot()
# plt.show()
# print(u'1阶差分序列的ADF检验结果为：',ADF(D_data[u'数量差分']))
#
# plot_acf(D_data,lags=20).show()
# plt.show()
# plot_pacf(D_data,lags=20).show() #,method='ywm'
# plt.show()

# ##############
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

pmax=int(10)
qmax=int(10)
bic_matrix=[]
for p in range(pmax+1):
    tmp=[]
    for q in range(qmax+1):
        try:
            tmp.append(ARIMA(data,(p,1,q),freq='7D').fit().aic)
        except:
            tmp.append(None)
    bic_matrix.append(tmp)
bic_matrix=pd.DataFrame(bic_matrix)
for i in range(2):
    for j in range(2):
        bic_matrix.iloc[i,j]=None
print(bic_matrix)
p,q=bic_matrix.stack().astype('float64').idxmin()
print(u'aic最小的P值和q值为：%s、%s'%(p,q))
try:
    # p,q=(4,3)
    model = ARIMA(data, (p,1,q),freq='7D').fit() #transparams=False
    model1 = ARIMA(data1, (p, 1, q), freq='7D').fit()
    model2 = ARIMA(data2, (p, 1, q), freq='7D').fit()
except:
    pass
    print('ss')


# model.summary2()        #生成一份模型报告
forecast1=model.forecast(12)[0]
forecast2=pd.DataFrame(model.forecast(4)[0])
forecast2=forecast2.append(list(model1.forecast(4)[0]), ignore_index= True)
forecast2=forecast2.append(list(model2.forecast(4)[0]), ignore_index= True)
print("aa:",model1.forecast(4)[0])   #为未来5天进行预测， 返回预测结果， 标准误差， 和置信区间


#######
# 画图
fig, axes = plt.subplots(2, 1)
plotdata.plot(color='red',ax=axes[0])
plotdata.plot(color='red',ax=axes[1])

plotfore =pd.DataFrame(index= data.tail(1).index, data= data.tail(1).values, columns=["predict1"])
foredata1= pd.DataFrame(index= testdata.index, data= forecast1, columns=["predict1"])
plotfore1=plotfore.append(foredata1,sort= False)
plotfore1.plot(color='blue', ax= axes[0])
axes[0].set_title('RMSE1: %.4f ' % (np.sqrt(sum((foredata1.iloc[:,0] - testdata.iloc[:,0]) ** 2) / testdata.size)))

plotfore =pd.DataFrame(index= data.tail(1).index, data= data.tail(1).values, columns=["predict2"])
foredata2= pd.DataFrame(index= testdata.index, data= forecast2.values, columns=["predict2"])
plotfore2=plotfore.append(foredata2,sort= False)
plotfore2.plot(color='green', ax= axes[1])
axes[1].set_title('RMSE2: %.4f ' % (np.sqrt(sum((foredata2.iloc[:,0] - testdata.iloc[:,0]) ** 2) / testdata.size)))
# print('RMSE1: %.4f RMSE2: %.4f' % (np.sqrt(sum((foredata1.iloc[:,0] - testdata.iloc[:,0]) ** 2) / testdata.size),np.sqrt(sum((foredata2.iloc[:,0] - testdata.iloc[:,0]) ** 2) / testdata.size)))

# plt.figure(facecolor='white')
# plt.plot(plotdata,color='red',label="Original")
# plt.legend='Original'
# plt.plot(forecast,color='blue')
# plt.legend(loc='best')

# plt.title('RMSE1: %.4f RMSE2: %.4f' % (np.sqrt(sum((foredata1.iloc[:,0] - testdata.iloc[:,0]) ** 2) / testdata.size),np.sqrt(sum((foredata2.iloc[:,0] - testdata.iloc[:,0]) ** 2) / testdata.size)))
plt.tight_layout()
plt.show()
# ###模型检验1：残差自相关
# resid = model.resid
# plot_acf(resid.values.squeeze(),lags=20).show()
# plt.show()
# plot_pacf(resid.values.squeeze(),lags=20).show() #,method='ywm'
# plt.show()
#
# ###模型检验2：D-W检验
# print(sm.stats.durbin_watson(model.resid.values))

###模型检验3：是否符合正态分布
# fig = plt.figure(figsize=(12,8))
# ax = fig.add_subplot(111)
# fig = qqplot(resid, line='r', ax=ax, fit=True)
# plt.show()
###模型检验4： Ljung-Box检验
# r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
# data1 = np.c_[range(1,41), r[1:], q, p]
# table = pd.DataFrame(data1, columns=['lag', "AC", "Q", "Prob(>Q)"])
# print(table.set_index('lag'))






