import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
##################################################

def chart_app(df_set, df_total) :        
    menu = ['월별 매출', '기간별 성적', '점유율']
    ms = st.sidebar.selectbox('차트', menu)

    st.subheader ('차트 옵션')
    st.write ('만약 원하는 옵션이 없다면 전체 범위를 확인해 보시기 바랍니다.')
    columns_kind = ['거래처', '품목']
    values_kind = ['매출', '거래량']

    col_sel = st.sidebar.radio('항목', columns_kind)
    
    all_acc = sorted(df_set['거래처'].unique())
    all_itm = sorted(df_set['품목'].unique())

    if col_sel == columns_kind[0]: # 거래처
        col_set = st.multiselect(columns_kind[0], all_acc)
        index_set = columns_kind[0]
    elif col_sel == columns_kind[1]: # 품목
        col_set = st.multiselect(columns_kind[1], all_itm)
        index_set = columns_kind[1]
    
    val_sel = st.sidebar.radio('기준', values_kind)
    if val_sel == values_kind[0]: # 매출
        val_set = values_kind[0]
    if val_sel == values_kind[1]: # 거래량
        val_set = values_kind[1]

    # menu 월별 매출
    if ms == menu[0]:

        # 연월 처리
        df_total['날짜'] = pd.to_datetime(df_total['날짜'])
        df_total['연월'] = df_total['날짜'].dt.strftime('%Y''-''%m')

        # 매입매출 구분
        df_total['isbuy'] = df_total['거래처'] == '매입'

        df_buy = df_total.loc[df_total['isbuy'] == True,]
        df_sell = df_total.loc[df_total['isbuy'] != True,]

        df_buy = df_buy.groupby('연월')[val_set].sum()
        df_sell = df_sell.groupby('연월')[val_set].sum()

        df_buy = df_buy.reset_index()
        df_sell = df_sell.reset_index()


        # 정해진 기간 내에 매입이나 매출 정보가 없으면 Join에서 문제가 생기므로, 있는 join 기준열만 가져온다.
        if df_buy['연월'].shape[0] == 0:
            df_buy['연월'] = df_sell['연월']
        if df_sell['연월'].shape[0] == 0:
            df_sell['연월'] = df_buy['연월']
        

        df_all = df_buy.merge(df_sell, how='outer', on='연월')
        df_all.columns = ['연월', '매입', '매출']
        df_all = df_all.fillna(0)
        df_all['매입'] = df_all['매입'].astype(int)

        df_all['순이익'] = df_all['매출'] - df_all['매입']

        print (df_all.columns[1:])
        fig1 = px.line(df_all, x='연월', y=df_all.columns[1:])
        st.plotly_chart(fig1)


        # 월간 매입매출 계산
        total_set = df_total.groupby(['연월','isbuy'])[val_set].sum()
        total_set = total_set.reset_index()
        

        #원하는 결과 [월 - 매입액 - 매출액 - 순이익]
        
        

        # st.dataframe(total_set)
        # st.line_chart(total_income)
        # fig1 = plt.figure()
        # plt.plot(total_income.iloc[:,0]) #총매출
        # plt.plot(total_income.iloc[:,1]) #총매입
        # plt.plot(total_income.iloc[:,2]) #순이익
        # plt.legend(total_income.columns)
        # st.pyplot(fig1)

    

    # menu 기간별 성적
    if ms == menu[1]:
        # col_set에는 선택한 값들이 리스트의 형태로 들어가 있다.
        # 이 값들에 해당하는 데이터만 가지고 오도록 df를 가공해야 한다.
        
        if len(col_set) != 0:
            df_set = df_set.set_index(index_set).loc[col_set]
            df_set.reset_index(inplace=True)
            df_set = df_set.groupby([index_set, '날짜'])[val_set].sum()
            df_set = df_set.reset_index()
            # df_set['날짜'] = pd.to_datetime(df_set['날짜'])
            # df_set = df_set.groupby(df_set['날짜'].dt.strftime('%B'))[val_set].sum()

            # 차트 그리기
            fig2 = px.line(df_set, x='날짜', y=val_set, color=index_set)
            st.plotly_chart(fig2)
        
        pass

    # menu 점유율(pie)
    elif ms == menu[2]:
        df_set = df_set.groupby(index_set)[val_set].sum()
        df_set = df_set.reset_index()
        # st.dataframe(df_set)
        fig3 = px.pie(df_set, names = index_set, values = val_set)
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig3)
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