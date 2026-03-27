# main.py
# 건강 케어 에이전트 실행 진입점

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agents import get_health_care_agent

load_dotenv()


def get_final_output(result: dict) -> str:
    """LangGraph 결과에서 마지막 AI 메시지를 추출합니다."""
    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.__class__.__name__ == "AIMessage":
            return msg.content
    return str(result)


def main():
    # .env 파일에 OPENAI_API_KEY가 있어야 합니다.
    model = ChatOpenAI(model="gpt-5-mini", temperature=0)
    care_agent = get_health_care_agent(model)

    user_input = "60세 여성이고 고혈압이 있어요. 평소에 어떤 음식을 조심해야 하고, 어떤 습관을 가지면 좋을까요?"

    result = care_agent.invoke({
        "messages": [{"role": "user", "content": user_input}]
    })

    print("\n" + "=" * 50)
    print("AI 케어 매니저의 제안:")
    print(get_final_output(result))


# ──────────────────────────────────────────────
# 대화형 모드 (선택 실행)
# ──────────────────────────────────────────────
def interactive():
    """터미널에서 반복 질문을 주고받는 대화형 모드."""
    model = ChatOpenAI(model="gpt-5-mini", temperature=0)
    care_agent = get_health_care_agent(model)

    print("=" * 50)
    print("  AI 건강 케어 매니저  ")
    print("  종료하려면 'quit' 또는 'exit' 입력  ")
    print("=" * 50)

    while True:
        user_input = input("\n질문: ").strip()
        if user_input.lower() in ("quit", "exit", "종료"):
            print("이용해 주셔서 감사합니다. 건강하세요!")
            break
        if not user_input:
            continue

        result = care_agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })

        print("\n" + "-" * 50)
        print("AI 케어 매니저:", get_final_output(result))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive()
    else:
        main()
