import openai
from config import OPENAI_API_KEY

class LLM:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY

    def analyze_text(self, text: str, prompt: str = ""):
        # 프롬프트와 공시 내용을 결합
        messages = [
            {"role": "system", "content": "너는 여의도의 유명한 투자 전문가야. 공시를 읽고 이게 어떻게 도움이 될 것 같은지 생각해서 요약해줘."},
            {"role": "user", "content": f"{prompt}\n\n{text}"}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
