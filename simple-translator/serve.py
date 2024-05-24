from typing import List

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv

import uvicorn.server

# Load env vars
load_dotenv()

# Create prompt template
system_template = "Translate following into {language}: "
prompt_template = ChatPromptTemplate.from_messages({
    ('system', system_template),
    ('user', '{text}')
})

# Create model
model = ChatOpenAI()

# Create parser
parser = StrOutputParser()

# Create chain
chain = prompt_template | model | parser

# Define app
app = FastAPI(
    title='LangChain Server',
    version='1.0',
    description="A simple API server using LangChain's Runnable interfaces"
)

# Add chaint to route
add_routes(
    app,
    chain,
    path='/chain'
)

# Start app
if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='localhost', port=8000)
