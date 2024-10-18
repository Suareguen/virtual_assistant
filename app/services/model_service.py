import asyncio
from transformers import AutoModelForCausalLM, AutoTokenizer

# Cargar el modelo y el tokenizador
tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModelForCausalLM.from_pretrained("gpt2")

async def generate_text(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    
    # Simular una operación asíncrona con asyncio
    outputs = await asyncio.to_thread(model.generate, **inputs)
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
