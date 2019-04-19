import pandas as pd
import numpy as np
import warnings
warnings.simplefilter('ignore')
# %matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
from pylab import rcParams
#from plotly.offline import iplot
rcParams['figure.figsize'] = 8, 5
data = pd.read_csv('data/video_games_sales.csv')
# data.info()
data = data.dropna()
# data.info()
data['User_Score'] = data.User_Score.astype('float64')
data['Year_of_Release'] = data.Year_of_Release.astype('int64')
data['User_Count'] = data.User_Count.astype('int64')
data['Critic_Count'] = data.Critic_Count.astype('int64')
useful_cols = ['Name', 'Platform', 'Year_of_Release', 'Genre', 
               'Global_Sales', 'Critic_Score', 'Critic_Count',
               'User_Score', 'User_Count', 'Rating'
              ]
print(data[useful_cols].head())
sales_data = data[[x for x in data.columns if 'Sales' in x] + ['Year_of_Release']]
#sales_data.groupby('Year_of_Release').sum().iplot
plt.plot(sales_data.groupby('Year_of_Release').sum())
plt.show()
cols = ['Global_Sales', 'Critic_Score', 'Critic_Count', 'User_Score', 'User_Count']
sns_plot = sns.pairplot(data[cols])
plt.show()
sns_plot = sns.distplot(data.Critic_Score)
plt.show()
cols = ['Critic_Score', 'User_Score']
sns_plot = sns.jointplot(data.Critic_Score, data.User_Score)
plt.show()
top_platforms = data.Platform.value_counts().sort_values(ascending = False).head(5).index.values
sns_plot = sns.boxplot(y="Platform", x="Critic_Score", data=data[data.Platform.isin(top_platforms)], orient="h")
plt.show()
platform_genre_sales = data.pivot_table(
                        index='Platform', 
                        columns='Genre', 
                        values='Global_Sales', 
                        aggfunc=sum).fillna(0).applymap(float)
sns_plot = sns.heatmap(platform_genre_sales, annot=True, fmt=".1f", linewidths=.5)
plt.show()
