from groq import Groq
from config.config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key="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")

def generate_response(prompt):

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content