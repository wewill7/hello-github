# import xlrd
# import pandas as pd
# data = xlrd.open_workbook('C:/Users/Administrator/Desktop/ARIMA/bianma/analyse-wuhan-ouhuan-day(bianma).xlsx')
# count = len(data.sheets())
# print(count)
# df = pd.DataFrame(columns=['物料名称','物料编码','出库记录数'])
# for i in range(0,count):
#     table = data.sheets()[i]
#     name1 = table.cell(1,1).value
#     nrows = table.nrows
#     name = table.name
#     # dict[name] = nrows-1
#     df = df.append(pd.DataFrame({'物料名称': [name1], '物料编码': [name], '出库记录数': [nrows]}), ignore_index=True)
#
# df.sort_values(by=['出库记录数'],ascending=False,inplace=True)
# outpath = 'C:/Users/Administrator/Desktop/ARIMA/bianma/name-wuhan-ouhuan-day(bianma).xlsx'
# writer = pd.ExcelWriter(outpath)
# df.to_excel(excel_writer=writer,sheet_name='sheet')
# writer.save()


import xlrd
import pandas as pd
# data = pd.read_excel('C:/Users/Administrator/Desktop/ARIMA/bianma/analyse-wuhan-ouhuan-day(bianma).xlsx',sheet_name=None)
data = pd.ExcelFile('C:/Users/Administrator/Desktop/ARIMA/bianma/analyse-wuhan-bihuan-day.xlsx')
outpath = 'C:/Users/Administrator/Desktop/ARIMA/bianma/name-wuhan-bihuan-day(bianma).xlsx'
count = len(data.sheet_names)
print(data.parse(data.sheet_names[0]))
df = pd.DataFrame(columns=['物料名称','物料编码','出库记录数'])
for i in range(count):
    table = data.parse(data.sheet_names[i],index_col=0)

    name = table.iloc[0,0]
    bianma = data.sheet_names[i]
    nrows = table.shape[0]

    df.loc[i]=[name,bianma,nrows]
    # df=df.append(pd.DataFrame({'物料名称':[name],'物料编码':[bianma], '出库记录数':[nrows]}),ignore_index=True)


df.sort_values(by=['出库记录数'],ascending=False,inplace=True)
df.index = list(range(len(data.sheet_names)))
writer = pd.ExcelWriter(outpath)
df.to_excel(excel_writer=writer,sheet_name='sheet')
writer.save()