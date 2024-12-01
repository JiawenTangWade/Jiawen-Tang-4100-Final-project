import openai

openai.api_key = "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"

# Test the available engines (models)
try:
    engines = openai.Engine.list()
    print("以下是当前账户下可用的模型：")
    for engine in engines['data']:
        print(f"- {engine['id']}")
except openai.error.AuthenticationError:
    print("API Key 验证失败，请检查密钥是否正确。")
except Exception as e:
    print(f"发生错误: {str(e)}")
