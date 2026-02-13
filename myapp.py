# import libraries
import pandas as pd
import plotly.express as px
import streamlit as st
 
st.set_page_config(
    page_title='Data Analytics Portal',
    page_icon='📊'
)
#title
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':red[Explore Data With Ease]',divider='rainbow')

file = st.file_uploader('Drop csv or excel file',type=['csv','xlsx'])
if(file!=None):
    if(file.name.endswith('csv')):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)   

    st.dataframe(data)
    st.info('File is successfully Uploaded',icon='🚨')

    st.subheader(':rainbow[Basic Information of The Dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4 =st.tabs(['Summary','Top & Bottom Rows','Data Types','Columns'])

    with tab1:
        st.write(f'There are{data.shape[0]} rows in dataset and {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical summary of the Dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows=st.slider('Number of rows you want',1,data.shape[0],key='topslider')
        st.dataframe(data.head(toprows))    
        st.subheader(':gray[Bottom Rows]')
        bottomrows=st.slider('Number of rows you want',1,data.shape[0],key='bottomslider')
        st.dataframe(data.tail(bottomrows))     
    with tab3:
        st.subheader(':grey[Data types of column]')
        st.dataframe(data.dtypes) 
    with tab4:
        st.subheader('Column Names in Dataset')
        st.dataframe(list(data.columns))

    st.subheader(':rainbow[Coloumn Values To Count]',divider='rainbow')
    with st.expander('Value Count'):
         col1,col2 = st.columns(2)
    with col1:
             column = st.selectbox('Choose Column name',options=list(data.columns))
    with col2: 
             toprows = st.number_input('Top Rows',min_value=1,step=1)


    count = st.button('count')
    if(count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader('Visualization',divider='gray')
            fig = px.bar(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.line(data_frame=result,x=column,y='count',text='count',template='plotly_white')
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)
    st.subheader(':rainbow[Group : Simplify your Data Analysis]',divider='rainbow')
    st.write('The groupby lest you summarize data by specific categories and groups')
    with st.expander('Group By your Columns'):
        col1,col2,col3 = st.columns(3)
        with col1:
             #st.markdown("<br>",unsafe_allow_html=True)#added by Abhishek
             groupby_cols = st.multiselect('Choose your Columns to Groupby',options = list(data.columns))
        with col2:
             operation_col = st.selectbox('Choose column for Operation',options=list(data.columns))
        with col3:
             operation = st.selectbox('Choose opertaion',options=['sum','max','min','mean','median','count'])  

        if(groupby_cols):
             result = data.groupby(groupby_cols).agg(
                 newcol=(operation_col,operation)
             ).reset_index()

             st.dataframe(result)

             st.subheader(':rainbow[Data visualization]',divider='rainbow')
             graphs= st.selectbox('choose your graphs',['line','bar','scatter','pie','sunburst'])
             if(graphs=='line'):
                  x_axis=st.selectbox('choose x axis',options=list(result.columns))
                  y_axis=st.selectbox('choose y axis',options=list(result.columns))
                  color=st.selectbox('color info',options= [None] +list(result.columns))
                  fig=px.line(data_frame=result,x=x_axis,y=y_axis,color=color,markers='o')
                  st.plotly_chart(fig)
             elif(graphs=='bar'):
                   x_axis=st.selectbox('choose x axis',options=list(result.columns))
                   y_axis=st.selectbox('choose y axis',options=list(result.columns))
                   color=st.selectbox('color info',options= [None] +list(result.columns))
                   facet_col=st.selectbox('column info',options=[None] +list(result.columns))
                   fig=px.bar(data_frame=result,x=x_axis,y=y_axis,color=color, facet_col=facet_col ,barmode='group',)
                   st.plotly_chart(fig)
             elif(graphs=='scatter'):
                   x_axis=st.selectbox('choose x axis',options=list(result.columns))
                   y_axis=st.selectbox('choose y axis',options=list(result.columns))
                   color=st.selectbox('color info',options= [None] +list(result.columns))
                   size=st.selectbox('size column',options=[None] +list(result.columns))
                   fig=px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color, size=size )
                   st.plotly_chart(fig)
             elif(graphs=='pie'):
                  values=st.selectbox('choose numerical values',options=list(result.columns))
                  names= st.selectbox('choose labels ',options=list(result.columns))     
                  fig=px.pie(data_frame=result,values=values,names=names)
                  st.plotly_chart(fig)
             elif(graphs=='sunburst'):
                  path=st.multiselect('choose your path',options=list(result.columns))
                  if len(path)==0:
                       st.warning("choose at least one")
                  else:     
                      fig=px.sunburst(data_frame=result,path=path,values='newcol')   
                      st.plotly_chart(fig)
 
                  
          
     
                  

                       







                     
                     
