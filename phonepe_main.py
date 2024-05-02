
###------- STREAMLIT UI
import json
import pandas as pd
import pymysql
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image
import numpy as np
import requests

#password = 'your db password'

st.set_page_config(
    page_title="Phonepe Project | By Anitha",
    page_icon=":shark:",
    layout="wide",  # wide
    initial_sidebar_state="auto"
)


#https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson
db_conn = pymysql.connect(
             host='localhost',
             user='root',
             password='xxx',
             database= "phonepe_db")
    
cursor_obj = db_conn.cursor()
selected = option_menu(None,
                       options=["HOME", "EXPLORE DATA",
                                "INSIGHTS","ABOUT"],
                       icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                       default_index=0,
                       orientation="horizontal",
                       styles={"container": {"width": "100%"},
                               "icon": {"color": "black", "font-size": "22px"},
                               "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px","--hover-color": "lightgreen"},
                               "nav-link-selected": {"background-color": "#6F36AD"}})

#-----> HOME
if selected == "HOME":
    col1, col2, = st.columns(2)
    col1.image(Image.open("C:/Users/phonepe_proj/csv_files/cover1.jpg"), width=650)
    with col1:
        st.markdown("#### PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer.")
        st.markdown("#### The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.markdown("#### India with 89.5 million digital transactions in the year 2022 has topped the list of five countries in digital payments, according to data from MyGovIndia")
    with col2:
        st.video("C:/Users/phonepe_proj/csv_files/pulse-video.mp4")
        
    st.write("<h4 style='color:red'>STEPS TO PROCEED:</h4>", unsafe_allow_html=True)
    st.markdown("##### 1.EXPLORE DATA -> Analysis and Top categories of States, District, Transaction, User using plotly for Phonepe Data")


#-----> EXPLORE
if selected == "EXPLORE DATA":
    st.write("<h3 style='color:black'>Analysis done based on States, Year, Transaction, User</h3>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["TRANSACTION","USER"])
    st.write("")
    with tab1: #Transaction
        col1, col2, col3 = st.columns(3)
        with col1:
            in_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_tr_yr')
        with col2:
            in_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_tr_qtr')
        with col3:
            in_tr_tr_typ = st.selectbox('**Select Transaction type**',
                                        ('Recharge & bill payments', 'Peer-to-peer payments',
                                         'Merchant payments', 'Financial Services', 'Others'), key='in_tr_tr_typ')
        # --bar chart query
        cursor_obj.execute(
            f"SELECT State, Transaction_amount FROM agg_trans WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
        tr_result = cursor_obj.fetchall()
        df_result = pd.DataFrame(np.array(tr_result), columns=['State', 'Transaction_amount'])
        df_bar_result = df_result.set_index(pd.Index(range(1, len(df_result) + 1)))

        # --table query
        cursor_obj.execute(
            f"SELECT State, Transaction_count, Transaction_amount FROM agg_trans WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
        tab_result = cursor_obj.fetchall()
        df_tab_result = pd.DataFrame(np.array(tab_result), columns=['State', 'Transaction_count', 'Transaction_amount'])
        df_tab_result1 = df_tab_result.set_index(pd.Index(range(1, len(df_tab_result) + 1)))

        # --Total Amount table query
        cursor_obj.execute(
            f"SELECT SUM(Transaction_amount),SUM(Transaction_count) FROM agg_trans WHERE Year = '{in_tr_yr}' AND Quarter = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
        am_result = cursor_obj.fetchall()
        df_am_result = pd.DataFrame(np.array(am_result), columns=['Total Amount','Total Count'])
        

        # GEO VISUALISATION
        df_result.drop(columns=['State'], inplace=True)
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names_tra.sort()
        df_state_names_tra = pd.DataFrame({'State': state_names_tra})
        df_state_names_tra['Transaction_amount'] = df_result
        df_state_names_tra.to_csv('C:/Users/phonepe_proj/csv_files/State_trans.csv', index=False)
        df_tra = pd.read_csv('C:/Users/phonepe_proj/csv_files/State_trans.csv')
        fig_tra = px.choropleth(
            df_tra,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',
            color_continuous_scale='thermal', title='State Vs Transaction Amount')
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), title_font_color='green', height=800)
        st.plotly_chart(fig_tra, use_container_width=True)

        # --Bar chart  
        df_bar_result['State'] = df_bar_result['State'].astype(str)
        df_bar_result['Transaction_amount'] = df_bar_result['Transaction_amount'].astype(float)
        df_bar_result_fig = px.bar(df_bar_result, x='State', y='Transaction_amount',
                                            color='Transaction_amount', color_continuous_scale='thermal',
                                            title='Transaction Analysis Chart', height=700, )
        df_bar_result_fig.update_layout(title_font=dict(size=33), title_font_color='green')
        st.plotly_chart(df_bar_result_fig, use_container_width=True)
        
        

        # ---Table 
        col4, col5 = st.columns(2)
        with col4:
            st.write("<span style='color: green; font-size: 24px;'>Transaction Analysis</span>", unsafe_allow_html=True)
            st.dataframe(df_tab_result1)
        with col5:
            st.write("<span style='color: green; font-size: 24px;'>Amount & Count</span>", unsafe_allow_html=True)
            st.dataframe(df_am_result)
    with tab2: # USER TAB
        col1, col2 = st.columns(2)
        with col1:
            in_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_us_yr')
        with col2:
            in_us_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_us_qtr')
        
        # User Bar chart query
        cursor_obj.execute(f"SELECT State, SUM(Count) FROM agg_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY State;")
        in_us_tab_qry_rslt = cursor_obj.fetchall()
        df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=['State', 'User Count'])
        df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt) + 1)))

        # User table query
        cursor_obj.execute(f"SELECT SUM(Count) FROM agg_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}';")
        in_us_co_qry_rslt = cursor_obj.fetchall()
        df_in_us_co_qry_rslt = pd.DataFrame(np.array(in_us_co_qry_rslt), columns=['Total'])
        
        #--- GEO VISUALIZATION FOR USER
        df_in_us_tab_qry_rslt.drop(columns=['State'], inplace=True)
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data2 = json.loads(response.content)
        state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
        state_names_use.sort()
        df_state_names_use = pd.DataFrame({'State': state_names_use})
        df_state_names_use['User Count'] = df_in_us_tab_qry_rslt
        df_state_names_use.to_csv('C:/Users/phonepe_proj/csv_files/State_trans.csv', index=False)
        df_use = pd.read_csv('C:/Users/phonepe_proj/csv_files/State_trans.csv')
        fig_use = px.choropleth(
            df_use,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM', locations='State', color='User Count',
            color_continuous_scale='thermal', title='User Analysis')
        fig_use.update_geos(fitbounds="locations", visible=False)
        fig_use.update_layout(title_font=dict(size=33), title_font_color='#AD71EF', height=800)
        st.plotly_chart(fig_use, use_container_width=True)

        # ---- User Bar chart 
        df_in_us_tab_qry_rslt1['State'] = df_in_us_tab_qry_rslt1['State'].astype(str)
        df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)
        df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1, x='State', y='User Count', color='User Count',
                                            color_continuous_scale='thermal', title='User Analysis Chart',
                                            height=700, )
        df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33), title_font_color='#AD71EF')
        st.plotly_chart(df_in_us_tab_qry_rslt1_fig, use_container_width=True)
        col3, col4 = st.columns(2)
        with col3:
            st.write("<span style='color: black; font-size: 24px;'>User Analysis</span>", unsafe_allow_html=True)
            st.dataframe(df_in_us_tab_qry_rslt1)
        with col4:
            st.write("<span style='color: black; font-size: 24px;'>Total User Count</span>", unsafe_allow_html=True)

            st.dataframe(df_in_us_co_qry_rslt)
        
    
# -- INSIGHTS MENU

if selected == "INSIGHTS":
    st.write("<h3 style='color:green'>1. Insights for Top Categories</h3>", unsafe_allow_html=True)
    st.write(
    """
    <style>
        .stSelectbox label {
            color: black;
            font-size: 20px;
        }
        .stSlider label {
            color: black;
            font-size: 18px;
        }
    </style>
    """
    , unsafe_allow_html=True
)
    Type = st.selectbox("* Select Type", ("Transactions", "Users"))
    st.write("")
    colum1,colum2= st.columns([1,1],gap="medium")
    with colum1:
        Year = st.slider("* Select Year", min_value=2018, max_value=2022)
    with colum2:
        Quarter = st.slider("* Select Quarter", min_value=1, max_value=4)
    
    # -- TRANS
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="medium")
        
        with col1:
            st.write("<h3 style='color:green'>TOP 10 State</h3>", unsafe_allow_html=True)
            cursor_obj.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(cursor_obj.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.write("<h3 style='color:green'>TOP 10 District</h3>", unsafe_allow_html=True)
            cursor_obj.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(cursor_obj.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.write("<h3 style='color:green'>TOP 10 Pincode</h3>", unsafe_allow_html=True)
            cursor_obj.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(cursor_obj.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
    # - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([1,1,1,1],gap="small")
        
        with col1:
            st.write("<h3 style='color:green'>TOP 10 Brands</h3>", unsafe_allow_html=True)
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                cursor_obj.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(cursor_obj.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.write("<h3 style='color:green'>TOP 10 District</h3>", unsafe_allow_html=True)
            cursor_obj.execute(f"select district, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor_obj.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.write("<h3 style='color:green'>TOP 10 States</h3>", unsafe_allow_html=True)
            cursor_obj.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor_obj.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.write("<h3 style='color:green'>TOP 10 Pincode</h3>", unsafe_allow_html=True)
            cursor_obj.execute(f"select Pincode, sum(Registered_users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(cursor_obj.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
    st.write("<h3 style='color:green'>2. Insights for Least Categories::</h3>", unsafe_allow_html=True)
    options = ["--select--",
               "1.Least 10 states based on year and amount of transaction",
               "2.Least 10 States and Districts based on Registered Users",
               "3.Least 10 Districts based on the Transaction Amount",
               "4.Least 10 Districts based on the Transaction count"]
    select = st.selectbox("",options)
    
    if select == "1.Least 10 states based on year and amount of transaction":
        cursor_obj.execute(
            "SELECT DISTINCT State,Year, SUM(Transaction_amount) as Total FROM top_trans GROUP BY State, Year ORDER BY Total ASC LIMIT 10");
        data = cursor_obj.fetchall()
        columns = ['States', 'Year', 'Transaction_amount']
        df = pd.DataFrame(data, columns=columns, index=range(1,len(data)+1))
        fig = px.bar(df, x='States', y='Transaction_amount', width=700, color="Year",
                     title="Least 10 states Vs transaction")
        st.plotly_chart(fig,use_container_width=True)
    elif select == "2.Least 10 States and Districts based on Registered Users":
        cursor_obj.execute("SELECT DISTINCT State, Pincode, SUM(Registered_users) AS Users FROM top_user GROUP BY State, Pincode ORDER BY Users ASC LIMIT 10");
        data = cursor_obj.fetchall()
        columns = ['State', 'Pincode', 'Registered_users']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        fig = px.bar(df, x='State', y='Registered_users', width=700, color="Pincode",
                     title="Least 10 States Vs Registered Users")
        st.plotly_chart(fig,use_container_width=True)
    elif select == "3.Least 10 Districts based on the Transaction Amount":
        cursor_obj.execute(
            "SELECT DISTINCT State,District,SUM(Amount) AS Total FROM map_trans GROUP BY State, District ORDER BY Total ASC LIMIT 10");
        data = cursor_obj.fetchall()
        columns = ['States', 'District', 'Amount']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        fig = px.bar(df, x="District", y="Amount", width=700, color="States",
                     title="Least 10 Districts  Vs Transaction Amount")
        st.plotly_chart(fig,use_container_width=True)    
    elif select == "4.Least 10 Districts based on the Transaction count":
        cursor_obj.execute(
            "SELECT DISTINCT State ,District,SUM(Count) AS Counts FROM map_trans GROUP BY State ,District ORDER BY Counts ASC LIMIT 10");
        data = cursor_obj.fetchall()
        columns = ['States', 'District', 'Counts']
        df = pd.DataFrame(data, columns=columns, index=range(1, len(data) + 1))
        fig = px.bar(df, x="District", y="Counts", width=700, color="States",
                     title="Least 10 Districts  Vs Transaction Amount")
        st.plotly_chart(fig,use_container_width=True)    
           

#-- ABOUT MENU
if selected == "ABOUT":
    col1,col2 = st.columns([1,1.5],gap="small")
    with col1:
        im = Image.open("C:/Users/phonepe_proj/csv_files/PhonePe_beat.jpg")
        st.image(im)
    with col2:
        st.write("<span style='color: blue; font-size: 24px;'>PHONEPE PULSE DATA VISUALIZATION AND EXPLORATION</span>", unsafe_allow_html=True)
        st.markdown("##### > PhonePe Pulse is a feature offered by the Indian digital payments platform called PhonePe.PhonePe Pulse provides users with insights and trends related to their digital transactions and usage patterns on the PhonePe app.")
        st.markdown("##### > Data visualization refers to the graphical representation of data using charts, graphs, and other visual elements to facilitate understanding and analysis in a visually appealing manner.")
        st.markdown("##### > The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.")
        st.write("<span style='color: blue; font-size: 24px;'>[Done by] : ANITHA VIKRAM</span>", unsafe_allow_html=True)
        st.markdown("## [Github --> Project Link](https://github.com/Anita-91/Phonepe_Pulse_Data_Visualization.git)")
        st.markdown("[Inspired from](https://www.phonepe.com/pulse/)")
        #st.markdown("[LinkedIn](link here)")
    