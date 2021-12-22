import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime

from chart import chart_app
from dataframe import df_app

#################################################################
# df = 전체 데이터 프레임
# df_month = 날짜를 연/월로 나눠놓은 데이터프레임
# total_income = 월별 총매출, 총매입, 순수익 데이터프레임 
#
#################################################################

#### 레이 아웃 #######################
st.set_page_config(
    page_title='기록관리',
    # page_icon=temp,
    layout='wide',
    initial_sidebar_state='expanded'
)
##########################################
# 주요 코드################################
def main() :
    # 파일 입력 및 기본 가공
    df = pd.read_csv('data/입출고 관리 - 작성.csv')
    df = df.fillna(method='pad')    # 현재 데이터는 기록이 자동화되어있지 않으므로
                                    # 기록 시간을 줄이기 위해 같은 데이터는 등장시에만
                                    # 기록하게끔 설정했음.
    # 날짜 형변환
    # 날짜 column 에서 float problem. 스프레드시트 파일에서 문제가 있었는지,
    # 혹은 기록중에 데이터가 오염되었는지는 알 수 없으나
    # float형식으로 읽어들이면서 20210902 형식에서 20,210,902.0000 형식으로 바뀌었음.
    # 데이터가 변형된 원인조차 알 수 없었으므로, 데이터 단위의 해결보다, 개발상의 해결 비용이 더 적다고 판단,
    # 이를 해결하기 위해 날짜를 여러번 형변환 해야 했음.
    df['날짜'] = df['날짜'].astype('str')
    df['날짜'] = df['날짜'].str.rstrip('.0') 
    df['날짜'] = df['날짜'].str[0:4] +'-'+ df['날짜'].str[4:6] +'-'+ df['날짜'].str[6:8]
   
    # # 전체 데이터프레임 가공
    df['날짜'] = pd.to_datetime(df['날짜'])#.dt.date
    df['품목'] = df['품목'].astype(str)
    df['단가'] = df['단가'].astype('int')
    df['거래량'] = abs (df['거래량'].astype('int'))
    df['매출'] = df['거래량'] * df['단가']
    
    # 리스트가 중첩된만큼 다차원 배열이 형성된다.

    # 날짜를 연/월별로 나눈 데이터프레임
    # df_month = df.copy()
    # df_month['년'] = df_month['날짜'].dt.year
    # df_month['월'] = df_month['날짜'].dt.month
    # df_month.drop(columns = '날짜', inplace=True)
    # df_month = df_month[['년', '월', '거래처', '품목', '거래량', '단가', '매출']]

    #! .dt.date된 데이터는 datetime이 아니므로 year와 month로 나눌 수 없어 하단에 작성함.
    df['날짜'] = df['날짜'].dt.date

    # 월별 매입/매출 데이터프레임
    # df_buy = df.loc[df['거래처']=='매입',]
    # df_sell = df.loc[df['거래처']!='매입',]
    # df_buy_month = df_month.loc[df['거래처']=='매입',]
    # df_sell_month = df_month.loc[df['거래처']!='매입',]

    # # 월별 총매출
    # total_sell = df_sell_month.groupby(['년','월'])['매출'].sum()
    # total_sell = pd.DataFrame(total_sell).reset_index()
    # # 월별 총매입
    # total_buy = df_buy_month.groupby(['년','월'])['매출'].sum()
    # total_buy = pd.DataFrame(total_buy).reset_index()
    # total_buy = total_buy.drop(columns='년')
    # # 월별 순이익 데이터프레임으로 합성
    # total_income = pd.merge(total_sell, total_buy, on='월', how='outer')
    # total_income.columns = ['년', '월', '총매출', '총매입']
    # total_income.fillna(0, inplace=True)
    # total_income['순이익'] = total_income['총매출'] - total_income['총매입']
    # total_income['년월'] = total_income['년'].astype(str) +'-'+ total_income['월'].astype(str)
    # total_income.set_index('년월', inplace=True)
    # total_income.drop(columns=['년', '월'],inplace=True)
##########################################################################################
##########################################################################################

    # 스트림릿 레이아웃
    st.title ('재고 및 재무관리 도우미')
    st.subheader ('범위 설정')
    st.write ('전체 데이터 범위를 설정합니다.')
    menu = ['전표', '차트']
    menu_choice = st.sidebar.selectbox('메뉴', menu)
    trade = ['매출', '매입']
    trade_sel = st.sidebar.radio('유형', trade)
    # 조건문은 데이터 가공이 끝난 후에 작성

    # 날짜 설정
    datecol1, datecol2 = st.columns(2)
    with datecol1:
        start_date = st.date_input('부터', min(df['날짜'])) # 최초 기입일
        
    with datecol2:            
        end_date = st.date_input('까지', datetime.now())

    # input widget의 값을 해당 widget 외부에서 변경하는 방법은 현재로선 없습니다만
    # 추후에 기능이 생겼을 때를 대비해
    # 추가할 기능을 명시할 방법으로써 남겨두겠습니다.    
    # btncol1, btncol2 = st.columns(2)

    # with btncol1:
    #     if st.button('재설정', help='최초 기입일로 설정합니다.'):            
    #         start_date = min(df['날짜'])
    # with btncol2:
    #     if st.button('오늘로'):
    #         end_date = datetime.now().date()

    # 스트림릿 목록 변수 설정
    accounts = sorted(df['거래처'].unique())
    items = sorted(df['품목'].unique())

    optioncol1, optioncol2 = st.columns(2)
    with optioncol1:
        accounts_ms = st.multiselect ('거래처 선택', accounts)
    with optioncol2:
        items_ms = st.multiselect ('품목 선택', items)

    # 데이터 프레임 최종 가공
    df_acc=df.set_index('거래처')
    df_items=df.set_index('품목')

    if len(accounts_ms) != 0:
        df_acc = df_acc.loc[accounts_ms,]
    if len (items_ms) != 0:
        df_items = df_items.loc[items_ms,]

    df_acc.reset_index(inplace=True)
    df_items.reset_index(inplace=True)

    columns_list = list (df_acc.columns)
    df_set = pd.merge(df_acc, df_items, how='inner', on=columns_list)
    df_set = df_set.loc[(df_set['날짜'] >= start_date) & (df_set['날짜'] <= end_date)]
    df_set.sort_values('날짜', inplace=True)

    df_total = df_set

    # 매출 매입 조건문
    if trade_sel == trade[0]:
        df_set = df_set.loc[df_set['거래처'] != '매입',]
    elif trade_sel == trade[1]:
        df_set = df_set.loc[df_set['거래처'] == '매입',]

    
    # df_set['연월'] = str(df_set['날짜'].dt.year), str(df_set['날짜'].dt.month)
    # df_set['날짜'] = pd.to_datetime(df_set['날짜'])
    # # st.dataframe(df_set)
    
    # st.dataframe(df_set)
    
    # # st.dataframe(df_set.groupby(df_set['날짜'].dt.month))
        
##################################################################
##################################################################

    # menu 전표
    if menu_choice == menu[0]:
        df_app(df_set)

    # menu 차트
    elif menu_choice == menu[1]:
        chart_app(df_set, df_total )



if __name__ == '__main__' :
    main()