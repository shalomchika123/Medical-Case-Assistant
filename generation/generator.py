import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from config import LLM_MODEL_ID
from generation.prompt import build_prompt

class Generator:
    def __init__(self):
        print(f"[INFO] Loading AI Model: {LLM_MODEL_ID}...")
        
        # Professional 4-bit Quantization Configuration
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
        )

        self.tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_ID)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            LLM_MODEL_ID,
            quantization_config=bnb_config,
            device_map="auto"
        )

    def generate(self, question, retrieved_docs):
        context = "\n\n".join(
            f"Source: {doc.metadata['source']}\n{doc.page_content}"
            for doc in retrieved_docs
        )

        prompt = build_prompt(question, context)
        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

        output = self.model.generate(
            **inputs,
            max_new_tokens=500,
            do_sample=True,
            temperature=0.2,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=self.tokenizer.eos_token_id
        )

        full_response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        # Remove prompt from response (Mistral specific handling can be added here)
        return full_response.replace(prompt, "").strip()