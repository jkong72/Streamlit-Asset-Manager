import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from datetime import datetime

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


def main() :
    # 파일 입력
    df = pd.read_csv('data/입출고 관리 - 작성.csv')
    df = df.fillna(method='pad')    # 현재 데이터는 기록이 자동화되어있지 않으므로
                                    # 기록 시간을 줄이기 위해 같은 데이터는 등장시에만
                                    # 기록하게끔 설정했음.
    # 날짜 형변환
    # 날짜 column 에서 float problem. 스프레드시트 파일에서 문제가 있었는지,
    # 혹은 기록중에 데이터가 오염되었는지는 알 수 없으나
    # float형식으로 읽어들이면서 20210902 형식에서 20,210,902.0000 형식으로 바뀌었음.
    # 이를 해결하기 위해 날짜를 여러번 형변환 해야 했음.
    df['날짜'] = df['날짜'].astype('str')
    df['날짜'] = df['날짜'].str.rstrip('.0') 
    df['날짜'] = df['날짜'].str[0:4] +'-'+ df['날짜'].str[4:6] +'-'+ df['날짜'].str[6:8]

    
    # # 전체 데이터프레임 가공
    df['날짜'] = pd.to_datetime(df['날짜'])#.dt.date
    df['단가'] = df['단가'].astype('int')
    df['거래량'] = abs (df['거래량'].astype('int'))
    df['매출'] = df['거래량'] * df['단가']



    # 날짜를 연/월별로 나눈 데이터프레임
    df_month = df.copy()
    df_month['년'] = df_month['날짜'].dt.year
    df_month['월'] = df_month['날짜'].dt.month
    df_month.drop(columns = '날짜', inplace=True)
    df_month = df_month[['년', '월', '거래처', '품목', '거래량', '단가', '매출']]

    #! .dt.date된 데이터는 datetime이 아니므로 year와 month로 나눌 수 없어 하단에 작성함.
    df['날짜'] = df['날짜'].dt.date

    # 월별 매입/매출 데이터프레임
    df_buy = df.loc[df['거래처']=='매입',]
    df_sell = df.loc[df['거래처']!='매입',]
    df_buy_month = df_month.loc[df['거래처']=='매입',]
    df_sell_month = df_month.loc[df['거래처']!='매입',]

    # 월별 총매출
    total_sell = df_sell_month.groupby(['년','월'])['매출'].sum()
    total_sell = pd.DataFrame(total_sell).reset_index()
    # 월별 총매입
    total_buy = df_buy_month.groupby(['년','월'])['매출'].sum()
    total_buy = pd.DataFrame(total_buy).reset_index()
    total_buy = total_buy.drop(columns='년')
    # 월별 순이익 데이터프레임으로 합성
    total_income = pd.merge(total_sell, total_buy, on='월', how='outer')
    total_income.columns = ['년', '월', '총매출', '총매입']
    total_income.fillna(0, inplace=True)
    total_income['순이익'] = total_income['총매출'] - total_income['총매입']
    total_income['년월'] = total_income['년'].astype(str) +'-'+ total_income['월'].astype(str)
    total_income.set_index('년월', inplace=True)
    total_income.drop(columns=['년', '월'],inplace=True)


    # 스트림릿 레이아웃
    menu = ['전표', '차트']
    menu_choice = st.sidebar.selectbox('메뉴', menu)

#temp corner ########################################

    st.dataframe(df)   
    

    # menu 전표
    if menu_choice == menu[0]:
        datecol1, datecol2 = st.columns(2)
        with datecol1:
            start_date = st.date_input('부터', min(df['날짜'])) # 최초 기입일
        with datecol2:            
            end_date = st.date_input('까지', datetime.now())

        # 목록 변수 설정
        accounts = df['거래처'].unique()
        items = df['품목'].unique()

        optioncol1, optioncol2 = st.columns(2)
        with optioncol1:
            accounts_ms = st.multiselect ('거래처 선택', accounts)
        with optioncol2:
            items_ms = st.multiselect ('품목 선택', items)

        # 날짜 검색 결과
        # datedf = df.loc[df['날짜']==start_date:df['날짜']==end_date,:]
        # st.dataframe(datedf)

        # 옵션 검색 결과
        search_range = ['넓히기(모두)', '좁히기(일치)']
        search_set = st.sidebar.radio('검색 설정', search_range)
        if search_set == search_range[0]:
            df_selected_ms = df.loc[(df['거래처']=='중앙')|(df['품목']=='102'),:] 
            # for는 스텝이 너무 많아지므로 고려하지 않음.
            # set_index를 통해 데이터를 구한후, reset index -> merge가 나을지...
            
            df_date=df.set_index('날짜')
            df_acc=df.set_index('거래처')
            df_items=df.set_index('품목')

            print(type(str(start_date)))

            # df_date = df_date.loc[start_date:,:]

            df_acc = df_acc.loc[accounts_ms,]
            st.dataframe(df_acc)

            df_items = df_items.loc[items_ms,]

        
            

        # elif search_set == search_range[1]:
            # df_selected_ms = df.loc[(df['거래처']=='중앙')&(df['품목']=='102'),:] 
        



    elif menu_choice == menu[1]:
        pass



if __name__ == '__main__' :
    main()