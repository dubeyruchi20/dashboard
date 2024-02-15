
import streamlit as st 
import plotly.express as px
import pandas as pd 
import os
#import warnings
#warnings.filterwarnings('ignore')
#st.set_page_config(page_title="Superstore!!!",page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart :sample SuperStore EDA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)
f1 =st.file_uploader(":file_folder:upload a file",type=(["csv","txt","xlsx","xls"]))
if f1 is not None:
    filename=f1.name
    st.write(filename)
    df=pd.read_csv(filename,encoding="ISO-8859-1")
else:
    #os.chdir(r"C:\Users\User47\Desktop\Dashboard")  
    df= pd.read_csv("Sample - Superstore.csv",encoding="ISO-8859-1")
col1,col2=st.columns((2))    
df["Order Date"]=pd.to_datetime(df["Order Date"])
# getting the min and max date
startDate=pd.to_datetime(df["Order Date"]).min()
endDate=pd.to_datetime(df["Order Date"]).max()
with col1:
    date1=pd.to_datetime(st.date_input("Start Date",startDate))

with col2:
    date2=pd.to_datetime(st.date_input("End Date",endDate))  
df=df[(df["Order Date"]>=date1)& (df["Order Date"]<=date2)].copy() 

st.sidebar.header("Choose your filter:")
#create for region
region=st.sidebar.multiselect("Pick your Region",df["Region"].unique())
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)] 
# create for state
state=st.sidebar.multiselect("Pick the State",df2["State"].unique()) 
if not state:
    df3=df2.copy()      
else:
    df3=df2[df2["State"].isin(state)] 
 #create for city
city=st.sidebar.multiselect("Pick the City",df3["City"].unique())   
#filter the data based on region,state and City
if not region and not state and not city:
    filtered_df=df
elif not state and not city:
    filtered_df=df[df["Region"].isin(region)]
elif not region and not city: 
    filtered_df=df[df["State"].isin(state)] 
elif state and city:
    filtered_df=df3[df["State"].isin(state) & df3["City"].isin(city)] 
elif region and city:
    filtered_df=df3[df["Region"].isin(region) & df3["City"].isin(city)] 
elif region and state:
    filtered_df=df3[df["Region"].isin(region) & df3["State"].isin(city)] 
elif city:
    filtered_df=df3[df3["City"].isin(city)] 
else:
    filtered_df=df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]  

category_df=filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()  
with col1:
    st.subheader("Category wise Sales")
    fig=px.bar(category_df,x="Category",y="Sales",text= ['${:,.2f}'.format(x) for x in category_df["Sales"]],
               template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height=200)

with col2:
    st.subheader("Region wise Sales")
    fig= px.pie(filtered_df,values="Sales",names="Region",hole=0.5) 
    fig.update_traces(text=filtered_df["Region"],textposition="outside")  
    st.plotly_chart(fig,use_container_width=True) 
col1,col2=st.columns((2))
with col1:
    with st.expander("Category_viewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv=category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Category.csv",mime="text/csv",
                           help='Click here to download the data as a CSV file')
with col2:
    with st.expander("Region_viewData"):
        region=filtered_df.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv=region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data",data=csv,file_name="Region.csv",mime="text/csv",
                           help='Click here to download the data as a CSV file')       
# create a scatter plot
data1=px.scatter(filtered_df,x="Sales",y="Profit",size="Quantity") 
data1['layout'].update(title="Relationship between Sales and Profit using Scatter plot.",
                       titlefont=dict(size=20),xaxis=dict(title="Sales",titlefont=dict(size=15)),
                       yaxis=dict(title="Profit",titlefont=dict(size=19))),
st.plotly_chart(data1,use_container_width=True)   
with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))  

# download orignal Dataset
csv=df.to_csv(index=False).encode('utf-8')        
st.download_button('Download Data',data=csv,file_name="Data.csv",mime="text/csv")
