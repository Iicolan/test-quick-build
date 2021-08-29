#coding=UTF-8
'''
This code deals with emon_data, including four categories: CSP, Enterprise, Public and Speccpu.
The ouput files include gen_perf.csv and workload_with_all_metrics_demo.csv, which corresponding to emon_data with all metrics
and emon_data with 19 selected metrics, respectively.
'''
import numpy as np
import pandas as pd
import os

if __name__ == '__main__':
  path = os.getcwd()
  '''
  testdata = None
  for root, dirs, files in os.walk(os.path.join(path,'..') + '/emon_data/'):
    #root当前路径，dirs该路径下子目录， files该路径下文件
    for i in range(len(files)):
      print(files[i])
      f = pd.read_excel(root + '/' + files[i], sheet_name = 'socket view', engine = 'openpyxl')
      row_name = f[f.columns[0]].values[0:]
      col_name = [os.path.splitext(files[i])[0]]
      temp = pd.DataFrame(f['socket 0'].values[:], index=row_name, columns=col_name)

      f1 = pd.read_excel(root + '/' + files[i], sheet_name = 'details socket view', engine = 'openpyxl')
      CPI = f1['metric_CPI (socket 0)'].dropna(axis=0,how='any')
      IPC = [1/x for x in CPI]
      CPU_Util = f1['metric_CPU utilization % (socket 0)']
      row_name1 = ['IPC_std_normalize','CPU_Util_std_normalize']
      std_values = [np.std(IPC), np.std(CPU_Util)]
      temp1 = pd.DataFrame(std_values, index=row_name1, columns=col_name)
      temp = pd.concat([temp, temp1],axis=0)
      testdata = pd.concat([testdata, temp],axis=1)
  # 所有workload的所有指标保存为gen_perf.csv
  testdata.to_csv('gen_perf.csv')
  '''
  testdata = pd.read_csv('gen_perf.csv', index_col = 0)
  # 只提取metric.txt中提到的几个维度的数据
  f = open(path + '/metric.txt', 'r')
  PCA_names= f.readlines()
  PCA_names = [x.strip('\n') for x in PCA_names] #PCA_names是多个维度指标
  f.close()  # 关闭文件

  # 读取文件并整理数据
  col_name = testdata.columns.values.tolist()
  result= None

  for names in PCA_names:
    data_temp = np.array([0])
    for i in range(len(names.split(','))):
      metric_name = names.split(',')[i]
      data_temp = data_temp + np.array([float(str(i).replace(',', '').replace('nan','0'))
                                      for i in (testdata.loc[[metric_name]]).values[0]])
    temp = pd.DataFrame(data_temp, columns = [names.split(',')[0]])
    result = pd.concat([result, temp],axis=1) #每一行是一个workload
  result.insert(0,'wl_name',col_name)
  result.to_csv('demo.csv')
