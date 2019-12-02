import numpy as np
import pandas as pd
path = "C:/Users/Administrator/Desktop/ARIMA/bianma/analyse-wuhan-ouhuan-day(bianma).xlsx"
SheetOuhuanData = pd.read_excel("C:/Users/Administrator/Desktop/ARIMA/bianma/name-wuhan-ouhuan-day(bianma).xlsx",index_col=0,dtype={'物料编码':str})
SheetBihuanData = pd.read_excel("C:/Users/Administrator/Desktop/ARIMA/bianma/name-wuhan-bihuan-day(bianma).xlsx",index_col=0,dtype={'物料编码':str})

###choose the name of material
for nama in range(32,33):
    Sheetname = SheetOuhuanData['物料编码'][nama]
    data=pd.read_excel(path,sheet_name= Sheetname,index_col=0)
    name = data.iloc[0,0]
    if(Sheetname in list(SheetBihuanData['物料编码'])):
        outpath = "C:/Users/Administrator/Desktop/ARIMA/bianma/ARIMA/oubihuan/"+str(nama)+' '+Sheetname+name+".xlsx"
    else:
        outpath = "C:/Users/Administrator/Desktop/ARIMA/bianma/ARIMA/ouhuan/"+ str(nama) + ' ' + Sheetname + name + ".xlsx"
    writer = pd.ExcelWriter(outpath)


    ###for days
    timelistd =pd.date_range(start='20171105',end='20191106')
    numsd = np.zeros(timelistd.shape[0])
    for i in range(data.shape[0]):
        for j in range(timelistd.shape[0]):
            if(data["出库时间"][i]==timelistd[j]):
                numsd[j]=data["数量"][i]
    # timeFrame['数量'] = pd.Series(nums)

    timeFramed = pd.DataFrame(columns = ('数量',), index=timelistd,data=numsd)
    timeFramed.to_excel(excel_writer =writer, sheet_name= Sheetname+"d")



    ##for weeks and cut the tail
    timelistw=pd.date_range(start='20171105',end='20191106',freq='7D')
    numsw= np.zeros(timelistw.shape[0])
    for i in range (data.shape[0]):
        for j in range (timelistw.shape[0]-1):
            if(data["出库时间"][i]>=timelistw[j] and data["出库时间"][i]<timelistw[j+1]):
                numsw[j] += data["数量"][i]

    timeFramew = pd.DataFrame(columns = ('数量',), index=timelistw,data=numsw)
    timeFramew.drop(timeFramew.tail(1).index,inplace=True)
    timeFramew.to_excel(excel_writer= writer, sheet_name= Sheetname+"w")


    ##for months and cut the tail
    timelistm=pd.date_range(start='20171105',end='20191106',freq='M')
    numsm= np.zeros(timelistm.shape[0])
    for i in range (data.shape[0]):
        for j in range (timelistm.shape[0]):
            if(j==0):
                if (data["出库时间"][i] < timelistm[j]):
                    numsm[j] += data["数量"][i]
            else:
                if(data["出库时间"][i]>=timelistm[j-1] and data["出库时间"][i]<timelistm[j]):
                    numsm[j] += data["数量"][i]

    timeFramem = pd.DataFrame(columns = ('数量',), index=timelistm, data=numsm)
    # timeFramem.drop(timeFramem.tail(1).index,inplace=True)
    timeFramem.to_excel(excel_writer= writer, sheet_name= Sheetname+"m")


    writer.save()