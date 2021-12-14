import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

#################################################################
# df = 전체 데이터 프레임
# df_month = 날짜를 연/월로 나눠놓은 데이터프레임
# total_income = 월별 총매출, 총매입, 순수익 데이터프레임 
#
#################################################################


def main() :
    
    # 날짜 형변환
    df = pd.read_csv('data/입출고 관리 - 작성.csv')
    df = df.fillna(method='pad')
    df['날짜'] = df['날짜'].astype('str')
    df['날짜'] = df['날짜'].str.rstrip('.0')
    df['날짜'] = df['날짜'].str[0:4] +'-'+ df['날짜'].str[4:6] +'-'+ df['날짜'].str[6:8]

    # # 전체 데이터프레임 가공
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['단가'] = df['단가'].astype('int')
    df['거래량'] = abs (df['거래량'].astype('int'))
    df['매출'] = df['거래량'] * df['단가']

    
    # 날짜를 연/월별로 나눈 데이터프레임
    df_month = df.copy()
    df_month['년'] = df_month['날짜'].dt.year
    df_month['월'] = df_month['날짜'].dt.month
    df_month.drop(columns = '날짜', inplace=True)
    df_month = df_month[['년', '월', '거래처', '품목', '거래량', '단가', '매출']]

    # 월별 매입/매출 데이터프레임
    df_buy = df.loc[df['거래처']=='매입',]
    df_sell = df.loc[df['거래처']!='매입',]
    df_buy_month = df_month.loc[df['거래처']=='매입',]
    df_sell_month = df_month.loc[df['거래처']!='매입',]

    # 월별 총매출 (데이터프레임)
    total_sell = df_sell_month.groupby(['년','월'])['매출'].sum()
    total_sell = pd.DataFrame(total_sell).reset_index()
    # 월별 총매입 (데이터프레임)
    total_buy = df_buy_month.groupby(['년','월'])['매출'].sum()
    total_buy = pd.DataFrame(total_buy).reset_index()
    total_buy = total_buy.drop(columns='년')
    # 월별 순이익
    total_income = pd.merge(total_sell, total_buy, on='월', how='outer')
    total_income.columns = ['년', '월', '총매출', '총매입']
    total_income.fillna(0, inplace=True)
    total_income['순이익'] = total_income['총매출'] - total_income['총매입']
    total_income['년월'] = total_income['년'].astype(str) +'-'+ total_income['월'].astype(str)
    total_income.set_index('년월', inplace=True)
    total_income.drop(columns=['년', '월'],inplace=True)



    if st.button ('전체 데이터 확인'):
        st.dataframe(df)
    if st.button ('재무 데이터 확인'):
        st.dataframe(total_income)



if __name__ == '__main__' :
    main()