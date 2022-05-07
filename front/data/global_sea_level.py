# -*- coding: utf-8 -*-
"""해수면상승_정리완료.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PKb_O265laru0UIoOg0vG9krVvfpnpHr
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import scipy as sp
import scipy.stats

# %matplotlib inline



datapath = './sealevel.csv'
df = pd.read_csv(datapath)

print(df.shape)
print("--------------------------------------------------------------------------------")
print(df.columns)
print("--------------------------------------------------------------------------------")
print(df.info())

"""> 데이터 정보
>
> __***위성으로 관찰한 해수면 변화***__

* Total Wighted Observations 
  * 각 데이터의 중요도를 판단하는 기준으로 둘 수 있다
  * Weight가 어떻게 도출되었는지 method에 대한 정보가 없어 기준으로 해도 될 지 판단하기 어렵다
  * 중요도의 수치를 시각화해서 어떤 값들이 있는지 확인할 계획이다


* GMSL : 지구 평균 해수면


* GIA : 빙하로 인한 해수면 차이값에 대한 조정 
  * 조정이 적용된 값, 조정이 적용되지 않은 값
  * **실제로 해수면이 상승한 값을 나타내므로 시각화 할 데이터로 결정함**

* StdDev : 표준 편차 값

* Smoothed : 가우시안 필터 적용한 값

> ___***Q. GIA 적용한 값/적용하지 않은 값 그리고 각 GMSL/StdDev/Smoothed 모두 plot 해봐야 하는건가?***___
  * 일단 해봄


> ___***Q. 해수면 상승 속도 비교할 수 있는지 질문하기***___
  * 최근 상승 속도가 증가했다는 가설 검증
"""

df = df[['Year', 'TotalWeightedObservations', 'GMSL_GIA']]

df

# 이상치를 제거하기 위해 표준화


print('feature 들의 평균 값')
print(df.mean())
print('feature 들의 분산 값')
print(df.var())

scaler = StandardScaler()
scaler.fit(df)
df_scaled = scaler.transform(df)

print("-표준화-")
scaled_sealevel_df = pd.DataFrame(data = df_scaled, columns = df.columns)
print('feature들의 평균 값')
print(scaled_sealevel_df.mean())
print(scaled_sealevel_df.var())

from collections import Counter

# 이상치 제거
def detect_outliers(scaled_sealevel_df, n, features):
  #n 값은  행 별로 outliers로 선택된 값이 몇 개 포함 되었는지 Counter 클래스로 딕셔너리로 만들어 준 후 n 개 보다 넘을 경우에만 drop 해주는 용도로 넣어준다.
    outlier_indices = []
    for col in features:
        Q1 = np.percentile(scaled_sealevel_df[col], 25)
        Q3 = np.percentile(scaled_sealevel_df[col], 75)
        IQR = Q3 - Q1
        
        outlier_step = 1.5 * IQR
        
        outlier_list_col = scaled_sealevel_df[(scaled_sealevel_df[col] < Q1 - outlier_step) | (scaled_sealevel_df[col] > Q3 + outlier_step)].index
        outlier_indices.extend(outlier_list_col)
    outlier_indices = Counter(outlier_indices)
    print(outlier_indices)
    multiple_outliers = list(k for k, v in outlier_indices.items() if v > n)
        
    return multiple_outliers
        
Outliers_to_drop = detect_outliers(scaled_sealevel_df, 2, ['Year', 'TotalWeightedObservations', 'GMSL_GIA'])

# 이상치 확인
scaled_sealevel_df.loc[Outliers_to_drop]

#TotalWeightedObservations 에서 drop할 값 확인
f, ax = plt.subplots(2, 1, figsize=(15,5))

x0 = scaled_sealevel_df.TotalWeightedObservations.plot(kind='box', vert=False, ax=ax[0])
plt.title('TotalWeightedObservations')
plt.grid()

x1 = df.TotalWeightedObservations.plot(kind='box', vert=False, ax=ax[1])
plt.title('TotalWeightedObservations')
plt.grid()

plt.show()

df_highweighted_scaled = scaled_sealevel_df[scaled_sealevel_df['TotalWeightedObservations']>-0.3]
filtered_index = list(df_highweighted_scaled.index)

scaled_sealevel_df.rename(columns={'TotalWeightedObservations':'TotalWeightedObservations_scaled'}, inplace=True)
scaled_sealevel_df

ov_scaled = scaled_sealevel_df[['TotalWeightedObservations_scaled']]

cc_df = pd.concat([df, ov_scaled], axis=1)

cc_df

df_highweighted = cc_df[cc_df.TotalWeightedObservations_scaled>-0.3]

year = list(df_highweighted['Year'].unique())
print(len(year))

"""> 년도별 지구 평균 해수면 관측치의 평균값을 시각화"""

avg = {}

for i in year:
  avg[i] = df_highweighted[df_highweighted['Year'] == i].GMSL_GIA.mean()

avg

"""> 1993년 관측된 해수면 수위를 기준으로 변환"""

yearly_sealever = pd.DataFrame(list(avg.items()), columns=['Year', 'Gsl'])
yearly_sealever_1993std = yearly_sealever - yearly_sealever.iloc[0]

yearly_sealever_1993std

col_year = yearly_sealever['Year']
col_gsl = yearly_sealever_1993std['Gsl']
gsl = pd.concat([col_year, col_gsl], axis=1)

plt.figure(figsize = (16, 6))

xticks = year

sns.barplot(data = yearly_sealever_1993std, x = xticks, y = 'Gsl')

plt.show()

"""> 4년 주기로 크게 상승한 것을 시각화"""

gsl = gsl.set_index('Year')

year = [1993, 1997, 2001, 2005, 2009, 2013, 2017, 2021]
df_gsl = gsl.loc[year]

df_gsl = df_gsl.reset_index().round(2)
df_gsl.to_csv('global_sea_level.csv')

df_gsl

plt.figure(figsize = (16, 6))

sns.barplot(data = df_gsl, x = 'Year', y = 'Gsl')

plt.show()

gslper4years