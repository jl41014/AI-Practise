from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    model="meta-llama/llama-4-maverick:free",
    temperature=0.2
)

# 定义响应的结构(JSON)，两个字段 answer和source。
response_schemas = [
    ResponseSchema(name="securityCode", description="security code of the bond"),
    ResponseSchema(name="currency", description="currency of the bond"),
    ResponseSchema(name="price", description="the unit price of the bond"),
    ResponseSchema(name="amount", description="total amount of the bond for an order"),
    ResponseSchema(name="quantity", description="quantity of the bond for an order"),
    ResponseSchema(name="orderRefNum", description="the order reference number of an order")
]
output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

# 获取响应格式化的指令
format_instructions = output_parser.get_format_instructions()

prompt = PromptTemplate(
    template="summarize user's question as best as possible.\n{format_instructions}\n{question}",
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions}
)

response = prompt.format_prompt(question="the order ABCDEFGHIJK is for security ABC123. the security price is 99.00 USD. ABCDEFGHIJK bought 1000 this bond. it total cost 99000")

print(response.to_string())

output = chat.invoke(response.to_string())

print(output_parser.parse(output.content))

# tutorial https://github.com/WTFAcademy/WTF-Langchain/tree/main/01_Hello_Langchain

