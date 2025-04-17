import streamlit as st
import pandas as pd

def load_material_data():
    """
    엑셀 파일에서 자재 데이터를 불러오는 함수
    """
    try:
        # 절대 경로 지정
        file_path = r'D:\github\training\가격정보.xlsx'
        
        # 엑셀 파일 읽기
        df = pd.read_excel(file_path, engine='openpyxl')
        
        return df
    
    except FileNotFoundError:
        st.error(f"파일을 찾을 수 없습니다. 경로를 확인해주세요.")
        return None
    except Exception as e:
        st.error(f"파일을 불러오는 중 오류 발생: {e}")
        return None

def search_materials(df, search_term, price_min, price_max, search_column, price_column):
    """
    품목명과 가격 범위로 복합 검색하는 함수
    """
    try:
        # 초기 데이터프레임 복사
        filtered_df = df.copy()
        
        # 품목명 검색 (대소문자 구분 없이)
        if search_term:
            filtered_df = filtered_df[
                filtered_df[search_column].str.contains(search_term, case=False, na=False)
            ]
        
        # 가격 범위 필터링
        filtered_df = filtered_df[
            (filtered_df[price_column] >= price_min) & 
            (filtered_df[price_column] <= price_max)
        ]
        
        return filtered_df
    
    except Exception as e:
        st.error(f"검색 중 오류 발생: {e}")
        return pd.DataFrame()

def main():
    st.set_page_config(
        page_title="복합 검색 시스템", 
        layout="wide"
    )
    
    st.title('🔍 품목 및 가격 복합 검색 시스템')
    
    # 데이터 로드
    materials_df = load_material_data()
    
    if materials_df is not None:
        # 사이드바 설정
        st.sidebar.header('🔎 검색 옵션')
        
        # 검색 컬럼 선택 (문자열 컬럼)
        search_columns = materials_df.select_dtypes(include=['object']).columns.tolist()
        search_column = st.sidebar.selectbox('검색 컬럼 선택', search_columns)
        
        # 가격 컬럼 선택 (숫자 컬럼)
        price_columns = materials_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        price_column = st.sidebar.selectbox('가격 컬럼 선택', price_columns)
        
        # 품목명 검색 입력
        search_term = st.sidebar.text_input('품목명 검색:')
        
        # 가격 범위 입력
        col1, col2 = st.sidebar.columns(2)
        with col1:
            min_price = st.number_input(
                '최소 가격', 
                min_value=0, 
                value=0, 
                step=100
            )
        
        with col2:
            max_price = st.number_input(
                '최대 가격', 
                min_value=min_price, 
                value=int(materials_df[price_column].max()), 
                step=100
            )
        
        # 검색 버튼
        if st.sidebar.button('검색'):
            # 복합 검색 실행
            filtered_df = search_materials(
                materials_df, 
                search_term, 
                min_price, 
                max_price, 
                search_column, 
                price_column
            )
            
            # 결과 표시
            if not filtered_df.empty:
                st.subheader(f"검색 결과")
                
                # 검색 조건 표시
                search_condition = f"""
                - 검색 컬럼: {search_column}
                - 품목명: {search_term if search_term else '전체'}
                - 가격 범위: {min_price}원 ~ {max_price}원
                """
                st.markdown(search_condition)
                
                # 검색 결과 표시
                st.dataframe(filtered_df)
                
                # 결과 통계 (건수만)
                st.metric(
                    label="검색 결과 건수", 
                    value=f"{len(filtered_df)}건"
                )
                
            else:
                st.warning('검색 결과가 없습니다.')

if __name__ == '__main__':
    main()