CUDA_VISIBLE_DEVICES=1
from flask import Flask, request, jsonify
import torch
from transformers import LlamaForCausalLM, AutoTokenizer, GenerationConfig
from peft import PeftModel

app = Flask(__name__)

device = "cuda"
model_path = 'models/CodeLlama-7b-Instruct-hf'

tokenizer = AutoTokenizer.from_pretrained(model_path)

model = LlamaForCausalLM.from_pretrained(
    "codellama/CodeLlama-7b-Instruct-hf",
    load_in_8bit=True,
    torch_dtype=torch.float16,
    device_map="auto",
)

model = PeftModel.from_pretrained(
    model,
	"zzzghttt/TestGen2-lora",
    torch_dtype=torch.float16,
)

model.eval()

def tokenize(text):
    result = tokenizer(
        text,
        truncation=True,
        max_length=128,
        padding=False,
        return_tensors="pt",
        )
    return result["input_ids"].to(device)

def generate(
        text: str,
        max_tokens: int = 128,
        temperature: float = 0.8,
        ):
    generation_config = GenerationConfig(
            temperature=temperature,
            eos_token_id=2,
            pad_token_id=0,
            )
    input_ids = tokenize(text)
    with torch.no_grad():
        result = model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                output_scores=True,
                max_new_tokens=max_tokens,
                )
    return result

@app.route('/generation', methods=['POST'])
def completion():
    # 获取 JSON 数据
    data = request.json

    # 检查是否有 'input' 字段
    if 'input' not in data:
        return jsonify({'error': 'No input provided'}), 400

    input_str = data['input']
    print("\n[Input]:\n", input_str)

    # 处理输入
    result = generate(input_str)
    # 返回处理后的结果
    return jsonify({'Result': result})

if __name__ == '__main__':
    app.run(debug=True, port=1234, threaded=True)
