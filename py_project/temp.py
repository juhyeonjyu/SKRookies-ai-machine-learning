import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

data = pd.read_csv('fulldata_.csv', encoding='cp949', low_memory=False)
# print(data.columns.values)

data_1 = data[['영업상태명', '사업장명', '도로명전체주소', '홈페이지', '소재지전화']]
# data_1

# 도로명전체주소 기준 값 NA 행 삭제
data_1 = data_1.dropna(subset=['도로명전체주소'])
# data_1.info()

data_2 = data_1[data_1['도로명전체주소'].str.contains('경기도')]
# data_2.head()

data_3 = data_2[data_2['영업상태명'] != '폐업']
# data_3.head()

data_3.loc[:, '경기도 내 행정구역'] = data_3['도로명전체주소'].str.split().str[1]
# data_3.head()

data_4 = data_3.groupby('경기도 내 행정구역').size().reset_index(name='사업장 수')
# data_4

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.figure(figsize=(12,6))

plt.bar(data_4['경기도 내 행정구역'], data_4['사업장 수'])
plt.xticks(rotation=45)
plt.title('경기도 내 영업 중인 휴게음식점')
plt.xlabel('행정구역')
plt.ylabel('사업장 수')

plt.show()