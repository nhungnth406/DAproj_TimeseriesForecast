#!/usr/bin/env python
# coding: utf-8

# ## Importing libraries

# In[80]:


import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import numpy as np 
get_ipython().run_line_magic('matplotlib', 'inline')
from pylab import rcParams
rcParams['figure.figsize'] = 15,6


# ## Khảo sát dữ liệu

# In[72]:


df = pd.read_csv('raw_sales.csv')
#Trả về (n) hàng đầu tiên cho các đối tượng trong bộ dữ liệu. Quickly testing data
df.head()


# In[3]:


df.info()


# In[4]:


df.isnull().any()


# In[73]:


#Chuyển đổi kiểu dữ liệu của datesold thành kiểu datetime
df['datesold'] = pd.to_datetime(df['datesold'])
df.head()


# In[6]:


# Tính khoảng thời gian đầu - cuối của bộ dữ liệu
print("Time period from {} to {}".format(df.datesold.min(), df.datesold.max()))


# ## Descriptive analytics (Phân tích mô tả)

# ### Chuẩn bị dữ liệu

# In[74]:


# Lấy year từ datesold và chia dữ liệu thành 3 vùng chính dựa vào postcode: Region 1 (2599 - 2700), Region 2 (2701 - 2800), Region 3 (2801 - 2915)
df['year'] = df['datesold'].dt.year
for d in [df]:
  d.loc[(df['postcode'] > 2599) & (df['postcode'] <= 2700), 'region'] = 1;
  d.loc[(df['postcode'] > 2701) & (df['postcode'] <= 2800), 'region'] = 2;
  d.loc[(df['postcode'] > 2801) & (df['postcode'] <= 2915), 'region'] = 3;
df['region'] = df['region'].astype(int)
df.head()
# Bộ dữ liệu không có dữ liệu bán bất động sản ở vùng 2


# ### Tổng quan

# #### Số lượng bất động bán sản mỗi năm

# In[81]:


font1 = {'family':'serif','size':12}
c = (0.2, 0.4, 0.6, 0.6)
s = df.datesold.dt.year.value_counts().sort_index(ascending=True).plot.bar(color=c)


plt.title("SỐ LƯỢNG BẤT ĐỘNG BÁN ĐƯỢC TỪ NĂM 2007 ĐẾN NĂM 2019\n")
plt.xlabel("Year",fontdict = font1)
plt.ylabel("Sales",fontdict  = font1)
for i in s.patches:
    ypos = i.get_height() + 30
    xpos = i.get_x() + i.get_width()/2.
    lbl = i.get_height()
    plt.text(xpos, ypos,lbl , ha='center', va='bottom', fontsize=12)  


# Nhận xét: Nhìn chung, doanh số bán hàng có chiều hướng tăng dần từ năm 2007 tới năm 2017. Số lượng nhà bán được đạt đỉnh vào năm 2017, là 4541 căn, và bắt đầu giảm dần tới 2019.

# #### Giá bán nhà hàng năm thay đổi theo thời gian đối với tất cả các lần bán nhà

# In[82]:


sns.boxplot(x = df['year'], y = df['price'])
plt.title("GIÁ BÁN BẤT ĐỘNG SẢN HÀNG NĂM THAY ĐỔI THEO THỜI GIAN ĐỐI VỚI TẤT CẢ CÁC LẦN BÁN")
plt.ylabel("Giá bán (Trăm nghìn USD)")


# Nhận xét:
# - Nhìn vào biểu đồ, có thể thấy sự phân bổ tổng thể của giá bán nhà hơi lệch về bên trái, khoảng từ 2007 - 2013 (tập trung nhiều hơn vào giá cao hơn) với doanh số bán nhà đắt đỏ hơn vì dữ liệu về giá bán tập trung ở mức thấp, dao động ở phạm vi hẹp. 
# - Còn các năm trở về sau cho thấy sự phân bổ giá bán nhà kém hơn vì xu hướng tập trung của dữ liệu (trung vị) ở mức cao, độ dao động lớn (mặc dù sự phân bổ giá bán nhà trông khá giống nhau theo thời gian với sự chuyển động dần dần của các khu đất hộp)

# #### Số lượng bán của từng loại phòng ngủ qua từng năm

# In[7]:


df1=df.bedrooms.groupby(df['year']).value_counts(sort= False).reset_index(name='counts')
#Sắp xếp lại dữ liệu
df2=df1.pivot_table(index='year', values='counts', columns='bedrooms',fill_value=0)
df2.head()


# In[83]:


df2.plot(linewidth = '1',title='SỐ LƯỢNG BÁN CỦA TỪNG LOẠI PHÒNG NGỦ QUA TỪNG NĂM')


# Nhận xét: Theo biểu đồ ta thấy loại 3 phòng ngủ được bán chạy nhất, tăng từ năm 2007 đến năm 2017, loại 0 phòng ngủ được bán ít nhất với 30 căn trong tất cả các năm.

# ### Theo từng vùng

# #### Tổng giá trị bất động sản tất cả các năm theo từng vùng

# In[9]:


df1 = df
df1['type'] = "Region " + df1['region'].astype(str) + ": " + df1['propertyType'] 

df1 = df.drop(['datesold','bedrooms','postcode', 'region'], axis ='columns')
df1 = df1.groupby(['type','year']).sum().astype(int)
df2 = df1.pivot_table(index = 'year', values = 'price', columns = 'type', fill_value=0)

df2 = df2.sum(axis = 0)

# Trực quan hóa bằng biểu đồ cột ghép
df2.plot(kind = 'barh', title = 'TỔNG GIÁ TRỊ BÁN CỦA TỪNG LOẠI HÌNH BẤT ĐỘNG SẢN THEO TỪNG NĂM THEO TỪNG VÙNG')
plt.ylabel("Khu vực và loại nhà")
plt.xlabel("Tổng giá trị nhà bán (Tỷ USD)")
df2.head() 


# Nhận xét: Biểu đồ trên thể hiện tổng giá trị nhà bán theo loại hình ở khu vực 1 và khu vực 3. Nhìn chung, loại hình nhà ở được ưa chuộng hơn so với loại hình căn hộ ở cả 2 khu vực. Loại hình này ở khu vực 1 cũng chiếm tổng giá trị được bán cao nhất, lên đến $6.465.443.379.

# #### Giá bán trung bình của bất động sản ở từng khu vực biến động theo thời gian

# In[10]:


# Xử lý dữ liệu để phù hợp cho việc trực quan hóa
df1 = df.drop(['datesold','bedrooms','propertyType','postcode'], axis ='columns')
df1['type'] = "Region " + df1['region'].astype(str)
df1=df1.groupby(['year','type']).mean().astype(int)
df2=df1.pivot_table(index='year', values='price', columns='type',fill_value=0)
df2.head()


# In[12]:


# Trực quan hóa dữ liệu bằng biểu đồ đường
df2.plot(linewidth = '1',title='GIÁ BÁN TRUNG BÌNH BẤT ĐỘNG SẢN Ở TỪNG KHU VỰC QUA TỪNG NĂM')
plt.ylabel("Giá bán (USD)")


# Nhận xét:
# Giá bất động trung bình ở cả 2 khu vực nhìn chung có sự biến động qua các năm và có xu hướng chung là tăng lên. Giá bất động sản ở khu vực 1 luôn cao hơn ở khu vực 3. Đặc điểm chung của sự biến động là từ năm 2017, giá nhà giảm thấp nhất vào khoảng 2008,2009 sau đó tăng lên và có sự giảm nhẹ trong 2 năm 2011, 2012. Sau đó liên tục tăng lên và chạm điểm ở năm 2017 sau đó bắt đầu giảm xuống. Với khu vực 1, giá bất động sản chạm mốc cao nhất vào năm 2017, thấp nhất vào năm 2009. Với khu vực 3, giá bất động sản chạm mốc cao nhất vào năm 2018, thấp nhất vào năm 2008.

# ### Loại hình bất động sản

# #### Số lượng bán của từng loại loại hình bất động sản qua từng năm

# In[11]:


df1=df.propertyType.groupby(df['year']).value_counts(sort= False).reset_index(name='counts')
df2=df1.pivot_table(index='year', values='counts', columns='propertyType',fill_value=0)
df2.head()


# In[12]:


df2.plot(kind='bar', title='SỐ LƯỢNG BÁN CỦA TỪNG LOẠI HÌNH BẤT ĐỘNG SẢN QUA TỪNG NĂM' )


# Nhận xét: Lượng nhà bán ra tăng liên tục từ năm 2007 tới năm 2017 nhưng lại sụt giảm vào năm 2018 và 2019. Còn số lượng bán căn hộ (unit) cũng tăng nhưng lượng tăng thấp hơn so với lượng bán nhà.

# ###  Loại hình bất động sản theo từng khu vực
# 

# #### Số lượng bán của từng loại loại hình bất động sản theo khu vực qua từng năm

# In[15]:


#Số lượng bán của từng loại propertyType theo region qua từng năm

df1 = df.pivot_table(columns=['propertyType','region'],index=['year'], aggfunc='size')
df1.head(5)
df1.plot(linewidth = '1', figsize=(15,7))
plt.title("SỐ LƯỢNG BÁN CỦA TỪNG LOẠI HÌNH BẤT ĐỘNG SẢN THEO KHU VỰC QUA TỪNG NĂM")
plt.ylabel("\n Count")


# Nhận xét: Theo biểu đồ ta thấy số lượng house, unit ở khu vực 1 là được bán nhiều nhất, tăng dần theo từng năm đỉnh điểm nhất là khoảng thời gian từ 2014 - 2018.

# #### Tổng giá trị bất động sản theo từng vùng theo từng năm

# In[16]:


# THỐNG KÊ TỔNG GIÁ TRỊ NHÀ BÁN THEO TỪNG NĂM (TỪ NĂM 2007 ĐẾN NĂM 2019) THEO TỪNG VÙNG (REGION 1 VÀ REGION 3)

# Xử lý dữ liệu để phù hợp cho việc trực quan hóa
df1 = df.drop(['datesold','bedrooms','propertyType','postcode'], axis ='columns')
df1['Region'] = "Region " + df1['region'].astype(str)
df1 = df1.groupby(['year','Region']).sum().astype(int)
df2 = df1.pivot_table(index = 'year', values = 'price', columns = 'Region', fill_value=0)
df2.head(13)

# Trực quan hóa bằng biểu đồ cột ghép
df2.plot(kind = 'bar', title = 'TỔNG GIÁ TRỊ NHÀ BÁN THEO TỪNG NĂM THEO TỪNG VÙNG')
plt.ylabel("Giá bán (tỷ USD)")
plt.xlabel("Tổng giá trị nhà bán theo từng khu vực")
df2.head()


# Nhận xét: 
# Biểu đồ trên thể hiện sự phân bố tổng giá trị nhà bán theo từng năm của hai khu vực 1 và 3, ta có thể thấy tổng giá trị nhà bán của khu vực 1 luôn cao hơn so với khu vực 3 ở tất cả các năm. Điều này cho thấy thị trường nhà đất ở khu vực 1 năng động hơn so với khu vực 3. 
# Tổng giá trị nhà bán của cả 2 khu vực có xu hướng tăng dần trong một thập kỷ (từ năm 2007 đến năm 2017), cụ thể là tổng giá trị đã đạt mức cao nhất vào năm 2017 với 1.940.566.595 ở khu vực 1 và 1.110.442.989 ở khu vực 3.
# Năm 2018, tổng giá trị nhà bán có xu hướng giảm so với năm trước ở cả 2 khu vuc, cụ thể là ở khu vực 1, tổng giá trị giảm từ 1.940.566.595 xuống 1.621.215.228 (giảm 319.351.367) ở khu vực 3, tổng giá trị giảm từ 1.110.442.989 xuống 927.769.395 (giảm 182.673.594). 
# Năm 2019, tổng giá trị nhà bán tiếp tục có xu hướng giảm mạnh, ở khu vực 1, tổng giá trị giảm từ $1.621.215.228 xuống 528.492.633 (giảm 1.092.722.595). Ở khu vực 2, tổng giá trị giảm từ 927.769.395 xuống 349.852.510 (giảm 577.916.885).

# #### Giá bán trung bình bất động sản ở từng khu vực qua từng năm theo loại hình bất động sản

# In[17]:


df1 = df
df1['type'] = "Region " + df1['region'].astype(str) + ": " + df1['propertyType'] 
df1 = df.drop(['datesold','bedrooms','propertyType'], axis ='columns')
df1=df1.groupby(['year','type']).mean().astype(int)
df2=df1.pivot_table(index='year', values='price', columns='type',fill_value=0)
df2.head()


# In[18]:


# Trực quan hóa dữ liệu bằng biểu đồ đường
df2.plot(linewidth = '1',title='GIÁ BÁN TRUNG BÌNH BẤT ĐỘNG SẢN Ở TỪNG KHU VỰC QUA TỪNG NĂM THEO LOẠI HÌNH BẤT ĐỘNG SẢN')
plt.ylabel("Giá bán (USD)")


# Nhận xét:
# Ta có thể thấy rõ ràng, giá của nhà ở thì luôn cao hơn đáng kể so với giá của căn hộ và giá ở khu vực 1 luôn cao hơn ở khu vực 3 ngoại trừ vào năm 2007, giá của căn hộ ở khu vực 3 lại cao hơn.
# Giá cả của căn hộ luôn giao động trong khoảng từ 300000 đô đến hơn 450000 đô. Ngoại trừ vào khoảng thời gian từ 2007 đến 2010 có sự biến động mạnh thì nhìn chung giá của căn hộ có sự ổn định hơn, không thay đổi quá nhiều.
# Giá cả của nhà ở thì giao động trong khoảng từ 450000 đô đến hơn 800000 đô. Giá của nhà ở nhìn chung thường tăng qua các năm và giá ở năm 2007 so với năm 2019 thì có sẽ thấp hơn rõ ràng. 
# 

# ### Loại hình bất động sản theo phòng ngủ của từng khu vực
# 

# #### Số lượng bán bất động sản theo từng loại phòng ngủ của mỗi loại loại hình

# In[13]:


df_solution = df.pivot_table(index=['propertyType','bedrooms'], aggfunc='size').unstack()
df_solution


# In[14]:


s = df.value_counts(['propertyType','bedrooms']).sort_values(ascending=True).plot.barh(color='#76DF7D',edgecolor='#90EE90')

plt.title("SỐ LƯỢNG BÁN BẤT ĐỘNG SẢN THEO TỪNG LOẠI PHÒNG NGỦ CỦA MỖI LOẠI HÌNH BDS\n")
plt.xlabel("\n Sales",fontdict = font1)

for i in s.patches:
    xpos = i.get_width() + 50
    ypos = i.get_y()
    lbl = i.get_width()
    plt.text(xpos, ypos, lbl, fontsize=12)


# Nhận xét: Theo biểu đồ, số lượng loại house với 3 phòng ngủ là bán chạy nhất từ trước tới nay, đạt 11,281 căn và thấp nhất là loại unit 5 phòng ngủ, chỉ đạt 3 căn. Phần lớn doanh số đến từ loại house từ 3-5 phòng ngủ và loại unit với 2 phòng ngủ.

# #### Giá bán trung bình bất động sản tất cả các năm ở từng khu vực theo loại hình bất động sản và phòng ngủ

# In[22]:


# GIÁ BÁN TRUNG BÌNH BẤT ĐỘNG SẢN TẤT CẢ CÁC NĂM Ở TỪNG KHU VỰC THEO LOẠI HÌNH VÀ PHÒNG NGỦ
df1 = df
df1['type'] = "Region " + df1['region'].astype(str) + ": " + df1['propertyType'] 
df1 = df.drop(['datesold','propertyType'], axis ='columns')
df1=df1.groupby(['bedrooms','type']).mean().astype(int)
df2=df1.pivot_table(index='type', values='price', columns='bedrooms',fill_value=0)
df2.head()


# In[23]:


df2.plot(figsize=(20,8),kind='bar', title='GIÁ BÁN TRUNG BÌNH BẤT ĐỘNG SẢN TẤT CẢ CÁC NĂM Ở TỪNG KHU VỰC THEO LOẠI HÌNH VÀ PHÒNG NGỦ')
plt.ylabel("Giá bán (Trăm nghìn USD)")
plt.xlabel("Loại hình bất động sản theo khu vực")


#  Nhận xét: 
# - Nhìn vào biểu đồ, giá của nhà ở theo phòng ngủ có xu hướng cao hơn so với giá của căn hộ theo phòng ngủ và giá ở khu vực 1 luôn cao hơn ở khu vực 3.
# - Giá cả của căn hộ ở khu vực 1 và 3 đều có xu hướng tăng theo số lượng phòng tăng dần. Cụ thể giá ở căn hộ không có phòng ngủ sẽ thấp nhất và giá ở căn hộ có 5 phòng ngủ sẽ cao nhất.
#   ->Giá cả căn hộ tỷ lệ thuận với số lượng phòng ngủ trong căn hộ đó
# - Giá cả nhà ở của khu vực 1 và 3 có sự biến động nhẹ, đặc biệt là đối với nhà không có phòng ngủ. Giá nhà ở có 1 đến 5 phòng ngủ sẽ có chiều hướng tăng dần theo số lượng phòng ngủ, tương tự như giá cả của căn hộ.
# Tuy nhiên, giá nhà ở không có phòng ngủ sẽ nằm ở giữa giá của nhà có 3 và 4 phòng ngủ. Lí giải điều này có thể là do những người có điều kiện và sống một mình thường sẽ mua những ngôi nhà ở vị trí gần khu trung tâm thành phố với giá thuê mặt bằng cao để tiện cho việc sinh hoạt và làm việc hơn.

# ## Predictive Analysis (Time-series Forecasting)

# In[48]:


# time-series prediction packages

import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX # sarimax algorithm for actual predictions

import warnings
warnings.filterwarnings("ignore")  #Specify to ignore warning messages


# In[49]:


df = pd.read_csv('raw_sales.csv')


# ### Sales Forecast 

# #### Data Preprosessing

# In[50]:


df['datesold'] = pd.to_datetime(df['datesold'])
df['month'] = df['datesold'].dt.strftime('%Y-%m')

ts=df['month'].value_counts().sort_index(ascending=True)
ts #dang series


# In[51]:


ts = pd.DataFrame(ts).reset_index()
ts.columns = ['Month', 'Sales']
ts['Month'] = pd.to_datetime(ts['Month'], format = '%Y-%m-%d')


# In[52]:


ts.set_index(['Month'], inplace = True)
ts


# #### Check Stationarity

# In[20]:


ts.plot()


# In[ ]:


#Cấu trúc của mô hình SARIMA 
Seasonal Autoregressive Integrated Moving Average SARIMA(p,d,q)(P,D,Q)m

p: the lag order (number of lag observations included)
d: the degree of differencing needed for stationarity (number of times the data is differenced)
q: the order of the moving average
P: Seasonal autoregressive order.
D: Seasonal difference order.
Q: Seasonal moving average order.
m: The number of time steps for a single seasonal period.


# #### Build SARIMAX Model with exogenous variable

# In[53]:


# multiplicative seasonal component
result_mul = seasonal_decompose(ts['Sales'][-36:],   # 3 years
                                model='multiplicative', 
                                extrapolate_trend='freq')

seasonal_index = result_mul.seasonal[-12:].to_frame()
seasonal_index['month'] = pd.to_datetime(seasonal_index.index).month

# merge with the base data
ts['month'] = ts.index.month
new_ts = pd.merge(ts, seasonal_index, how='left', on='month')
new_ts.columns = ['value', 'month', 'seasonal_index']
new_ts.index = ts.index  # reassign the index.
new_ts


# In[54]:


import pmdarima as pm
sxmodel = pm.auto_arima(new_ts[['value']], exogenous=new_ts[['seasonal_index']],
                           start_p=1, start_q=1,
                           test='adf',
                           max_p=3, max_q=3, m=12,
                           start_P=0, seasonal= True,  
                           d=None, D=1, trace=True,
                           error_action='ignore',  
                           suppress_warnings=True, 
                           stepwise=True)

sxmodel.summary()


# In[25]:


sxmodel.plot_diagnostics(figsize=(12,8))
plt.show()


# Sai số dư dường như dao động xung quanh giá trị trung bình bằng 0 và có phương sai đồng nhất.
# Histogram plus estimated density plot: Đường KDE theo sát với đường N (0,1). Đây là một dấu hiệu tốt cho thấy phần dư được phân phối bình thường.
# Biểu đồ Q-Q: phân phối có thứ tự của phần dư (chấm xanh lam) tuân theo xu hướng tuyến tính của các mẫu được lấy từ phân phối chuẩn chuẩn với N (0, 1) 

# #### Predict the next 24 months

# In[27]:


n_periods = 24
fitted, confint = sxmodel.predict(n_periods=n_periods, 
                                  exogenous=np.tile(seasonal_index.values, 1).reshape(-1,1), 
                                  return_conf_int=True)

index_of_fc = pd.date_range(new_ts.index[-1], periods = n_periods, freq='MS')

# make series for plotting purpose
fitted_series = pd.Series(fitted, index=index_of_fc)
lower_series = pd.Series(confint[:, 0], index=index_of_fc)
upper_series = pd.Series(confint[:, 1], index=index_of_fc)

# Plot
plt.plot(new_ts['value'])
plt.plot(fitted_series, color='darkgreen')
plt.fill_between(lower_series.index, 
                 lower_series, 
                 upper_series, 
                 color='k', alpha=.15)

plt.title("SARIMAX Forecast - Number of House Sales")
plt.show()


# In[70]:


fitted_series.plot(figsize=(12,5))


# Biểu đồ dự đoán mang xu hướng và tính mùa của bộ dữ liệu 3 năm gần đây. Nhìn chung, số lượng bất động sản bán trong tương lai được dự đoán có xu hướng tăng so với 3 năm gần đây, đạt dỉnh vào các tháng 10 năm 2019, 2020 và giảm mạnh vào các tháng 12. Sau đó tăng mạnh và duy trì ổn định trong các tháng giữa năm.

# ### Price Forecasting

# #### Data Preprocessing

# In[55]:


# Xử lý dữ liệu để phù hợp cho việc trực quan hóa
df = df.drop(['bedrooms','propertyType','postcode'], axis ='columns')
tp= df.groupby(df['month']).mean().astype(int)


# In[56]:


tp.reset_index(drop=False, inplace=True)
tp


# In[57]:


tp['month'] = pd.to_datetime(tp.month)
tp = tp.set_index(tp.month)

tp.drop('month', axis = 1, inplace = True)
tp


# #### Check Stationarity

# In[32]:


tp.plot()


#  Xu hướng của chuỗi có xu hướng lên xuống 🡺 Chuỗi không dừng

# In[33]:


#Sử dụng phương pháp phân tích (decomposition method)
result = seasonal_decompose(tp, model='ad')
result.plot();


# Biểu đồ cho thấy dữ liệu có cả xu hướng và tính thời vụ. Điều đó có nghĩa là nó not stationary.

# In[34]:


#Kiểm tra thống kê bằng Dickey-Fuller test
result = adfuller(tp)
print('ADF result:', result[0])
print('p-value = ', result[1])
print('#Lags = ', result[2])
critical_values = result[4]
print('Number of observation used:', result[3])
for key, value, in critical_values.items():
  print("critical values (%s): %.3f" % (key, value))


# p-value > 0.05 và trị tuyệt đối của ADF statistic còn lớn hơn các Critical value 1%, 5% và 10% 
# 🡺 Chuỗi chưa dừng. Do đó, ta tiến hành biến đổi làm cho chuỗi có tính dừng

# #### Make series stationary & determine the d value

# In[35]:


#lấy sai phân của chuỗi
tp_diff = tp.diff()
tp_diff.dropna(inplace = True)
result = adfuller(tp_diff)
print('ADF result', result[0])
print('p-value = ', result[1])
print('#Lag = ', result[2])
critical_values = result[4]
print('Number of observation used:', result[3])
for key, value, in critical_values.items():
  print("critical values (%s): %.3f" % (key, value))


# In[36]:


pd.plotting.autocorrelation_plot(tp_diff)


# Chuỗi đã dừng. Như vậy d = 1

# #### Build ARIMA model

# In[37]:


####  Finding the order of differencing. 
plt.subplot(211)
plot_acf(tp_diff, ax=plt.gca())
plt.subplot(212)
plot_pacf(tp_diff, ax=plt.gca())
plt.show()


# #Dựa vào biểu đồ ACF để chọn bậc q cho MA
# Sau một độ trễ 1 lag nằm ngoài khoảng tin cậy, các giá trị giảm dần về 0
# và năm trong dãy màu xanh (nằm trong độ tin cậy 95%), nên ta có thể chọn q thuộc (0,1)
# 
# #Dựa vào biểu đồ của PACF để xác định p cho AR
# Ta thấy rằng sau sau một độ trễ 2 lags nằm ngoài khoảng tin cậy, các giá trị giảm dần về 0 và nằm trong dãy màu xanh (nằm trong độ tin cậy 95%). Nên ta có thể chọn p thuộc (0,2)

# In[ ]:


# Finding model parameters by grid search


# In[58]:


import itertools
p = d = q = range(3) #0,1,2
pdq = list(itertools.product(p, d, q))     


# In[59]:


AIC_df = pd.DataFrame({}, columns = ['param', 'AIC'])

for param in pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(tp, order = param, enforce_stationarity = False, enforce_invertibility = False)
            results = mod.fit()
            #print('ARIMA{}x{}-AIC:{}'.format(param, param_seasonal, results.aic))
            temp = pd.DataFrame([[param, results.aic]], columns = ['param', 'AIC'])
            AIC_df = AIC_df.append(temp, ignore_index = True)
            del temp
        except:
            continue


# In[60]:


min_aic = AIC_df.sort_values(by = 'AIC').iloc[0]    #Row with minimum AIC value
model = sm.tsa.statespace.SARIMAX(tp, order = min_aic.param, enforce_stationarity = False, enforce_invertibility = False)
results = model.fit()
print(results.summary())


# In[42]:


results.plot_diagnostics(figsize=(12,8))
plt.show()


# #### Forecasting price of next 24 months

# In[61]:


pred_uc = results.get_forecast(steps=24)    
pred_ci = pred_uc.conf_int()   
pred_ci


# In[62]:


#Take exponential function
pred_uc = pred_uc.predicted_mean
pred_uc


# In[84]:


#Plot original data prediction
ax = tp['2016':].plot(label='Observed')
pred_uc.plot(ax=ax, label='Forecast')
ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color='k', alpha=.25)
ax.set_xlabel('Month')
ax.set_ylabel('Price')
plt.legend(loc = 'upper left')
plt.title("ARIMA Forecast - Price of House Sales")
plt.show()


# In[69]:


pred_uc.plot(figsize=(12,5))

Nhìn chung giá bất động sản đang có xu hướng tăng và trong 24 tháng tới, giá bất động sản có thể tăng lên tới 641,633 vào tháng 08/2019 và có dấu hiệu giảm dần trong 4 tháng tiếp theo. Tới 01/2020 giá có xu hướng ổn định, giữ mức trung bình ở 640,600 trong những tháng còn lại. 