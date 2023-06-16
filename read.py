import typing
import os
import sys
import shutil

import langchain

#os.environ["OPENAI_API_KEY"] = ""


def load_docs(directory: str="./documents") -> typing.List[langchain.docstore.document.Document]:
    raw_documents = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            if file.endswith('.pdf'):
                print(filepath)
                loader = langchain.document_loaders.UnstructuredPDFLoader(filepath)
                raw_documents.extend(loader.load())
            elif file.endswith('.txt'):
                print(filepath)
                loader = langchain.document_loaders.UnstructuredFileLoader(filepath)
                raw_documents.extend(loader.load())
    return raw_documents

def load_code(directory: str="./code") -> typing.List[langchain.docstore.document.Document]:
    raw_documents = []
    for dirpath, dirnames, filenames in os.walk(directory):
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            if file.endswith('.py') and '/.venv/' not in dirpath:
                try:
                    print(filepath)
                    loader = langchain.document_loaders.TextLoader(
                        filepath,
                        encoding='utf-8'
                    )
                    raw_documents.extend(loader.load())
                except Exception as e:
                    pass
            elif file.endswith('.hpp') or file.endswith('.cpp') or file.endswith('.docs'):
                try:
                    print(filepath)
                    loader = langchain.document_loaders.TextLoader(
                        filepath,
                        encoding='utf-8'
                    )
                    raw_documents.extend(loader.load())
                except Exception as e:
                    pass
    return raw_documents


def read(file_type: str, directory: str) -> None:
    # load documents/code
    raw_documents = []
    if file_type.lower() == "docs":
        raw_documents = load_docs(directory)
    elif file_type.lower() == "code":
        raw_documents = load_code(directory)
    print(f"Number of documents: {len(raw_documents)}")

    # prepare text
    text_splitter = langchain.text_splitter.TokenTextSplitter(
        model_name="text-embedding-ada-002",
        chunk_size=500,
        chunk_overlap=25
    )
    documents = text_splitter.split_documents(raw_documents)
    print(f"Number of texts: {len(documents)}")

    #print('\n')
    #print(documents[0])
    #print('\n')
    #print(documents[1])
    #print('\n')
    #print(documents[2])
    #print('\n')

    # create embedding model
    embedding = langchain.embeddings.openai.OpenAIEmbeddings(
        model="text-embedding-ada-002",
        openai_api_key=os.environ['OPENAI_API_KEY']
    )

    # create vectorstore database
    persist_directory = "./vectorstore"
    if os.path.isdir(persist_directory):
        shutil.rmtree(persist_directory)

    vectorstore = langchain.vectorstores.Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=persist_directory
    )

    vectorstore.persist()


if __name__ == "__main__":
    assert len(sys.argv) == 3, "python read.py <file_type> <directory> where <file_type> can be docs or code"
    file_type = sys.argv[1]
    directory = sys.argv[2]
    read(file_type, directory)