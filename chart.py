import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns
import plotly.express as px
##################################################

def chart_app(df_set, total_income) :
    st.subheader ('차트 옵션')
    menu = ['월별 매출', '기간별 성적', '점유율']
    ms = st.sidebar.selectbox('차트', menu)

    st.dataframe(df_set)
    st.dataframe(total_income)

    # menu 월별 매출
    if ms == menu[0]:
        st.line_chart(total_income)
        # fig1 = plt.figure()
        # plt.plot(total_income.iloc[:,0]) #총매출
        # plt.plot(total_income.iloc[:,1]) #총매입
        # plt.plot(total_income.iloc[:,2]) #순이익
        # plt.legend(total_income.columns)
        # st.pyplot(fig1)

    # menu 기간별 성적
    if ms == menu[1]:
        columns_kind = ['거래처', '품목']
        values_kind = ['매출', '거래량']

        col_sel = st.sidebar.radio('항목', columns_kind)
        
        all_acc = sorted(df_set['거래처'].unique())
        all_itm = sorted(df_set['품목'].unique())

        if col_sel == columns_kind[0]:
            col_set = st.multiselect(columns_kind[0], all_acc)
            index_set = columns_kind[0]
        elif col_sel == columns_kind[1]:
            col_set = st.multiselect(columns_kind[1], all_itm)
            index_set = columns_kind[1]
        
        val_sel = st.sidebar.radio('기준', values_kind)
        if val_sel == values_kind[0]:
            val_set = values_kind[0]
        if val_sel == values_kind[1]:
            val_set = values_kind[1]

        # col_set에는 선택한 값들이 리스트의 형태로 들어가 있다.
        # 이 값들에 해당하는 데이터만 가지고 오도록 df를 가공해야 한다.
        
        if len(col_set) != 0:
            df_set = df_set.set_index(index_set).loc[col_set]
            df_set.reset_index(inplace=True)
            st.dataframe(df_set)

        fig2 = px.line(df_set, x='날짜', y=val_set)
        st.plotly_chart(fig2)
        
        pass

    # menu 점유율(pie)
    if ms == menu[2]:
        pass




    pass

# 무슨 차트를 표현해야 하나??

# 0. 전체 매출과 이익을 월별로 그리는 그래프

# 1. 기간을 x축, 수치를 y축으로 하는 거래처or품목 그래프
# 기간은 월별로 하며 수치는 매출과 거래량을 사용한다. (라디오)
# 항목의 종류도 라디오로 선택 (라디오)
# 이 그래프는 기본적으로 가장 성적이 좋은 상위 3개와, 하위 3개를 뿌려주며
# 이용자가 원하는 항목만 볼 수도 있다 (멀티셀렉트)

# 2. 기간 매입