import openai

openai.api_key = "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"

# Test the ChatCompletion API
def test_openai_api():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the new ChatCompletion method
            messages=[
                {"role": "system", "content": "你是一个友好的助手。"},
                {"role": "user", "content": "请测试 OpenAI API 的正常运行情况。"}
            ],
            max_tokens=50,
            temperature=0.7
        )
        print("API 调用成功！返回结果如下：")
        print(response['choices'][0]['message']['content'].strip())
    except Exception as e:
        print(f"API 调用失败: {e}")

# Run the test
if __name__ == "__main__":
    test_openai_api()
