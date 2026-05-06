import llm_lens
import openai

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "say hi in 5 words"}]
)
print(response.choices[0].message.content)
