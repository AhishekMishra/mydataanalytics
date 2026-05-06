import pandas as pd
import plotly.express as px
import streamlit as st
import time
from groq import Groq

# PAGE CONFIG

st.set_page_config(
    page_title='Data Analytics Portal',
    page_icon='📊',
    layout='wide'
)


# GROQ API SETUP

client = Groq(
    api_key="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"
)

# AI FUNCTION



def get_accurate_response(user_query, df):

    user_query_lower = user_query.lower()
    calc_context = ""

    try:

        numeric_cols = df.select_dtypes(include='number').columns

        if len(numeric_cols) > 0:

            col = numeric_cols[0]

            if (
                'lowest' in user_query_lower
                or 'minimum' in user_query_lower
                or 'sabse kam' in user_query_lower
            ):

                min_val = df[col].min()
                row = df[df[col] == min_val].iloc[0]

                calc_context = f'''
                Lowest value in {col} is {min_val}
                Row details: {row.to_dict()}
                '''

            elif (
                'highest' in user_query_lower
                or 'maximum' in user_query_lower
                or 'sabse zyada' in user_query_lower
            ):

                max_val = df[col].max()
                row = df[df[col] == max_val].iloc[0]

                calc_context = f'''
                Highest value in {col} is {max_val}
                Row details: {row.to_dict()}
                '''

    except:
        pass

    try:

        summary_data = df.describe(include='all').to_string()

    except:

        summary_data = "Summary not available"

    system_prompt = f'''
    You are a professional Data Analyst.

    Dataset Columns:
    {list(df.columns)}

    Dataset Shape:
    {df.shape}

    Dataset Summary:
    {summary_data}

    {calc_context}

    RULES:
    1. Reply in user's language.
    2. Keep answers short and accurate.
    3. Use provided calculations if available.
    4. Explain professionally.
    5. If data is insufficient, say so clearly.
    '''

    try:

        completion = client.chat.completions.create(
            model='llama-3.1-8b-instant',
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': user_query
                }
            ],
            temperature=0
        )

        return completion.choices[0].message.content

    except Exception as e:

        return f'AI Error: {str(e)}'


# SESSION STATE

if 'messages' not in st.session_state:
    st.session_state.messages = []


# SIDEBAR AI CHATBOT

with st.sidebar:

    st.title('🤖 AI Data Analyst')
    st.divider()

    chat_container = st.container(height=450)

    with chat_container:

        for msg in st.session_state.messages:

            with st.chat_message(msg['role']):
                st.markdown(msg['content'])


# MAIN TITLE

st.title(':rainbow[Data Analytics Portal]')
st.subheader(':red[Explore Data With Ease]', divider='rainbow')



# FILE UPLOADER

file = st.file_uploader(
    'Drop CSV or Excel File',
    type=['csv', 'xlsx']
)


# MAIN APPLICATION


if file is not None:

    # READ FILE

    try:

        if file.name.endswith('csv'):
            data = pd.read_csv(file)

        else:
            data = pd.read_excel(file)

    except Exception as e:

        st.error(f'File Error: {str(e)}')
        st.stop()


    # SHOW DATAFRAME
    

    st.dataframe(data, use_container_width=True)

    st.success('File Uploaded Successfully ✅')


   
    # AI CHAT INPUT
  

    user_prompt = st.sidebar.chat_input('Ask About Your Data...')

    if user_prompt:

        st.session_state.messages.append(
            {
                'role': 'user',
                'content': user_prompt
            }
        )

        response = get_accurate_response(user_prompt, data)

        st.session_state.messages.append(
            {
                'role': 'assistant',
                'content': response
            }
        )

        st.rerun()


    # BASIC INFORMATION
  

    st.subheader(
        ':rainbow[Basic Information of Dataset]',
        divider='rainbow'
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        'Summary',
        'Top & Bottom Rows',
        'Data Types',
        'Columns'
    ])


    # SUMMARY TAB
    

    with tab1:

        st.write(
            f'Dataset has {data.shape[0]} rows and {data.shape[1]} columns'
        )

        st.subheader('Statistical Summary')

        try:
            st.dataframe(data.describe(include='all'))
        except:
            st.warning('Summary not available for this dataset.')


    # TOP/BOTTOM ROWS TAB
   

    with tab2:

        st.subheader('Top Rows')

        top_rows = st.slider(
            'Select Top Rows',
            1,
            len(data),
            min(5, len(data)),
            key='top_slider'
        )

        st.dataframe(data.head(top_rows))

        st.subheader('Bottom Rows')

        bottom_rows = st.slider(
            'Select Bottom Rows',
            1,
            len(data),
            min(5, len(data)),
            key='bottom_slider'
        )

        st.dataframe(data.tail(bottom_rows))


    # DATA TYPES TAB

    with tab3:

        st.subheader('Data Types')

        dtypes_df = pd.DataFrame({
            'Column': data.columns,
            'Data Type': data.dtypes.astype(str)
        })

        st.dataframe(dtypes_df)


    # COLUMNS TAB

    with tab4:

        st.subheader('Column Names')

        st.write(list(data.columns))


    # VALUE COUNTS SECTION

    st.subheader(
        ':rainbow[Column Value Count Analysis]',
        divider='rainbow'
    )

    with st.expander('Value Count Analysis'):

        col1, col2 = st.columns(2)

        with col1:

            selected_column = st.selectbox(
                'Choose Column',
                options=list(data.columns)
            )

        with col2:

            top_values = st.number_input(
                'Top Values',
                min_value=1,
                value=10,
                step=1
            )

        if st.button('Generate Count'):

            result = (
                data[selected_column]
                .value_counts()
                .reset_index()
            )

            result.columns = [selected_column, 'Count']

            result = result.head(top_values)

            st.dataframe(result)

            st.subheader('Visualizations')

            # BAR CHART

            fig1 = px.bar(
                result,
                x=selected_column,
                y='Count',
                text='Count',
                template='plotly_white'
            )

            st.plotly_chart(fig1, use_container_width=True)


            # LINE CHART

            fig2 = px.line(
                result,
                x=selected_column,
                y='Count',
                text='Count',
                template='plotly_white'
            )

            st.plotly_chart(fig2, use_container_width=True)


            # PIE CHART

            fig3 = px.pie(
                result,
                names=selected_column,
                values='Count'
            )

            st.plotly_chart(fig3, use_container_width=True)


    # GROUP BY ANALYSIS
    
    st.subheader(
        ':rainbow[Group By Analysis]',
        divider='rainbow'
    )

    st.write(
        'Group your dataset and visualize insights easily.'
    )

    with st.expander('Group Your Data'):

        c1, c2, c3 = st.columns(3)

        with c1:

            group_cols = st.multiselect(
                'Choose Columns To Group By',
                options=list(data.columns)
            )

        with c2:

            operation_col = st.selectbox(
                'Choose Operation Column',
                options=list(data.columns)
            )

        with c3:

            operation = st.selectbox(
                'Choose Operation',
                ['sum', 'max', 'min', 'mean', 'median', 'count']
            )


        if group_cols:

            try:

                result = (
                    data.groupby(group_cols)
                    .agg(Result=(operation_col, operation))
                    .reset_index()
                )

                st.dataframe(result)

                st.subheader('Visualization')

                graph = st.selectbox(
                    'Choose Graph',
                    ['line', 'bar', 'scatter', 'pie', 'sunburst']
                )


                # LINE GRAPH

                if graph == 'line':

                    fig = px.line(
                        result,
                        x=result.columns[0],
                        y='Result',
                        markers=True
                    )

                    st.plotly_chart(fig, use_container_width=True)


                # BAR GRAPH

                elif graph == 'bar':

                    fig = px.bar(
                        result,
                        x=result.columns[0],
                        y='Result'
                    )

                    st.plotly_chart(fig, use_container_width=True)


                # SCATTER GRAPH

                elif graph == 'scatter':

                    fig = px.scatter(
                        result,
                        x=result.columns[0],
                        y='Result'
                    )

                    st.plotly_chart(fig, use_container_width=True)


                # PIE GRAPH

                elif graph == 'pie':

                    fig = px.pie(
                        result,
                        names=result.columns[0],
                        values='Result'
                    )

                    st.plotly_chart(fig, use_container_width=True)


                # SUNBURST GRAPH

                elif graph == 'sunburst':

                    path = st.multiselect(
                        'Choose Path Columns',
                        options=list(result.columns)
                    )

                    if len(path) == 0:
                        st.warning('Please choose at least one path column')

                    else:

                        fig = px.sunburst(
                            result,
                            path=path,
                            values='Result'
                        )

                        st.plotly_chart(fig, use_container_width=True)


            except Exception as e:

                st.error(f'GroupBy Error: {str(e)}')


else:

    st.info('Upload a CSV or Excel file to begin.')

