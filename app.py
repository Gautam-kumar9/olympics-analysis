import streamlit as st
import pandas as pd
from matplotlib.pyplot import autoscale

import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
# from helper import medal_tally
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://tse1.mm.bing.net/th?id=OIP.dTvYWFiuSMkD-anpkDuQPQHaEK&pid=Api&P=0&h=180')
df = pd.read_csv('athlete_events.csv')
df_region = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,df_region)
user_menu = st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)
# st.dataframe(df)
# st.sidebar.title("Olympics Analysis")
if user_menu =='Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select year",years)
    selected_country = st.sidebar.selectbox("Select country",country)

    medal_tally = helper.fetch_mdeal_tally(df,selected_year,selected_country)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title("Overall Tally")
    if selected_country == 'Overall' and selected_year != 'Overall':
        st.title("Medal Tally in "+str(selected_year)+" Olympics")
    if selected_country != 'Overall' and selected_year == 'Overall':
        st.title(selected_country + " Overall Performance")
    if selected_country != 'Overall' and selected_year != 'Overall':
        st.title(selected_country + " Performance in "+str(selected_year)+" Olympics")
    st.table(medal_tally)


if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)


    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Athletes")
        st.title(athletes)
    with col3:
        st.header("Nations")
        st.title(nations)
    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nation Over the Year")
    st.plotly_chart(fig)


    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events Over the Year")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title("Athletes Over the Year")
    st.plotly_chart(fig)

    st.title("No. of Events over the time(Every Sports)")
    fig,ax = plt.subplots(figsize = (20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)



if user_menu == 'Country-wise Analysis':

    st.sidebar.title('Country Wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+" Medal Tally over the Years")
    st.plotly_chart(fig)


    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot = True)
    st.title(selected_country + " Excels in the following Sports")
    st.pyplot(fig)

    st.title("Top 10 Athletes of "+selected_country)
    top10_df = helper.most_successful_country(df,selected_country)
    st.table(top10_df)


if user_menu == 'Athlete wise Analysis':
    ath_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = ath_df['Age'].dropna()
    x2 = ath_df[ath_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = ath_df[ath_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = ath_df[ath_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = ath_df[ath_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age with respect to Sport(Gold Medalist)")
    st.plotly_chart(fig)


    for sport in famous_sports:
        temp_df = ath_df[ath_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age with respect to Sport(Silver Medalist)")
    st.plotly_chart(fig)
    st.title("Height Vs Weight")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x='Weight', y='Height', data=temp_df,hue = 'Medal',style='Sex',s=60)

    st.pyplot(fig)

    st.title("Men Vs Women participation over the Years")
    final = helper.men_v_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)

    st.plotly_chart(fig)
# Custom CSS to set a background image
def set_background_image(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

