# Import Required Libraries

import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_player import st_player
import plotly.graph_objects as go
import plotly.figure_factory as ff




# Page setup configurations
st.set_page_config(
    page_title="Tseries youtube channel dashbord",
    page_icon=":bar_chart:",
    layout="wide"
    )




# # Hide menu ------------------
# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         #val {color: green;}
#         </style>
#         """
# st.markdown(hide_menu_style, unsafe_allow_html=True)





# Dataset load
@st.cache
def get_data_from_csv():
    df = pd.read_csv("data/clean_tseries_data.csv", lineterminator='\n')
    return df

df = get_data_from_csv()






# Sidebar settings
st.sidebar.header("Please Filter Here:")

year = st.sidebar.multiselect(
    "Select the year:",
    options=df["publishedYear"].unique(),
    default=df["publishedYear"].unique()
)


df = df.query(
    "publishedYear == @year"
)

st.title(":bar_chart: Tseries Youtube Channel Analysis")

st.markdown("""---""")




# Top KPI 
total_videos = int(len(df))
average_views = round(df['viewCount'].mean()/1000000, 2)
average_comments = round(df['commentCount'].mean()/1000, 2)
average_likes = round(df['likeCount'].mean()/1000, 2)
max_view_millions = round(df['viewCount'].max()/1000000, 2)

sum_duration_minutes = (df['durationSecs'].sum()/60)/len(df)
average_duration = round(sum_duration_minutes, 2)





# Start KPI display section ##################

# First Three columns
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Videos")
    st.markdown(f'<h4 style="color:#33ff33;">{total_videos}</h4>', unsafe_allow_html=True)

with middle_column:
    st.subheader("Average Duration")
    st.markdown(f'<h4 style="color:#33ff33;">{average_duration} Minutes</h4>', unsafe_allow_html=True)


with right_column:
    st.subheader("Max. Views")
    st.markdown(f'<h4 style="color:#33ff33;">{max_view_millions}M</h4>', unsafe_allow_html=True)




# Second Three columns
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Average Views")
    st.markdown(f'<h4 style="color:#33ff33;">{average_views}M</h4>', unsafe_allow_html=True)

with middle_column:
    st.subheader("Average Likes")
    st.markdown(f'<h4 style="color:#33ff33;">{average_likes}K</h4>', unsafe_allow_html=True)
   
with right_column:
    st.subheader("Average Comments")
    st.markdown(f'<h4 style="color:#33ff33;">{average_comments}K</h4>', unsafe_allow_html=True)
    

st.markdown("---")
# End KPI display section ##################






# Display highest views video
def max_view_video(df):
    
    con = df['viewCount'] == df["viewCount"].max()
    max_v = df[con]['video_id'].values[0]
    return max_v


st.subheader("1. Most Viewed Video")
st.markdown("---")
max_view = max_view_video(df)
st_player(f"https://youtu.be/{max_view}")
st.markdown("---")






# Display Sample Dataframe
st.subheader('2. Sample Dataframe of Tseries')
st.markdown("---")
df_sample = df[['mainTitle', 'viewCount', 'publishedAt', 'likeCount', 'commentCount', 'durationSecs', 'likeViewRatio', 'CommentViewRatio']].head(5)
st.table(df_sample)
st.markdown("---")






# Display Top 10 Most views Videos
st.subheader('3. Top 10 Most Viewed Videos')
st.markdown("---")

top_20_videos_by_views = (
    df.sort_values('viewCount', ascending=False)[['mainTitle', 'viewCount']][0:10]
)

fig = px.bar(
    top_20_videos_by_views,
    x = 'viewCount',
    y = 'mainTitle',
    orientation="h",
    color_discrete_sequence=["#0083B8"] * len(top_20_videos_by_views),
    template="plotly_white",
    width=900, height=600,
  
)

fig.update_layout(
    xaxis_title="Views counts",
    yaxis_title="",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=12,
    )
)
st.plotly_chart(fig)
st.markdown("---")






# Display Views by year line plot
st.subheader('4. Views by Year')
st.markdown("---")
fig = px.line(df, x="publishedAt", y="viewCount", width=900, height=500)
st.plotly_chart(fig)
st.markdown("---")





# Display Correlation of comment vs Views and Likes vs views
st.subheader('5. Comment VS Views and Likes Vs Views')
st.markdown("---")
col1, col2= st.columns(2)

with col1:
    fig = px.scatter(df, x="likeCount", y="viewCount", trendline="ols")
    st.plotly_chart(fig)

with col2:
    fig = px.scatter(df, x="commentCount", y="viewCount", trendline="ols")
    st.plotly_chart(fig)



# Footer

st.write('Copyright @ 2022 | [Noro Chalise](https://www.linkedin.com/in/norochalise/)')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


