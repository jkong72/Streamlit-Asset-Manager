import streamlit as st
import numpy as np
import pandas as pd


# 전체 데이터
def df_app(df_set, start_date, end_date):
    
    # st.subheader ('전표')
    df_set.set_index('날짜', inplace=True)

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

    # st.subheader (f'{val_sel} {dich} {num_sel[0]}개 {col_sel}에 대한 데이터')
    # st.dataframe(df_set.groupby(col_sel).sum().sort_values(val_sel, ascending=con).head(num_sel[0]), 400, 500)
    
    # 단위 구분 쉼표. 정수 자료형을 잃어버리므로 반드시 표시 직전에 수행
    df_set['거래량']
    df_set['단가']
    df_set['매출']

    # df_set['거래량'] = df_set.거래량.apply(lambda x: "{:,}".format(x))
    # df_set['단가'] = df_set.단가.apply(lambda x: "{:,}".format(x))
    # df_set['매출'] = df_set.매출.apply(lambda x: "{:,}".format(x))

    # 실제 표시
    df1, df2 = st.columns(2)
    with df1:
        st.subheader (f'{start_date} 부터 {end_date} 간의')
        st.markdown ('### 총 매출')
        total_sales = format (df_set['매출'].sum(), ',d')
        st.markdown (f'#### {total_sales} ₩')
        
        st.markdown("""---""")
        st.markdown ('### 거래량')
        total_trade = format (df_set['거래량'].sum(), ',d')
        st.markdown (f'#### {total_trade} ₩')
        
    with df2:
        st.subheader (f'{val_sel} {dich} {num_sel[0]}개 {col_sel}에 대한 데이터')
        df_summary = df_set.groupby(col_sel).sum().sort_values(val_sel, ascending=con).head(num_sel[0])
        df_summary['단가'] = df_summary.단가.apply(lambda x: "{:,}".format(x))+' ₩'
        df_summary['매출'] = df_summary.매출.apply(lambda x: "{:,}".format(x))+' ₩'
        st.dataframe(df_summary)

    st.markdown("""---""")
    st.subheader ('전체 전표')
    df_set['단가'] = df_set.단가.apply(lambda x: "{:,}".format(x))+' ₩'
    df_set['매출'] = df_set.매출.apply(lambda x: "{:,}".format(x))+' ₩'
    st.dataframe(df_set, width=650)