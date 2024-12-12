from openai import OpenAI
from config import OPENAI_API_KEY

class LLM:
    def __init__(self):
        OpenAI.api_key = OPENAI_API_KEY

    def analyze_text(self, text: str, prompt: str = ""):
        # 프롬프트와 공시 내용을 결합
        messages = [
            {"role": "system", "content": "너는 여의도의 유명한 투자 전문가야. 공시를 읽고 이게 어떻게 도움이 될 것 같은지 생각해서 요약해줘."},
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ]
        try:
            # 메시지 목록을 자동으로 생성해요
            messages = [
                {"role": "system", "content": system_input},
                {"role": "user", "content": user_input}
            ]

            response = OpenAI().chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens  # 최대 토큰 수를 지정해요
            )
            # 생성된 응답을 반환해요
            return response
        except Exception as e:
            return f"Error: {str(e)}"
