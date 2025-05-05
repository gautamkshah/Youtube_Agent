import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Cohere
from dotenv import load_dotenv

load_dotenv()

class YouTubeRAGProcessor:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        self.llm = Cohere(
            cohere_api_key="0TMwPWseVMf56uYE0pLoUuFMCqEk4qbZ1t1AacGQ", 
            model="command", 
            temperature=0.3,
            max_tokens=512
        )

        self.prompt_template = PromptTemplate(
            template="""
            You are a helpful assistant that answers questions about YouTube videos.
            Answer ONLY from the provided transcript context.
            Be concise and accurate.
            
            Transcript Context:
            {context}
            
            Question: {question}
            
            Answer:
            """,
            input_variables=['context', 'question']
        )
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

    def get_transcript(self, video_id: str) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=["en"]
            )
            return " ".join(chunk["text"] for chunk in transcript_list)
        except TranscriptsDisabled:
            raise ValueError("No captions available for this video")
        except Exception as e:
            raise ValueError(f"Error fetching transcript: {str(e)}")

    def process_video(self, video_id: str):
        transcript = self.get_transcript(video_id)
        chunks = self.splitter.create_documents([transcript])
        vector_store = FAISS.from_documents(chunks, self.embeddings)
        return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

    def ask_question(self, retriever, question: str) -> str:
        retrieved_docs = retriever.invoke(question)
        context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
        final_prompt = self.prompt_template.invoke({
            "context": context_text,
            "question": question
        })
        return self.llm.invoke(final_prompt)

if __name__ == "__main__":
    processor = YouTubeRAGProcessor()
    
    video_id = "Gfr50f6ZBvo"  
    retriever = processor.process_video(video_id)
    
    question = "What is the main topic of this video?"
    answer = processor.ask_question(retriever, question)
    print(answer)