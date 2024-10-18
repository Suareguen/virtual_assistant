from ollama import Client
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


memory = ConversationBufferMemory()
client = Client()


async def generate_response(user_input):

    template = """
    Eres un asistente virtual especializado en responder solo sobre los productos y servicios de la tienda de ecommerce "FashionPlus". 
    No debes proporcionar información fuera de este contexto. Si el usuario te hace preguntas no relacionadas con productos, pedidos o políticas de la tienda, simplemente dile que solo puedes responder preguntas relacionadas con "FashionPlus".
    Reglas:
    - Si el usuario pregunta algo fuera de este contexto, responde con: "Lo siento, solo puedo responder preguntas sobre FashionPlus. ¿Cómo puedo ayudarte con algún producto o pedido?"
    - No respondas preguntas que no tengan relación con productos, servicios o políticas de la tienda.

    Historial de conversación:
    {history}

    User: {user_message}
    AI: 
    """
    
    prompt = PromptTemplate(inout_variables=["history", "user_message"], template=template)
    history = memory.load_memory_variables({}).get("history", "")
    prompt_message = prompt.format(history=history, user_message=user_input)
    response = client.generate(prompt=prompt_message, model="llama3.1")

    if response["done"] == True:
        result = response["response"]
        memory.save_context({"input": user_input}, {"output": result})
        return result
    else: 
        print(f"Error al devolver la respues")


