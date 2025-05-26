import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Plotly 시각화 앱", layout="wide")
st.title("📊 Google Drive CSV 데이터 Plotly 시각화 앱")

# 데이터 로딩
url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(url, encoding='utf-8')  # 필요시 'cp949'로 변경
        return df
    except Exception as e:
        st.error(f"데이터 로딩 실패: {e}")
        return None

df = load_data()

if df is not None:
    st.subheader("🔍 데이터 미리보기")
    st.dataframe(df, use_container_width=True)

    # 컬럼 자동 분류
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_cols = df.columns.tolist()

    st.sidebar.header("🛠️ 시각화 설정")

    chart_type = st.sidebar.selectbox("그래프 유형", ["산점도", "선 그래프", "막대 그래프"])
    x_axis = st.sidebar.selectbox("X축", all_cols)
    y_axis = st.sidebar.selectbox("Y축", numeric_cols)

    color_col = st.sidebar.selectbox("색상 구분 컬럼 (선택)", [None] + all_cols)

    # 결측치 처리
    if df[[x_axis, y_axis]].isnull().any().any():
        st.warning("⚠️ 선택된 컬럼에 결측치가 포함되어 있어 자동 제거됩니다.")
        df = df.dropna(subset=[x_axis, y_axis])

    # 시각화
    if chart_type == "산점도":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_col, title=f"{x_axis} vs {y_axis} 산점도")
    elif chart_type == "선 그래프":
        fig = px.line(df, x=x_axis, y=y_axis, color=color_col, title=f"{x_axis} vs {y_axis} 선 그래프")
    elif chart_type == "막대 그래프":
        fig = px.bar(df, x=x_axis, y=y_axis, color=color_col, title=f"{x_axis} vs {y_axis} 막대 그래프")

    st.plotly_chart(fig, use_container_width=True)

    # 다운로드 기능
    st.download_button(
        label="📥 데이터 다운로드 (CSV)",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='data.csv',
        mime='text/csv'
    )
else:
    st.stop()
