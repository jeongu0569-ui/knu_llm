# tools.py
# 질병별 식단·습관 조회 및 세션 관리 Tool 정의

import json
from langchain_core.tools import tool
from mock_db import (
    DISEASE_KNOWLEDGE,
    SUPPORTED_DISEASES,
    save_session,
    get_session,
    append_history,
)


@tool
def get_disease_diet_info(disease_name: str) -> str:
    """
    특정 질병의 식단 정보를 조회합니다.
    피해야 할 음식과 권장 음식 목록을 반환합니다.

    Args:
        disease_name: 질병명 (예: 고혈압, 당뇨, 고지혈증, 비만, 위염)
    """
    info = DISEASE_KNOWLEDGE.get(disease_name)
    if not info:
        supported = ", ".join(SUPPORTED_DISEASES)
        return f"'{disease_name}'에 대한 정보가 없습니다. 현재 지원 질병: {supported}"

    result = {
        "질병": disease_name,
        "피해야_할_음식": info["foods_to_avoid"],
        "권장_음식": info["foods_to_eat"],
        "주의사항": info.get("warning", ""),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def get_disease_habit_info(disease_name: str) -> str:
    """
    특정 질병에 대한 생활 습관 개선 방법을 조회합니다.

    Args:
        disease_name: 질병명 (예: 고혈압, 당뇨, 고지혈증, 비만, 위염)
    """
    info = DISEASE_KNOWLEDGE.get(disease_name)
    if not info:
        supported = ", ".join(SUPPORTED_DISEASES)
        return f"'{disease_name}'에 대한 정보가 없습니다. 현재 지원 질병: {supported}"

    result = {
        "질병": disease_name,
        "습관_개선_방법": info["habits"],
        "주의사항": info.get("warning", ""),
    }
    return json.dumps(result, ensure_ascii=False, indent=2)


@tool
def list_supported_diseases() -> str:
    """
    현재 시스템이 지원하는 모든 질병 목록을 반환합니다.
    사용자가 어떤 질병 정보를 물어볼 수 있는지 확인할 때 사용합니다.
    """
    return f"현재 지원 질병 목록: {', '.join(SUPPORTED_DISEASES)}"


@tool
def save_user_profile(session_id: str, age: int, gender: str, diseases: str) -> str:
    """
    사용자의 프로필(나이, 성별, 질병)을 세션에 저장합니다.

    Args:
        session_id: 사용자 세션 ID (예: "user_001")
        age: 나이 (정수)
        gender: 성별 ("남성" 또는 "여성")
        diseases: 질병 목록, 쉼표로 구분 (예: "고혈압,당뇨")
    """
    disease_list = [d.strip() for d in diseases.split(",") if d.strip()]
    profile = {
        "age": age,
        "gender": gender,
        "diseases": disease_list,
    }
    save_session(session_id, {"profile": profile})
    append_history(session_id, "system", f"프로필 저장: {profile}")
    return f"프로필이 저장되었습니다: {json.dumps(profile, ensure_ascii=False)}"


@tool
def get_user_profile(session_id: str) -> str:
    """
    저장된 사용자 프로필을 불러옵니다.

    Args:
        session_id: 사용자 세션 ID
    """
    session = get_session(session_id)
    profile = session.get("profile")
    if not profile:
        return f"세션 '{session_id}'에 저장된 프로필이 없습니다."
    return json.dumps(profile, ensure_ascii=False, indent=2)


# 에이전트에 전달할 tool 목록
ALL_TOOLS = [
    get_disease_diet_info,
    get_disease_habit_info,
    list_supported_diseases,
    save_user_profile,
    get_user_profile,
]
