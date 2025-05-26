import streamlit as st
import pandas as pd
import plotly.express as px

# 웹앱 제목
st.title("Google Drive 데이터 Plotly 시각화")

# 데이터 읽기
url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"

@st.cache_data
def load_data():
    df = pd.read_csv(url)
    return df

df = load_data()
st.write("데이터 미리보기:")
st.dataframe(df)

# 시각화: 예를 들어 'x', 'y'라는 컬럼이 있다면
if 'x' in df.columns and 'y' in df.columns:
    fig = px.scatter(df, x='x', y='y', title="Plotly 산점도")
    st.plotly_chart(fig)
else:
    st.warning("시각화를 위해 필요한 'x'와 'y' 컬럼이 없습니다.")
