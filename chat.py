import typing
import os

import langchain

os.environ["OPENAI_API_KEY"] = ""


class Chat():
    def __init__(self) -> None:
        # create embedding model
        embedding_function = langchain.embeddings.openai.OpenAIEmbeddings(
            model="text-embedding-ada-002",
            openai_api_key=os.environ["OPENAI_API_KEY"]
        )

        # load vectorstore database, make an empty one if it doesn't exist
        persist_directory = "./vectorstore"
        if not os.path.isdir(persist_directory):
            os.mkdir(persist_directory)

        vectorstore = langchain.vectorstores.Chroma(
            embedding_function=embedding_function,
            persist_directory=persist_directory
        )

        retriever = vectorstore.as_retriever(
            search_type="mmr", # max marginal relevance
            search_kwargs={"k": 10}
        )

        # create llm
        llm = langchain.chat_models.ChatOpenAI(
            openai_api_key=os.environ["OPENAI_API_KEY"],
            model_name="gpt-3.5-turbo-16k",
            temperature=0.0
        )

        # create chat memory
        memory = langchain.memory.ConversationBufferWindowMemory(
            memory_key="chat_history",
            k=5,
            return_messages=True
        )

        # create qa chain
        qa = langchain.chains.ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            memory=memory
        )

        self.embedding_function = embedding_function
        self.vectorstore = vectorstore
        self.retriever = retriever
        self.llm = llm
        self.memory = memory
        self.qa = qa

    def __call__(
        self,
        query: str
    ) -> typing.Dict[str, str]:
        return self.qa(query)


from termcolor import colored

if __name__ == "__main__":
    bot = Chat()
    print(f"{colored('Librarian', 'blue')}\nHello! How can I assist you today?\n")
    while(1):
        query = input(f"{colored('--', 'green')}")
        if "goodbye" in query.lower() or "good bye" in query.lower():
            break
        result = bot(query)
        print(f"\n{colored('Librarian:', 'blue')}\n{result['answer']}\n")