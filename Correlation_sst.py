import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import netCDF4 as nc
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.mpl.gridliner 
# import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import cartopy.mpl.ticker as cticker
import cartopy.io.shapereader as shpreader
from math import sqrt

from matplotlib import colors,cm
import matplotlib as mpl
import cmaps
from matplotlib.colors import ListedColormap 


file = './HadISST_sst.nc'
dataset = nc.Dataset(file)
# print(dataset.variables.keys())

longitude, latitude = dataset.variables['longitude'],dataset.variables['latitude']
time = dataset.variables['time']
sst =dataset.variables['sst']

sum_month = np.zeros(sst[:1].data.shape, dtype=float, order='C') # 创建空矩阵
num_month = time[:].data.shape[0] # 创建空时间矩阵
num_month_1997to1982 = (1998 - 1982) * 12 #计算1982年1月到1997年12月的192月数
num_month_2021to1998 = (2022 - 1998) * 12 #计算1998年1月到2021年12月的288月数
sum_month = np.zeros(sst[:1].data[0][44:136,:].shape, dtype=float, order='C') # 创建空矩阵

sum_month_year = sum_month

ls_mean_year = []
for i in range(1343, 1343+num_month_1997to1982+num_month_2021to1998, 12): 
    for month in range(12):
        tmp_month = i + month
        tmp_pre = sst[tmp_month:tmp_month+1].data[0][44:136,:]
        sum_month_year += tmp_pre
    mean_year = sum_month_year / 12
#     mean_year = mean_year.tolist()
    ls_mean_year.append(mean_year)

cor_num = pd.read_excel(io = r'./ACE.xlsx')

coordinate = cor_num['WP-NA'].tolist()

# 矩阵进行转换
reshape_mean = ls_mean_year.transpose(1,2,0)



