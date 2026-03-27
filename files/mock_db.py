# mock_db.py
# 질병별 식단/습관 데이터 및 사용자 세션 임시 저장소

from datetime import datetime

# ──────────────────────────────────────────────
# 질병별 정적 지식 DB
# ──────────────────────────────────────────────
DISEASE_KNOWLEDGE = {
    "고혈압": {
        "foods_to_avoid": ["짠 음식", "가공식품", "인스턴트 라면", "소시지·햄", "치즈", "절인 채소(김치 과다 섭취)", "술·알코올"],
        "foods_to_eat": ["바나나", "두부", "저지방 유제품", "잎채소(시금치·케일)", "연어·고등어", "귀리", "마늘"],
        "habits": [
            "하루 나트륨 섭취 2,000 mg 이하로 제한",
            "매일 30분 이상 유산소 운동(걷기·수영)",
            "금연 — 흡연은 혈압을 즉각 상승시킵니다",
            "스트레스 관리: 명상·복식호흡 10분/일",
            "충분한 수면(7~8시간)",
            "혈압을 아침·저녁 같은 시각에 측정·기록",
        ],
        "warning": "혈압이 180/120 mmHg 이상이면 즉시 의료기관을 방문하세요.",
    },
    "당뇨": {
        "foods_to_avoid": ["흰 쌀밥(과다)", "설탕·사탕·케이크", "과일 주스·탄산음료", "흰 빵·베이글", "고지방 육류", "술"],
        "foods_to_eat": ["현미·보리·귀리", "콩류(렌틸콩·병아리콩)", "잎채소·브로콜리", "저당 과일(블루베리·사과 소량)", "닭가슴살·생선", "올리브 오일"],
        "habits": [
            "식사 시간을 규칙적으로 유지(3끼 일정한 간격)",
            "식후 15~30분 가벼운 산책으로 혈당 급등 방지",
            "탄수화물 양 일정하게 유지(탄수화물 계산법 활용)",
            "혈당 측정 일지 작성",
            "발 상태 매일 확인(당뇨 합병증 예방)",
            "스트레스·수면 관리(코르티솔이 혈당 올림)",
        ],
        "warning": "저혈당(공복 혈당 70 mg/dL 미만) 증상 시 즉시 당분을 보충하세요.",
    },
    "고지혈증": {
        "foods_to_avoid": ["트랜스 지방(마가린·쇼트닝)", "포화지방(삼겹살·버터·라드)", "새우·오징어(과다)", "전란 노른자(과다)", "튀김류", "술"],
        "foods_to_eat": ["등 푸른 생선(오메가-3)", "견과류(호두·아몬드 소량)", "귀리·보리(베타글루칸)", "사과·배(펙틴)", "올리브 오일", "콩·두부"],
        "habits": [
            "주 5회 이상 유산소 운동 30분",
            "포화지방 섭취 총 칼로리의 7% 이하로 제한",
            "체중 감량(5~10%만 줄여도 LDL 개선)",
            "금연(HDL 콜레스테롤 올라감)",
            "식이섬유 하루 25~30 g 목표",
            "정기적 혈중 지질 검사(6개월~1년)",
        ],
        "warning": "가족성 고콜레스테롤혈증은 식이 조절만으로 부족할 수 있으므로 의사와 상담하세요.",
    },
    "비만": {
        "foods_to_avoid": ["초가공식품·패스트푸드", "액상 칼로리(음료·주스)", "야식", "대용량 간식", "고칼로리 소스·드레싱"],
        "foods_to_eat": ["단백질 위주 식단(닭가슴살·두부·달걀흰자)", "채소·샐러드(포만감)", "통곡물", "물·무가당 차", "저칼로리 과일(방울토마토·오이)"],
        "habits": [
            "하루 500 kcal 결손 목표(주 0.5 kg 감량 속도)",
            "식사 일지 앱으로 칼로리 추적",
            "천천히 먹기(20분 법칙)",
            "규칙적 근력 운동으로 기초대사율 향상",
            "수면 7시간 이상(수면 부족은 식욕 호르몬 증가)",
            "스트레스성 폭식 패턴 인식·대처 전략 마련",
        ],
        "warning": "BMI 35 이상이거나 동반 질환이 있으면 의사·영양사·운동 처방사와 함께 팀 접근을 권장합니다.",
    },
    "위염": {
        "foods_to_avoid": ["맵고 자극적인 음식", "커피·카페인", "술·탄산음료", "기름진 튀김", "빈속 진통제(NSAIDs)", "공복 상태 장시간 유지"],
        "foods_to_eat": ["죽·흰 쌀밥(부드럽게)", "바나나·사과(삶은 것)", "두부·달걀(부드럽게 조리)", "저지방 생선", "감자·고구마(찐 것)", "따뜻한 물·허브차"],
        "habits": [
            "규칙적인 식사(소량씩 자주 — 하루 5~6회)",
            "식사 후 2시간 이내 눕지 않기",
            "금연(위산 분비 촉진)",
            "스트레스 관리(위장-뇌 연결 축)",
            "헬리코박터 균 검사 및 치료 여부 확인",
            "취침 전 3시간 금식",
        ],
        "warning": "검은 변, 피를 토하는 증상 시 즉시 응급실을 방문하세요.",
    },
}

# 지원 질병 목록 (검색용)
SUPPORTED_DISEASES = list(DISEASE_KNOWLEDGE.keys())

# ──────────────────────────────────────────────
# 사용자 세션 임시 저장소 (메모리)
# ──────────────────────────────────────────────
_session_store: dict[str, dict] = {}


def save_session(session_id: str, data: dict) -> None:
    """세션 데이터를 저장합니다."""
    if session_id not in _session_store:
        _session_store[session_id] = {"created_at": datetime.now().isoformat(), "history": []}
    _session_store[session_id].update(data)
    _session_store[session_id]["updated_at"] = datetime.now().isoformat()


def get_session(session_id: str) -> dict:
    """세션 데이터를 불러옵니다. 없으면 빈 dict 반환."""
    return _session_store.get(session_id, {})


def append_history(session_id: str, role: str, content: str) -> None:
    """대화 히스토리를 세션에 추가합니다."""
    if session_id not in _session_store:
        save_session(session_id, {})
    _session_store[session_id].setdefault("history", []).append(
        {"role": role, "content": content, "timestamp": datetime.now().isoformat()}
    )


def list_sessions() -> list[str]:
    """저장된 모든 세션 ID를 반환합니다."""
    return list(_session_store.keys())


def clear_session(session_id: str) -> bool:
    """특정 세션을 삭제합니다."""
    if session_id in _session_store:
        del _session_store[session_id]
        return True
    return False
