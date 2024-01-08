import numpy as np  # 引入numpy、pandas库
import pandas as pd
from dbfread import DBF
from pandas import DataFrame
import matplotlib.pyplot as plt
import proplot as plot
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from IPython.display import display
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter  # 刻度格式
import matplotlib.ticker as mticker  # 添加网格线
import math

pd.options.display.max_columns = None

path = "./data/IBTrACS.since1980.list.v04r00.lines.dbf"
df_raw = pd.DataFrame(iter(DBF(path)))

df = df_raw

def filter_indesity(year, indensity):
    """
    int year: year
    indensity: 台风大小
    return 返回满足年份year台风大小大于34的台风编号列表 以及最小台风大小
    """
    df_year = df[df['year'] == year]
    Typh_times = df_year['NUMBER'].value_counts().sort_index().reset_index() # 每个台风出现的次数
    Typh_times.rename(columns={'NUMBER': 'times'})
    ls_num_34 = []
    ls_min = []
    ls_max = []
    for typh_num in Typh_times['index']:
        df_typh_num = df_year[df_year['NUMBER'] == typh_num]
        typh_num_max = df_typh_num['USA_WIND'].max()
    #     print("The No. %d maxium is %.2f" %(typh_num, typh_num_max))
        if math.isnan(typh_num_max) is False:
            if typh_num_max > indensity:
                ls_wind_indesity = list(df_typh_num['USA_WIND'])
                length_indesity = len(ls_wind_indesity)
                typh_num_min = df_typh_num['USA_WIND'].min()
                df_indesity_min = df_typh_num[df_typh_num['USA_WIND'] == typh_num_min]
                min_times = df_indesity_min['USA_WIND'].value_counts()
                min_times = min_times[int(typh_num_min)]
                ls_num_34.append(typh_num)
                ls_min.append(typh_num_min) 
                ls_max.append(typh_num_max)

    return ls_num_34, ls_min, ls_max

def filter_min_and_max(year, num):
    """
    int TpyhoneNomber:  num
    return 返回当前year年份的编号为num的最小台风数据和最大台风数据 dataframe
    """
    df_year = df[df['year'] == year]
    df_typh_num = df_year[df_year['NUMBER'] == num]
    typh_num_max = df_typh_num['USA_WIND'].max() # 查找最大值
#     print("The No. %d maxium is %.2f" %(typh_num, typh_num_max))

    ls_wind_indesity = list(df_typh_num['USA_WIND']) #列出台风风速的列表
    # length_indesity = len(ls_wind_indesity)  # 求长度
    typh_num_min = df_typh_num['USA_WIND'].min() # 找出最小台风风速

    df_indesity_min = df_typh_num[df_typh_num['USA_WIND'] == typh_num_min] # 设置最小台风风速的dataframe结构
    # min_counts = df_indesity_min['USA_WIND'].value_counts() #计算最小值出现了多少次
    # min_counts[int(typh_num_min)]
    # df_indesity_min[:1]

    df_indesity_max = df_typh_num[df_typh_num['USA_WIND'] == typh_num_max] # 设置最大台风风速的dataframe结构
    return df_indesity_min, df_indesity_max
    
def aptitude(year_list):
    """
    year_list: einino, lanina, neutrual
    """
    df_aptitude_min = pd.DataFrame(columns=["SEASON", "NUMBER", "LAT", "LON", "USA_WIND"])
    df_aptitude_max = pd.DataFrame(columns=["SEASON", "NUMBER", "LAT", "LON", "USA_WIND"])

    for year in year_list:
        ls_num_34_year, ls_min_year, ls_max_year = filter_indesity(year)
        for number, min_typh in zip(ls_num_34_year, ls_min_year):
            df_indesity_min, df_indesity_max = filter_min_and_max(year, number)
            df_aptitude_min = df_aptitude_min.append(df_indesity_min[0:1].loc[df_indesity_min['USA_WIND'] == min_typh, ["SEASON", "NUMBER", "LAT", "LON", "USA_WIND"]], ignore_index=True)
        for number, max_typh in zip(ls_num_34_year, ls_max_year):
            df_indesity_min, df_indesity_max = filter_min_and_max(year, number)
            df_aptitude_max = df_aptitude_max.append(df_indesity_max[0:1].loc[df_indesity_max['USA_WIND'] == max_typh, ["SEASON", "NUMBER", "LAT", "LON", "USA_WIND"]], ignore_index=True)

    return df_aptitude_min, df_aptitude_max

def main():
    """
    厄尔尼诺年(1982、1986-1987、1991、1994、1997、2002、2004、2009、2015)。
    拉尼娜年(1988、1995、1998-2000、2007、2010-2011，2016、2020-2021).
    中立年份(1983-1985、1989-1990、1992-1993、1995-1996、2001、2003、2005-2006、2008、2012-2014、2017-2019)
    """

    # 1. 厄尔尼诺年(1982、1986-1987、1991、1994、1997、2002、2004、2009、2015)。
    einino = [1982,1986,1987,1991,1994,1997,2002,2004,2009,2015]
    # einino = [1986,1987,1991,1994,1997,2002,2004,2009,2015]
    lanina = [1988, 1995, 1998, 1998, 2000, 2007, 2010, 2011, 2016, 2020, 2021]
    neutrual = [1983, 1984, 1985, 1989, 1990, 1992, 1993, 1995, 1996, 2001, 2003, 2005, 2006, 2008, 2012, 2013, 2014, 2017, 2018, 2019]

    df_aptitude_einino_min,  df_aptitude_einino_max= aptitude(einino)
    df_aptitude_lanina_min,  df_aptitude_lanina_max = aptitude(lanina)
    df_aptitude_neutrual_min,  df_aptitude_neutrual_max =  aptitude(neutrual)

    map_proj = ccrs.PlateCarree(central_longitude=180)
    tick_proj = ccrs.PlateCarree(central_longitude=0)

    fig, ax = plt.subplots(
        nrows=1, ncols=1, figsize=(16, 10),
        subplot_kw={'projection': map_proj}
    )

    ax.set_global()
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.set_xticks(np.linspace(-180, 180, 7), crs=tick_proj)
    ax.set_yticks(np.linspace(-90, 90, 5), crs=tick_proj)

    ax.xaxis.set_major_formatter(LongitudeFormatter())
    ax.yaxis.set_major_formatter(LatitudeFormatter())


    ax.scatter(df_aptitude_einino_min['LON'], df_aptitude_einino_min['LAT'],
            s=10, c = 'r', marker = 'o', 
            transform=ccrs.PlateCarree())

    ax.scatter(df_aptitude_einino_max['LON'], df_aptitude_einino_max['LAT'],
            s=10, c = 'b', marker = '*', 
            transform=ccrs.PlateCarree())

    map_proj = ccrs.PlateCarree(central_longitude=180)
    tick_proj = ccrs.PlateCarree(central_longitude=0)

    fig = plt.figure(figsize=[20, 10])

    ax1 =fig.add_subplot(2,3,1,projection=map_proj)
    ax1.set_global()
    ax1.add_feature(cfeature.LAND)
    ax1.add_feature(cfeature.OCEAN)
    ax1.set_xticks(np.linspace(-180, 180, 7), crs=tick_proj)
    ax1.set_yticks(np.linspace(-90, 90, 5), crs=tick_proj)
    ax1.xaxis.set_major_formatter(LongitudeFormatter())
    ax1.yaxis.set_major_formatter(LatitudeFormatter())
    ax1.set_title("fig 1")
    ax1.scatter(df_aptitude_einino_min['LON'], df_aptitude_einino_min['LAT'],
            s=3, c = 'r', marker = 'o', 
            transform=ccrs.PlateCarree())

    ax2 =fig.add_subplot(2,3,4,projection=map_proj)
    ax2.set_global()
    ax2.add_feature(cfeature.LAND)
    ax2.add_feature(cfeature.OCEAN)
    ax2.set_xticks(np.linspace(-180, 180, 7), crs=tick_proj)
    ax2.set_yticks(np.linspace(-90, 90, 5), crs=tick_proj)
    ax2.xaxis.set_major_formatter(LongitudeFormatter())
    ax2.yaxis.set_major_formatter(LatitudeFormatter())
    ax2.scatter(df_aptitude_einino_max['LON'], df_aptitude_einino_max['LAT'],
            s=3, c = 'b', marker = 'o', 
            transform=ccrs.PlateCarree())

    ax3 =fig.add_subplot(2,3,2,projection=map_proj)
    ax3.set_global()
    ax3.add_feature(cfeature.LAND)
    ax3.add_feature(cfeature.OCEAN)
    ax3.set_xticks(np.linspace(-180, 180, 7), crs=tick_proj)
    ax3.set_yticks(np.linspace(-90, 90, 5), crs=tick_proj)
    ax3.xaxis.set_major_formatter(LongitudeFormatter())
    ax3.yaxis.set_major_formatter(LatitudeFormatter())
    ax3.scatter(df_aptitude_lanina_min['LON'], df_aptitude_lanina_min['LAT'],
            s=3, c = 'r', marker = 'o', 
            transform=ccrs.PlateCarree())

    ax4 =fig.add_subplot(2,3,5,projection=map_proj)
    ax4.set_global()
    ax4.add_feature(cfeature.LAND)
    ax4.add_feature(cfeature.OCEAN)
    ax4.set_xticks(np.linspace(-180, 180, 7), crs=tick_proj)
    ax4.set_yticks(np.linspace(-90, 90, 5), crs=tick_proj)
    ax4.xaxis.set_major_formatter(LongitudeFormatter())
    ax4.yaxis.set_major_formatter(LatitudeFormatter())
    ax4.scatter(df_aptitude_lanina_max['LON'], df_aptitude_lanina_max['LAT'],
            s=3, c = 'b', marker = 'o', 
            transform=ccrs.PlateCarree())

    ax5 =fig.add_subplot(2,3,3,projection=map_proj)
    ax5.set_global()
    ax5.add_feature(cfeature.LAND)
    ax5.add_feature(cfeature.OCEAN)
    ax5.set_xticks(np.linspace(-180, 180, 7), crs=tick_proj)
    ax5.set_yticks(np.linspace(-90, 90, 5), crs=tick_proj)
    ax5.xaxis.set_major_formatter(LongitudeFormatter())
    ax5.yaxis.set_major_formatter(LatitudeFormatter())
    ax5.scatter(df_aptitude_neutrual_min['LON'], df_aptitude_neutrual_min['LAT'],
            s=3, c = 'r', marker = 'o', 
            transform=ccrs.PlateCarree())

    ax6 =fig.add_subplot(2,3,6,projection=map_proj)
    ax6.set_global()
    ax6.add_feature(cfeature.LAND)
    ax6.add_feature(cfeature.OCEAN)
    ax6.set_xticks(np.linspace(-180, 180, 7), crs=tick_proj)
    ax6.set_yticks(np.linspace(-90, 90, 5), crs=tick_proj)
    ax6.xaxis.set_major_formatter(LongitudeFormatter())
    ax6.yaxis.set_major_formatter(LatitudeFormatter())
    ax6.scatter(df_aptitude_neutrual_max['LON'], df_aptitude_neutrual_max['LAT'],
            s=3, c = 'b', marker = 'o', 
            transform=ccrs.PlateCarree())

    fig.show()
    fig.savefig("./storm.jpg")

if __name__ == "__main__":
    main()
