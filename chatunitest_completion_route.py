from flask import Flask, request, jsonify
from langchain.llms import OpenAI

app = Flask(__name__)

def process_input(llm, prompt):
    # 这里替换为你的字符串处理逻辑
    result = llm(prompt)
    print(prompt)
    print(f"> {result}")
    print("\n==================================\n")
    return result

@app.route('/v1/completions', methods=['POST'])
def completion():
    # 获取 JSON 数据
    data = request.json

    frequency_penalty = data['frequency_penalty'] if 'frequency_penalty' in data else 0
    max_tokens = data['max_tokens'] if 'max_tokens' in data else 512
    presence_penalty = data['presence_penalty'] if 'presence_penalty' in data else 0
    temperature = data['temperature'] if 'temperature' in data else 0.5
    messages = data['messages'] if 'messages' in data else []
    model = data['model'] if 'model' in data else 'gpt-3.5-turbo'

    if messages == []:
        return jsonify({'error': 'No messages provided'}), 400

    llm = OpenAI(
        model_name=model,
        openai_api_base="http://127.0.0.1:1234/generation",
        openai_api_key="xxx",
        max_tokens=max_tokens,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    print(llm)

    # 处理输入
    input_str = ''
    for msg in messages:
        input_str += msg['content']

    result = process_input(llm, input_str)

    # 返回处理后的结果
    return jsonify({'choices': [{'message': {'content': result}}]})

if __name__ == '__main__':
    app.run(debug=True, port=8000, threaded=True)
