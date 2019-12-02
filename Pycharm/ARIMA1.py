import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.tsa.stattools import adfuller as ADF
plt.rcParams['font.sans-serif'] = ['SimHei'] #正常显示中文字体黑体
plt.rcParams['axes.unicode_minus'] = False #正常显示表示负号
filename='C:/Users/Administrator/Desktop/ARIMA/ARIMA/entireTime1.xlsx'
forrecastnum=3
data=pd.read_excel(filename,index_col=0)
data.plot()
plt.title('Time Series')
plt.show()
plot_acf(data)
plt.show()
print(u'原始序列的ADF检验结果为：',ADF(data[u'数量']))

D_data=data.diff(2).dropna()
D_data.columns=[u'数量差分']
D_data.plot()
plt.show()
plot_acf(D_data).show()
plot_pacf(D_data).show()
print(u'1阶差分序列的ADF检验结果为：',ADF(D_data[u'数量差分']))
from statsmodels.stats.diagnostic import acorr_ljungbox
print(u'差分序列的白噪声检验结果为：',acorr_ljungbox(D_data,lags=1))
from statsmodels.tsa.arima_model import ARIMA
data[u'数量'] = data[u'数量'].astype(float)
# pmax=int(len(D_data)/30)
# qmax=int(len(D_data)/30)
# bic_matrix=[]
# for p in range(pmax+1):
#     tmp=[]
#     for q in range(qmax+1):
#         try:
#             tmp.append(ARIMA(data,(p,1,q)).fit().bic)
#         except:
#             tmp.append(None)
#     bic_matrix.append(tmp)
# bic_matrix=pd.DataFrame(bic_matrix)
# print(bic_matrix)
# p,q=bic_matrix.stack().idxmin()
# print(u'bic最小的P值和q值为：%s、%s'%(p,q))
model=ARIMA(data,(3,1,3)).fit()
model.summary2()
forecast=model.forecast(3)
print("aa:",forecast)