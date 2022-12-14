#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing files
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(
  page_title= 'Why best Cereal',
  page_icon= ':smiley:',
  initial_sidebar_state= 'expanded')
  
st.title("Welcome to my my Homework!")


df = pd.read_csv("/content/drive/MyDrive/MSBA325/cereal.csv")
df.head(2)

brands = {"A" : "American Home Food Products",
"G" : "General Mills",
"K" : "Kelloggs",
"N" : "Nabisco",
"P" : "Post",
"Q" : "Quaker Oats",
"R" : "Ralston Purina"
}
df.replace({"mfr": brands}, inplace=True)

types = {"C" : "Cold",
          "H" : "Hot"
}
df.replace({"type": types}, inplace=True)

df=df.rename(columns={'type':'Type','rating':'Rating',"sugars":"Sugars","calories":"Calories","fiber":"Fiber","vitamins":"Vitamins","mfr":"Brand"})


# logistics: changing page icon and setting title
st.write("The below dataset sums the rating of different cereal with their nutrition components")
st.write("These are the first five rows in my data:")

#Reading the data
if st.checkbox('Click for Expanded Data'):
    st.subheader('Expanded Data')
    st.write(df)


# page 1:

st.sidebar.markdown("# Discovery Phase :eye:")



st.header("Number of Observation per Brand")

Q_per_brand = df.groupby(['Brand'])['Brand'].count()
Q_per_brand=pd.DataFrame({'Brand':Q_per_brand.index, 'Count':Q_per_brand.values})


# Visual number 1 

fig = px.pie(Q_per_brand, values='Count', names='Brand', color='Brand')
st.plotly_chart(fig)

st.markdown('The above plot shows that the dataset does not have equal instances from each brand')

# Visual 2 
st.header("Different Nutrition Facts Across Brands")
# pivot table to get the mean of each the below nutrition facts across brands
nutrition_per_brand=df.pivot_table(values=['Calories','Fiber','Sugars','Vitamins'],index= "Brand", aggfunc=np.mean)
# bringing it back to Pd
nutrition_per_brand = pd.DataFrame(nutrition_per_brand.to_records())



# The used code only takes input as lists, thus I rearranged the data to lists
brands=nutrition_per_brand.Brand.tolist()
Calories_mn=nutrition_per_brand.Calories.tolist()
Fiber_mn=nutrition_per_brand.Fiber.tolist()
Sugars_mn=nutrition_per_brand.Sugars.tolist()
Vitamins_mn=nutrition_per_brand.Vitamins.tolist()

# Multiple subplot code
specs = [[{'type':'domain'}, {'type':'domain'}], [{'type':'domain'}, {'type':'domain'}]]
fig = make_subplots(rows=2, cols=2, specs=specs)
# Each line is a piechart
fig.add_trace(go.Pie(labels=brands, values=Calories_mn, title="Calories Across Brands"), 1, 1)
fig.add_trace(go.Pie(labels=brands, values= Fiber_mn, title='Fiber Across Brands'), 1, 2)
fig.add_trace(go.Pie(labels=brands, values= Sugars_mn, title='Sugars Across Brands'), 2, 1)
fig.add_trace(go.Pie(labels=brands, values= Vitamins_mn, title='Vitamins Across Brands'), 2, 2)
# Adding a title and deleting the percentages for clarity 
fig.update(layout_showlegend=True)
fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

fig.update_traces(textinfo='none')
fig = go.Figure(fig)
st.plotly_chart(fig)

st.markdown('The above plot shows the average nutrients across brands')



# Figure 3 



st.markdown("# Better Cereal to Better Business :money_mouth_face: ")
st.sidebar.markdown("# Business Insights :wink: ")


st.header("Ratings Across Different Types of Cereals")
fig = px.box(df,x='Type' ,y="Rating",title='Ratings Across Different Types of Cereals')
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=30, r=30, t=30, b=30))
fig.show()
st.plotly_chart(fig)


st.markdown('The above box-plot shows that on average people like hot cereal more than cold ones')


# Figure 4
st.header("Ranking and Calories Across Brands")
# pivot table to get the mean of rating, calories and fiber across different brands
rating_per_brand=df.pivot_table(values=["Rating",'Calories','Fiber'],index= "Brand", aggfunc=np.mean)
rating_per_brand = pd.DataFrame(rating_per_brand.to_records())

fig = px.bar(rating_per_brand, x='Brand', y='Rating',hover_data=['Calories', 'Fiber'], color='Calories',labels={'mfr':'Brand'},height=500)
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=40, r=40, t=40, b=40))
st.plotly_chart(fig)

st.markdown('The above plot shows that brands that have the most calories have lower rating')


# figure 5:


st.header('Ranking and Fibers Across Brands')
fig = px.bar(rating_per_brand, x='Brand', y='Rating',hover_data=['Calories', 'Fiber'], color='Fiber',
             labels={'mfr':'Brand'})
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=40, r=40, t=40, b=40))
st.plotly_chart(fig)

st.markdown('The above plot shows that brands that have the most fibers have higher rating')




st.header('Correlation Heatmap for nutrients and Rankings')
#Creates the Correlation Matrix
corr_matrix=df.corr()
### takes out only one side of the matrix to make it visually appealing 
mask=np.triu(np.ones_like(corr_matrix,dtype= bool))
rLT = corr_matrix.mask(mask)


heat = go.Heatmap(
    z = rLT,
    x = rLT.columns.values,
    y = rLT.columns.values,
    zmin = - 0.25, # Sets the lower bound of the color domain
    zmax = 1,
    xgap = 1, # Sets the horizontal gap (in pixels) between bricks
    ygap = 1,
    colorscale = px.colors.diverging.RdBu)





layout = go.Layout( 
    width=800, 
    height=600,
    xaxis_showgrid=False,
    yaxis_showgrid=False,
    yaxis_autorange='reversed'
)

fig=go.Figure(data=[heat], layout=layout)
st.plotly_chart(fig)


st.markdown('The above Correlation Matrix is very insightful. We can see that calories and brands hurt the rating. However, fiber and protein are boost ratings up')


# Setting a sidebar:
st.markdown("# Interactive Plots :wink:")
st.sidebar.markdown("# Time to Make It Interactive :wink:")

st.header('Filtering By Ratings and Calories')


df_container= st.container()


Menu_Items= ['Filter By Ratings', 'View All Data', 'Filter By Calories']
Menu_choice= st.sidebar.selectbox('Select the Option', Menu_Items)


if Menu_choice== 'View All Data':
    with df_container:   
        st.subheader("Full Data with all Ratings:")
        st.write(df)
 
elif Menu_choice== 'Filter By Ratings':
        st.header('Determine Rating Range:')
        range= st.slider('Slide & Pick', 0.0,100.0, (50.0,76.0))
   
        st.write(range)
        filtered= df[df['Rating'].between(range[0], range[1])]
        st.write(filtered)


elif Menu_choice== 'Filter By Calories':
        st.header('Determine Rating Range:')
        range= st.slider('Slide & Pick', 0.0,160.0, (50.0,76.0))
   
        st.write(range)
        filtered_cal= df[df['Calories'].between(range[0], range[1])]
        st.write(filtered_cal)

st.markdown('The above scroll works as a filtering criteria')


st.header('Average Rating per Brand')





Brand = rating_per_brand['Brand']
Brand_choice = st.sidebar.selectbox('Select The Brand:', Brand)
Rating = rating_per_brand["Rating"].loc[rating_per_brand["Brand"] == Brand_choice]
st.write('Averge Rating of the chosen brand is:', Rating)

st.markdown('This helps us knowing the average rating by brand simply by zooming in to the brand. ')

st.header('Bubble Plot for Brands, Sugars, Ratings and Fiber')

fig = px.scatter(df[df['Brand']==Brand_choice],x='Sugars',y='Rating',size='Fiber', color="Brand")


st.plotly_chart(fig)
st.markdown('It is clear that larger bubbles score higher. This means cereal rich in fiber. Also, there is a negative slope. This shows the negative impact of sugars on the rating ')

st.markdown('Kindly note that American Home Food Products have only one entry. Please try another company to see the visualization ')


st.sidebar.markdown("Homework Done By Bashar Salha")


# In[ ]:




