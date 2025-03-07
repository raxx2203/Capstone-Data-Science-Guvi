import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd 
import psycopg2
import plotly_express as px 
import json
import requests



#sql
mydb=psycopg2.connect(host="localhost",
                    user="postgres",
                    password="raveena",
                    database="phonepluse_data",
                    port="5432"

)

cursor=mydb.cursor()

#aggregate_insurance

cursor.execute(''' SELECT  *  from aggregated_transaction''')
mydb.commit()
table1=cursor.fetchall()
AGGREAGATED_INSURANCE=pd.DataFrame(table1,columns=("states","years","quarter","transaction_type","transaction_count","transaction_amount"))



#aggregate_transaction

cursor.execute(''' SELECT  *  from aggregated_transaction''')
mydb.commit()
table2=cursor.fetchall()
AGGREAGATED_TRANSACTION=pd.DataFrame(table2,columns=("states","years","quarter","transaction_type","transaction_count","transaction_amount"))


#aggregated_user

cursor.execute(''' SELECT  *  from aggregated_user''')
mydb.commit()
table3=cursor.fetchall()
AGGREAGATED_USER=pd.DataFrame(table3,columns=("states","years","quarter","brand","count","percentage"))


#map_insurance

cursor.execute(''' SELECT  *  from map_insurance''')
mydb.commit()
table4=cursor.fetchall()
MAP_INSURANCE=pd.DataFrame(table4,columns=("states","years","quarter",'hoverDataList',"transaction_count","transaction_amount"))



#map_transaction

cursor.execute(''' SELECT  *  from map_transaction''')
mydb.commit()
table5=cursor.fetchall()
MAP_TRANSACTION=pd.DataFrame(table5,columns=("states","years","quarter","District","transaction_count","transaction_amount"))



#map_user

cursor.execute(''' SELECT  *  from map_user''')
mydb.commit()
table6=cursor.fetchall()
MAP_USER=pd.DataFrame(table6,columns=("states","years","quarter","District","registeredUsers","appOpens"))



#top_insurance

cursor.execute(''' SELECT  *  from top_insurance''')
mydb.commit()
table7=cursor.fetchall()
TOP_INSURANCE=pd.DataFrame(table7,columns=("states","years","quarter", "pincodes","transaction_amount","transaction_count"))


#top_transaction


cursor.execute(''' SELECT  *  from top_transaction''')
mydb.commit()
table8=cursor.fetchall()
TOP_TRANSACTION=pd.DataFrame(table8,columns=("states","years","quarter", "pincodes","transaction_amount","transaction_count"))


#top_user

cursor.execute(''' SELECT  *  from top_user''')
mydb.commit()
table9=cursor.fetchall()
TOP_USER=pd.DataFrame(table9,columns=("states","years","quarter", "pincodes","registeredUsers"))






def Transaction_amount_count_y(df, year):
    plot = df[df["years"] == year]
    plot.reset_index(drop=True, inplace=True)

    graph = plot.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    graph.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        
        fig_amount = px.bar(graph, x="states", y="transaction_amount", title=f"{year} TRANSACTION_AMOUNT",
                        height=650, width=600)
        st.plotly_chart(fig_amount, use_container_width=False)


        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map = json.loads(response.content)
        states_name = []
        for feature in map["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1 = px.choropleth(graph, geojson=map, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_amount", color_continuous_scale="Rainbow",
                                    range_color=(graph["transaction_amount"].min(), graph["transaction_amount"].max()),
                                    hover_name="states", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
          fig_count = px.bar(graph, x="states", y="transaction_count", title=f"{year} TRANSACTION_COUNT",
                       color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
          st.plotly_chart(fig_count, use_container_width=False)


          fig_india_2 = px.choropleth(graph, geojson=map, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_count", color_continuous_scale="Rainbow",
                                    range_color=(graph["transaction_count"].min(), graph["transaction_count"].max()),
                                    hover_name="states", title=f"{year} TRANSACTION COUNT ", fitbounds="locations",
                                    height=600, width=600)
          fig_india_2.update_geos(visible=False)
          st.plotly_chart(fig_india_2)

    return plot


def Transaction_amount_count_x(df, quarter):

    plot = df[df["quarter"] == quarter]
    plot.reset_index(drop=True, inplace=True)

    graph = plot.groupby("states")[["transaction_count", "transaction_amount"]].sum()
    graph.reset_index(inplace=True)

    col1, col2 = st.columns(2)

    with col1:
        fig_amount = px.bar(graph, x="states", y="transaction_amount", title=f"{plot['quarter'].min()} year {quarter} TRANSACTION_AMOUNT",
                            height=650, width=600)
        st.plotly_chart(fig_amount)

        fig_count = px.bar(graph, x="states", y="transaction_count", title=f"{plot['quarter'].min()} year {quarter} TRANSACTION_COUNT",
                           color_discrete_sequence=px.colors.sequential.Aggrnyl, height=650, width=600)
        st.plotly_chart(fig_count)

    with col2:
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        map = json.loads(response.content)
        states_name = []
        for feature in map["features"]:
            states_name.append(feature["properties"]["ST_NM"])
        states_name.sort()

        fig_india_1 = px.choropleth(graph, geojson=map, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_amount", color_continuous_scale="Rainbow",
                                    range_color=(graph["transaction_amount"].min(), graph["transaction_amount"].max()),
                                    hover_name="states", title=f"{plot['quarter'].min()} YEAR {quarter} quarter ", fitbounds="locations",
                                    height=600, width=600)
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

        fig_india_2 = px.choropleth(graph, geojson=map, locations="states", featureidkey="properties.ST_NM",
                                    color="transaction_count", color_continuous_scale="Rainbow",
                                    range_color=(graph["transaction_count"].min(), graph["transaction_count"].max()),
                                    hover_name="states", title=f"{plot['quarter'].min()} YEAR {quarter} quarter ", fitbounds="locations",
                                    height=600, width=600)
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return plot
                        
def agree_tran(df, state): 
    
    plot = df[df["states"] == state]
    plot.reset_index(drop=True, inplace=True)

    graph = plot.groupby("transaction_type")[["transaction_count", "transaction_amount"]].sum()
    graph.reset_index(inplace=True)

    col1,col2=st.columns(2)

    with col1:

       fig_pie_1 = px.pie(data_frame=graph, names="transaction_type", values="transaction_amount",
                      width=600, title=f"{state.upper()} Transaction_amount", hole=0.5)
       st.plotly_chart(fig_pie_1)

    with col2:

     fig_pie_2 = px.pie(data_frame=graph, names="transaction_type", values="transaction_count",
                      width=600, title=f"{state.upper()} Transaction_count", hole=0.5)
     st.plotly_chart(fig_pie_2)


def agree_user(df, year): 
    
    plot = df[df["years"] == year]
    plot.reset_index(drop=True, inplace=True)

    graph =pd.DataFrame( plot.groupby("brand")[["count"]].sum())
    graph.reset_index(inplace=True)

    fig_pie_1 = px.bar(graph, x="brand", y="count",title=f"{year} BRAND AND TRANSACTION COUNT",
                      width=600, color_discrete_sequence=px.colors.sequential.Aggrnyl,hover_data="brand")
    st.plotly_chart(fig_pie_1)


    return plot


def agree_user1(df,quarter):
    
    plot = df[df["quarter"] == quarter]
    plot.reset_index(drop=True, inplace=True)
 
    graph =pd.DataFrame( plot.groupby("brand")[["count"]].sum())
    graph.reset_index(inplace=True)
    

    fig_pie_1 = px.bar(graph, x="brand", y="count",title=f"{quarter}  QUARTER BRAND AND TRANSACTION COUNT",
                      width=600, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig_pie_1)

    return plot


def agree_user2(df,state):

  plot=df[df["states"]== state]
  plot.reset_index(drop=True, inplace=True)

  fig_pie_1 = px.line(plot, x="brand", y="count",hover_data="percentage",title=f"{state.upper()} BRAND,TRANSACTION COUNT AND PERCENTAGE",
                      width=600, markers=True) 
  st.plotly_chart(fig_pie_1)
  
  return plot



def map_district(df, state): 
    
    plot = df[df["states"] == state]
    plot.reset_index(drop=True, inplace=True)

    graph = plot.groupby("hoverDataList")[["transaction_count", "transaction_amount"]].sum()
    graph.reset_index(inplace=True)
    

    fig_bar_1 = px.bar(graph,x="transaction_amount",y="hoverDataList",orientation="h",
                       title=f"{state.upper()} DISTRICT AND TRANSACTION_AMOUNT",color_discrete_sequence=px.colors.sequential.Magma,
                       height=600)
                       
    st.plotly_chart(fig_bar_1)

    fig_bar_2 = px.bar(graph,x="transaction_count",y="hoverDataList",orientation="h",
                       title=f"{state.upper()} DISTRICT AND TRANSACTION_COUNT",color_discrete_sequence=px.colors.sequential.Blues_r,
                     height=600)
    st.plotly_chart(fig_bar_2)

    return plot


#streamlit
st.set_page_config (
    page_title="PHONPE",
    page_icon="💳📱"
    )


st.markdown(
    """
    <h1 style='color: red;'>PHONEPULSE DATA VISUALIZATION</h1>
    """,
    unsafe_allow_html=True)
st.sidebar.markdown(
    """
    <p style='color: blue;'>Visualize The Page Above</p>
    """,
    unsafe_allow_html=True
)

selected= st.sidebar.selectbox("Select Application", ["HOME", "DATA EXPLORATION", "TOP CHARTS"])

# Display content based on the selected option
if selected == "HOME":
    st.title("Welcome to HOME")
    # Add content for the HOME section


elif selected == "DATA EXPLORATION":
    st.title("DATA EXPLORATION")
    
    # Custom tabs for the DATA EXPLORATION section
    tab1,tab2,tab3=st.tabs(["AGGREGATED ANALYSIS", "MAP ANALYSIS", "TOP ANALYSIS"])

    with tab1:
        method=st.selectbox("select the Method",["INSURANCE ANALYSIS","TRANSACTION ANALYSIS","USER ANALYSIS"])

        if method == "INSURANCE ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
               years=st.slider("select the year",AGGREAGATED_INSURANCE["years"].min(),AGGREAGATED_INSURANCE["years"].max(),AGGREAGATED_INSURANCE["years"].min())
            result=Transaction_amount_count_y(AGGREAGATED_INSURANCE,years)
            

            with col2:

                quarters=st.slider("select the quater",result["quarter"].min(),result["quarter"].max(),result["quarter"].min())

            Transaction_amount_count_x(result,quarters)



        elif method == "TRANSACTION ANALYSIS":
             
              col1,col2=st.columns(2)
              with col1:
               year1=st.slider("select the year",AGGREAGATED_TRANSACTION["years"].min(),AGGREAGATED_TRANSACTION["years"].max(),AGGREAGATED_TRANSACTION["years"].min())
              result1=Transaction_amount_count_y(AGGREAGATED_TRANSACTION,year1)
            
              col1,col2=st.columns(2)
              with col1:
                  states1=st.selectbox("select the states",result1["states"].unique())
              agree_tran(result1, states1)     


        elif method == "USER ANALYSIS":
             col1, col2 = st.columns(2)

             with col1:
               selected_year = st.slider("Select the Year", AGGREAGATED_USER["years"].min(),
                                  AGGREAGATED_USER["years"].max(), AGGREAGATED_USER["years"].min())
        
               result2 = agree_user(AGGREAGATED_USER, selected_year)

             with col2:
                 selected_quarter = st.slider("Select the Quarter", result2["quarter"].min(),
                                      result2["quarter"].max(), result2["quarter"].min())
        
                 aggregated_result = agree_user1(result2, selected_quarter)

             col1, col2 = st.columns(2)  
             with col1:
              selected_state = st.selectbox("Select the State", aggregated_result["states"].unique())

              agree_user2(aggregated_result, selected_state)


  

    with tab2:
        method=st.selectbox("select the Method",["MAP INSURANCE","MAP TRANSACTION"," MAP USER"])

        if method == "MAP INSURANCE":
           col1,col2=st.columns(2)
           with col1:
               year1=st.slider("select the year",MAP_INSURANCE["years"].min(),MAP_INSURANCE["years"].max(),MAP_INSURANCE["years"].min())
               map1=Transaction_amount_count_y(MAP_INSURANCE,year1)


               col1,col2=st.columns(2)
               with col1:
                  states1=st.selectbox("select the states",map1["states"].unique())
                  map_district(map1, states1)     
            
        
        elif method == "MAP TRANSACTION":
            pass
        elif method == "MAP USER":
            pass

        with tab3:
          method=st.selectbox("select the Method",[" TOP INSURANCE","TOP TRANSACTION"," TOP USER"])

          if method == " TOP INSURANCE ":
             pass
        
          if method == "TOP TRANSACTION":
             pass
          if method == "TOP USER":
             pass


elif selected == "TOP CHARTS":
    st.title("Top Charts")





          


