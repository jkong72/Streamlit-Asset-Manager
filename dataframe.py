import streamlit as st
import numpy as np
import pandas as pd


# 전체 데이터
def df_app(df_set):
    
    # st.subheader ('전표')
    df_set.set_index('날짜', inplace=True)
    # st.dataframe(df_set, 650)

    st.sidebar.subheader('뽑아보기 (요약)')

    val = [df_set.columns[2], df_set.columns[4]]
    val_sel = st.sidebar.selectbox('어떤거 (기준)', val)

    menu = ['상위', '하위']
    dich = st.sidebar.selectbox('어느쪽 (분위)', options= menu) # dichotomy
    if dich == menu[0]:
        con = False
    else:
        con = True

    col = [df_set.columns[0], df_set.columns[1]]
    col_sel = st.sidebar.selectbox('어디서 (항목)', col)


    num_sel = st.sidebar.number_input('얼만큼 (개수)', min_value=0, value=5), # max_val을 수정해야 함.
    print(num_sel[0])

    # st.subheader (f'{val_sel} {dich} {num_sel[0]}개 {col_sel}에 대한 데이터')
    # st.dataframe(df_set.groupby(col_sel).sum().sort_values(val_sel, ascending=con).head(num_sel[0]), 400, 500)
    
    df1, df2 = st.columns(2)
    with df1:
        st.subheader ('전체 전표')
        st.dataframe(df_set, 650)
    with df2:
        st.subheader (f'{val_sel} {dich} {num_sel[0]}개 {col_sel}에 대한 데이터')
        st.dataframe(df_set.groupby(col_sel).sum().sort_values(val_sel, ascending=con).head(num_sel[0]))

        