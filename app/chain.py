from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama


llm = ChatOllama(
    model="llama3-groq-tool-use:latest",
    temperature=0,
    max_tokens=512
)

template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a knowledgeable culinary assistant specializing in providing"
            "detailed cooking recipes. Your responses should be informative, engaging, "
            "and tailored to the user's specific requests. Include ingredients, "
            "step-by-step instructions, cooking times, and any helpful tips or "
            "variations. If asked about dietary restrictions or substitutions, offer "
            "appropriate alternatives.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

chain = template | llm
