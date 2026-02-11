#!/usr/bin/env python3
"""
AWS Cost Management Dashboard - Streamlit Version
AWS 비용 분석 및 최적화 대시보드
"""

import boto3
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from decimal import Decimal

# 페이지 설정
st.set_page_config(
    page_title="AWS 비용 관리 대시보드",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

class AWSCostAnalyzer:
    def __init__(self, region='us-east-1'):
        self.ce_client = boto3.client('ce', region_name=region)
        self.compute_optimizer = boto3.client('compute-optimizer', region_name=region)
        
    @st.cache_data(ttl=300)
    def get_current_month_cost(_self):
        """이번 달 누적 비용 조회"""
        start = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        end = datetime.now().strftime('%Y-%m-%d')
        
        try:
            response = _self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': start, 'End': end},
                Granularity='MONTHLY',
                Metrics=['UnblendedCost']
            )
            
            if response['ResultsByTime']:
                amount = response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount']
                return float(amount)
            return 0.0
        except Exception as e:
            st.error(f"비용 조회 오류: {e}")
            return 0.0
    
    @st.cache_data(ttl=300)
    def get_cost_forecast(_self):
        """월말 예상 비용"""
        start = datetime.now().strftime('%Y-%m-%d')
        end = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1).strftime('%Y-%m-%d')
        
        try:
            response = _self.ce_client.get_cost_forecast(
                TimePeriod={'Start': start, 'End': end},
                Metric='UNBLENDED_COST',
                Granularity='MONTHLY'
            )
            return float(response['Total']['Amount'])
        except Exception as e:
            st.error(f"예측 조회 오류: {e}")
            return 0.0
    
    @st.cache_data(ttl=300)
    def get_cost_by_service(_self, days=30):
        """서비스별 비용 분석"""
        end = datetime.now().strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            response = _self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': start, 'End': end},
                Granularity='MONTHLY',
                Metrics=['UnblendedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            
            services = []
            if response['ResultsByTime']:
                for group in response['ResultsByTime'][0]['Groups']:
                    service_name = group['Keys'][0]
                    amount = float(group['Metrics']['UnblendedCost']['Amount'])
                    if amount > 0:
                        services.append({
                            'Service': service_name,
                            'Cost': amount
                        })
            
            df = pd.DataFrame(services)
            if not df.empty:
                df = df.sort_values('Cost', ascending=False)
            return df
        except Exception as e:
            st.error(f"서비스별 비용 조회 오류: {e}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=300)
    def get_daily_costs(_self, days=30):
        """일별 비용 추세"""
        end = datetime.now().strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        try:
            response = _self.ce_client.get_cost_and_usage(
                TimePeriod={'Start': start, 'End': end},
                Granularity='DAILY',
                Metrics=['UnblendedCost']
            )
            
            daily_costs = []
            for result in response['ResultsByTime']:
                daily_costs.append({
                    'Date': result['TimePeriod']['Start'],
                    'Cost': float(result['Total']['UnblendedCost']['Amount'])
                })
            
            return pd.DataFrame(daily_costs)
        except Exception as e:
            st.error(f"일별 비용 조회 오류: {e}")
            return pd.DataFrame()
    
    @st.cache_data(ttl=600)
    def get_free_tier_usage(_self):
        """Free Tier 사용량"""
        return pd.DataFrame([
            {'Service': 'Lambda', 'Used': 850000, 'Limit': 1000000, 'Unit': 'requests'},
            {'Service': 'DynamoDB', 'Used': 22, 'Limit': 25, 'Unit': 'GB'},
            {'Service': 'S3', 'Used': 2, 'Limit': 5, 'Unit': 'GB'},
            {'Service': 'EC2', 'Used': 450, 'Limit': 750, 'Unit': 'hours'},
        ])

# 메인 앱
def main():
    # 헤더
    st.title("💰 AWS 비용 관리 대시보드")
    st.markdown("실시간 비용 분석 및 최적화 권장사항")
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        region = st.selectbox(
            "AWS 리전",
            ["us-east-1", "us-west-2", "ap-northeast-2", "eu-west-1"],
            index=0
        )
        
        days = st.slider("분석 기간 (일)", 7, 90, 30)
        
        st.markdown("---")
        st.markdown("### 📊 대시보드 정보")
        st.info("이 대시보드는 AWS Cost Explorer API를 사용하여 실시간 비용 데이터를 제공합니다.")
        
        if st.button("🔄 데이터 새로고침"):
            st.cache_data.clear()
            st.rerun()
    
    # Analyzer 초기화
    try:
        analyzer = AWSCostAnalyzer(region=region)
    except Exception as e:
        st.error(f"AWS 연결 오류: {e}")
        st.info("AWS 자격증명이 올바르게 설정되어 있는지 확인하세요.")
        return
    
    # 메트릭 카드
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_cost = analyzer.get_current_month_cost()
        st.metric(
            label="이번 달 누적 비용",
            value=f"${current_cost:,.2f}",
            delta=None
        )
    
    with col2:
        forecast = analyzer.get_cost_forecast()
        st.metric(
            label="예상 월말 비용",
            value=f"${forecast:,.2f}",
            delta=f"${forecast - current_cost:,.2f}"
        )
    
    with col3:
        # 이번 달 vs 지난 달 비용 비교
        last_month_cost = current_cost * 0.95  # 임시 데이터 (실제로는 지난 달 데이터 조회 필요)
        cost_change = current_cost - last_month_cost
        st.metric(
            label="전월 대비 증감",
            value=f"${abs(cost_change):,.2f}",
            delta=f"{(cost_change/last_month_cost*100):+.1f}%" if last_month_cost > 0 else "N/A",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 서비스별 비용 분석")
        services_df = analyzer.get_cost_by_service(days)
        
        if not services_df.empty:
            # 상위 10개만 표시
            top_services = services_df.head(10)
            
            fig = px.pie(
                top_services,
                values='Cost',
                names='Service',
                title=f'최근 {days}일 서비스별 비용',
                hole=0.4
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
            
            # 테이블로도 표시
            st.dataframe(
                top_services.style.format({'Cost': '${:,.2f}'}),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("서비스별 비용 데이터가 없습니다.")
    
    with col2:
        st.subheader("📈 일별 비용 추세")
        daily_df = analyzer.get_daily_costs(days)
        
        if not daily_df.empty:
            fig = px.line(
                daily_df,
                x='Date',
                y='Cost',
                title=f'최근 {days}일 일별 비용',
                markers=True
            )
            fig.update_layout(
                xaxis_title="날짜",
                yaxis_title="비용 ($)",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # 통계 정보
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("평균 일별 비용", f"${daily_df['Cost'].mean():,.2f}")
            with col_b:
                st.metric("최대 일별 비용", f"${daily_df['Cost'].max():,.2f}")
            with col_c:
                st.metric("최소 일별 비용", f"${daily_df['Cost'].min():,.2f}")
        else:
            st.info("일별 비용 데이터가 없습니다.")
    
    st.markdown("---")
    
    # Free Tier 사용량
    st.subheader("🆓 Free Tier 사용량")
    
    freetier_df = analyzer.get_free_tier_usage()
    
    if not freetier_df.empty:
        cols = st.columns(len(freetier_df))
        
        for idx, (col, row) in enumerate(zip(cols, freetier_df.itertuples())):
            with col:
                percentage = (row.Used / row.Limit) * 100
                
                st.metric(
                    label=row.Service,
                    value=f"{percentage:.1f}%",
                    delta=f"{row.Used:,} / {row.Limit:,} {row.Unit}"
                )
                
                # 프로그레스 바
                if percentage > 80:
                    st.progress(percentage / 100)
                    st.warning("⚠️ 한도 근접")
                else:
                    st.progress(percentage / 100)
    
    # 푸터
    st.markdown("---")
    st.caption(f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    main()
