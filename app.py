import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="풍산 R&D 성과연계 내부통제 분석",
    page_icon="🔎",
    layout="wide"
)

# -----------------------------
# 기본 스타일
# -----------------------------
st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
[data-testid="stMetricValue"] {font-size: 1.65rem;}
.small-note {color:#666; font-size:0.88rem;}
.box {
    border:1px solid #e5e5e5; border-radius:12px;
    padding:16px; margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 공개 공시 기반 R&D 데이터
# 단위: 억원
# -----------------------------
annual = pd.DataFrame({
    "기간": ["2023", "2024", "2025"],
    "자산계상": [14.98, 10.81, 3.58],
    "비용계상": [275.85, 304.07, 340.62],
    "연구개발비": [290.83, 314.88, 344.20],
    "매출액대비비율": [0.70, 0.69, 0.68],
})

half = pd.DataFrame({
    "기간": ["2025 상반기", "2026 상반기"],
    "자산계상": [5.43, 2.74],
    "비용계상": [147.42, 157.34],
    "연구개발비": [152.85, 160.08],
    "매출액대비비율": [0.62, 0.58],
})

annual["자산계상비중"] = annual["자산계상"] / annual["연구개발비"] * 100
half["자산계상비중"] = half["자산계상"] / half["연구개발비"] * 100

# 공개 공시에서 확인 가능한 연구과제 예시
projects = pd.DataFrame([
    {
        "연구과제": "Bio MediCopper 제품화 개발",
        "개발기간": "2015.07 ~ 2026.12",
        "진행상황": "개발완료 후 용도 확대",
        "관련제품": "건축·내장재·인테리어·식기",
        "기대효과": "위생·환경 친화성 홍보 강화 및 시장 확대를 통한 판매 증대",
        "실제성과": "공개자료만으로 개별 과제 성과 확인 제한",
    },
    {
        "연구과제": "고전압용 동합금 개발",
        "개발기간": "2019.01 ~ 2026.12",
        "진행상황": "양산화 진행",
        "관련제품": "전기차·ESS용 고전압 커넥터",
        "기대효과": "수입소재 대체 및 신규 자동차 소재 적용을 통한 매출 증대",
        "실제성과": "공개자료만으로 개별 과제 매출 확인 제한",
    },
    {
        "연구과제": "Cu-Ni-Co-Si계 합금 개발",
        "개발기간": "2021.02 ~ 2028.12",
        "진행상황": "양산화 개발",
        "관련제품": "자동차 초소형 단자·스마트폰 부품",
        "기대효과": "고부가가치 고강도 모바일 단자용 동합금 신수요 창출",
        "실제성과": "공개자료만으로 개별 과제 성과 확인 제한",
    },
    {
        "연구과제": "Cu-Cr-Zr계 합금 개발",
        "개발기간": "2025.01 ~ 2027.12",
        "진행상황": "제품 개발",
        "관련제품": "전기전자 부품",
        "기대효과": "고전도 합금 시장 확대",
        "실제성과": "공개자료만으로 개별 과제 성과 확인 제한",
    },
])

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("풍산 R&D 내부통제")
page = st.sidebar.radio(
    "분석 메뉴",
    [
        "1. Overview",
        "2. 연구과제 현황",
        "3. R&D → 성과 연결",
        "4. 내부통제 Risk 분석",
        "5. 상시모니터링",
        "6. 내부통제 Dashboard",
    ]
)

st.sidebar.divider()
st.sidebar.caption(
    "공개 공시자료를 기반으로 구현한 지원자 관점의 분석 도구입니다. "
    "풍산의 실제 내부통제 운영 결과나 비공개 내부 데이터를 추정하지 않습니다."
)

# -----------------------------
# 1. Overview
# -----------------------------
if page == "1. Overview":
    st.title("풍산 R&D 성과연계 내부통제 분석")
    st.write(
        "연구개발비의 증가 자체보다, 연구개발 투입이 연구과제 진행·양산화·사업성과로 "
        "이어지는 과정에서 무엇을 확인해야 하는지 분석합니다."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("2023 R&D", "290.83억원")
    c2.metric("2025 R&D", "344.20억원", "+18.4% vs 2023")
    c3.metric("2026 상반기 R&D", "160.08억원", "+4.7% YoY")
    c4.metric("2025 자산계상 비중", f"{annual.loc[2,'자산계상비중']:.2f}%",
              f"{annual.loc[2,'자산계상비중']-annual.loc[0,'자산계상비중']:.2f}%p vs 2023")

    st.subheader("연구개발비 추이")
    fig = px.line(
        annual, x="기간", y="연구개발비",
        markers=True, text="연구개발비",
        labels={"연구개발비":"억원"}
    )
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("비용·자산 계상")
    melted = annual.melt(
        id_vars="기간",
        value_vars=["비용계상", "자산계상"],
        var_name="구분", value_name="억원"
    )
    fig2 = px.bar(melted, x="기간", y="억원", color="구분", barmode="stack")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("최신 반기 비교")
    h1, h2 = st.columns(2)
    yoy = (160.08 / 152.85 - 1) * 100
    h1.metric("2025 H1", "152.85억원")
    h2.metric("2026 H1", "160.08억원", f"+{yoy:.1f}%")

    st.info(
        "핵심 관찰: 2023~2025년 연구개발비는 18.4% 증가했지만 "
        "자산계상액은 14.98억원 → 3.58억원으로 감소했습니다. "
        "프로그램은 이러한 변화 자체를 이상으로 단정하지 않고, "
        "내부통제 담당자가 확인해야 할 근거와 프로세스를 도출합니다."
    )

# -----------------------------
# 2. 연구과제 현황
# -----------------------------
elif page == "2. 연구과제 현황":
    st.title("연구과제 현황")
    st.write("공시에서 확인되는 연구과제를 개발기간·진행상황·기대효과와 연결합니다.")

    keyword = st.text_input("과제명/제품 검색")
    view = projects.copy()
    if keyword:
        mask = view.astype(str).apply(
            lambda row: row.str.contains(keyword, case=False, na=False).any(), axis=1
        )
        view = view[mask]

    st.dataframe(
        view[["연구과제","개발기간","진행상황","관련제품","기대효과"]],
        use_container_width=True,
        hide_index=True
    )

    st.warning(
        "과제별 예산, 실제 집행액, 승인내역, 진행률 및 개별 매출성과는 "
        "공개자료만으로 확인할 수 없습니다. 실제 내부통제에서는 해당 내부데이터가 필요합니다."
    )

# -----------------------------
# 3. R&D → 성과 연결
# -----------------------------
elif page == "3. R&D → 성과 연결":
    st.title("R&D → 성과 연결")
    selected = st.selectbox("연구과제 선택", projects["연구과제"])
    row = projects.loc[projects["연구과제"] == selected].iloc[0]

    a,b,c,d,e = st.columns(5)
    a.markdown("### ① 투입\nR&D 예산·집행")
    b.markdown(f"### ② 연구\n{row['연구과제']}")
    c.markdown(f"### ③ 진행\n{row['진행상황']}")
    d.markdown(f"### ④ 제품\n{row['관련제품']}")
    e.markdown("### ⑤ 성과\n매출·수익성")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("공시에서 확인")
        st.write("**개발기간:**", row["개발기간"])
        st.write("**진행상황:**", row["진행상황"])
        st.write("**관련제품:**", row["관련제품"])
        st.write("**기대효과:**", row["기대효과"])

    with c2:
        st.subheader("추가 내부데이터 필요")
        st.write("• 과제별 승인 예산")
        st.write("• 실제 집행액 및 증빙")
        st.write("• 단계별 연구진행률 및 성과물")
        st.write("• 양산전환 승인 내역")
        st.write("• 관련 제품 매출·수익성")
        st.write("• 개발비 자산화 판단 근거")

    st.success(
        "내부통제 관점: R&D 비용을 단순히 줄이는 것이 아니라, "
        "승인된 연구목적에 따라 자금이 집행되고 연구성과가 양산과 사업성과로 "
        "연결되는 과정의 신뢰성을 확보하는 것이 핵심입니다."
    )

# -----------------------------
# 4. 내부통제 Risk 분석
# -----------------------------
elif page == "4. 내부통제 Risk 분석":
    st.title("R&D 프로세스 Risk-Control Matrix")

    rcm = pd.DataFrame([
        ["과제 선정", "사업전략과 관련성이 낮은 과제 승인", "과제 타당성 검토 및 승인", "과제기획서·승인내역"],
        ["예산", "승인 예산을 초과한 집행", "예산 대비 실적 비교 및 추가승인", "예산·집행액·추가승인"],
        ["비용 집행", "R&D와 무관한 비용 포함", "증빙·계정·프로젝트 코드 검증", "전표·증빙·프로젝트 코드"],
        ["연구 진행", "일정 지연에도 비용 지속 발생", "개발일정·진행률 정기 점검", "진행보고서·성과물"],
        ["양산 전환", "개발완료 후 양산전환 지연", "양산전환 승인 및 일정 점검", "양산승인·생산계획"],
        ["성과", "양산 후 기대성과 미달", "제품별 매출·수익성 사후점검", "제품별 매출·원가"],
        ["회계처리", "연구비/개발비 분류 오류", "자산인식 요건 및 승인근거 검토", "회계검토서·승인자료"],
        ["자산 사후관리", "사업화 지연에도 손상징후 미검토", "손상징후 정기 검토", "사업계획·회수가능성 자료"],
    ], columns=["단계","주요 Risk","Control","필요 데이터"])

    st.dataframe(rcm, use_container_width=True, hide_index=True)

    stage = st.selectbox("상세 확인 단계", rcm["단계"])
    r = rcm.loc[rcm["단계"] == stage].iloc[0]
    st.markdown(
        f"""
        <div class="box">
        <b>Risk</b><br>{r['주요 Risk']}<br><br>
        <b>Control</b><br>{r['Control']}<br><br>
        <b>필요 데이터</b><br>{r['필요 데이터']}
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 5. 상시모니터링
# -----------------------------
elif page == "5. 상시모니터링":
    st.title("R&D 상시모니터링 시뮬레이터")
    st.caption("아래 입력값은 풍산의 실제 내부데이터가 아닌 통제 Rule 작동을 보여주기 위한 사용자 입력값입니다.")

    c1,c2,c3 = st.columns(3)
    with c1:
        budget = st.number_input("승인 예산(억원)", min_value=0.0, value=10.0, step=0.5)
        actual = st.number_input("실제 집행액(억원)", min_value=0.0, value=10.5, step=0.5)
        extra_approval = st.checkbox("예산 초과 추가승인 존재")
    with c2:
        planned_progress = st.slider("계획 진행률(%)", 0, 100, 80)
        actual_progress = st.slider("실제 진행률(%)", 0, 100, 75)
        period_ended = st.checkbox("개발기간 종료")
    with c3:
        mass_production = st.checkbox("양산화 완료")
        performance = st.checkbox("관련 제품 성과 확인")
        capitalized = st.checkbox("개발비 자산계상")
        commercialization_delay = st.checkbox("사업화 장기지연")

    alerts = []

    if budget > 0 and actual > budget * 1.10 and not extra_approval:
        alerts.append(("🔴", "Rule 01", "실제 집행액이 승인 예산의 110%를 초과했으나 추가승인이 확인되지 않습니다.",
                       "예산 변경 승인 및 초과 집행 증빙 확인"))
    if actual_progress + 10 < planned_progress:
        alerts.append(("🟠", "Rule 02", "실제 연구진행률이 계획보다 10%p 이상 낮습니다.",
                       "진행보고서, 지연 원인 및 향후 일정 확인"))
    if period_ended and not mass_production:
        alerts.append(("🟠", "Rule 03", "개발기간이 종료됐으나 양산화 완료가 확인되지 않습니다.",
                       "개발완료 여부 및 양산전환 계획 확인"))
    if mass_production and not performance:
        alerts.append(("🟡", "Rule 04", "양산화 완료 후 관련 제품 성과가 확인되지 않습니다.",
                       "제품별 매출·수익성 및 사후성과 평가 확인"))
    if capitalized and commercialization_delay:
        alerts.append(("🔴", "Rule 05", "개발비가 자산계상된 상태에서 사업화 지연 신호가 있습니다.",
                       "자산인식 근거 및 손상징후 검토"))

    st.subheader("모니터링 결과")
    if alerts:
        for level, rule, msg, action in alerts:
            st.error(f"{level} {rule} | {msg}\n\n확인사항: {action}")
    else:
        st.success("현재 입력값에서는 사전 정의된 주요 이상징후가 탐지되지 않았습니다.")

    st.info(
        "실무 적용 시에는 SAP·전자증빙·연구과제 관리 데이터 등 내부 시스템과 연동해 "
        "Rule 기반으로 확인대상을 추출하는 구조를 가정합니다."
    )

# -----------------------------
# 6. Dashboard
# -----------------------------
elif page == "6. 내부통제 Dashboard":
    st.title("내부통제 Dashboard")

    c1,c2,c3 = st.columns(3)
    c1.metric("2023→2025 R&D 증가", "+18.4%")
    c2.metric("2023→2025 자산계상액 변화", "-76.1%")
    c3.metric("2026 H1 R&D YoY", "+4.7%")

    st.subheader("공개자료에서 확인된 사실")
    st.write("1. 연구개발비 절대 규모는 2023년 이후 증가했습니다.")
    st.write("2. 연구개발비 중 자산계상액과 자산계상 비중은 크게 감소했습니다.")
    st.write("3. 연구과제별 개발기간·진행상황·기대효과·관련제품은 공시에서 일부 확인할 수 있습니다.")

    st.subheader("내부통제 담당자가 추가로 확인할 데이터")
    needs = pd.DataFrame({
        "우선순위":["높음","높음","높음","중간","중간","중간"],
        "내부데이터":[
            "과제별 예산·실제 집행액",
            "지출 증빙·승인 이력",
            "연구진행률·단계별 성과물",
            "양산전환 승인 및 생산실적",
            "관련 제품 매출·수익성",
            "개발비 자산인식·손상 검토자료",
        ],
        "목적":[
            "예산 초과 및 목적 외 집행 확인",
            "거래의 실재성·적정성 확인",
            "일정지연·성과부진 조기 탐지",
            "연구성과의 사업화 연결 확인",
            "R&D의 사후 사업성과 확인",
            "재무정보 신뢰성 확보",
        ]
    })
    st.dataframe(needs, use_container_width=True, hide_index=True)

    st.subheader("프로그램 결론")
    st.success(
        "R&D 비용의 규모만 관리하는 것이 아니라, 연구개발 투자가 승인된 목적에 따라 집행되고 "
        "연구과제의 진행·양산·사업성과와 정확한 회계처리로 연결되는지를 지속적으로 확인해야 합니다. "
        "이상징후를 조기에 식별하고 필요한 증빙과 승인 절차를 확인하는 것이 R&D 성과를 지원하는 "
        "내부통제의 역할이라고 판단했습니다."
    )

    st.caption(
        "※ 본 프로그램은 공개 공시자료와 사용자가 입력하는 시뮬레이션 값을 활용한 지원자 분석 도구이며, "
        "풍산의 실제 내부통제 평가 결과를 의미하지 않습니다."
    )
