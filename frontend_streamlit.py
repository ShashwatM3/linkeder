from langchain_openai import ChatOpenAI  # For creating the LLM model instances
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from backend import RAGInstance
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
import streamlit as st

st.title("Welcome to Linkeder")
st.subheader("Ask questions about the :blue[Linkedin] university student base")
st.text("Note: All data is fake")
st.divider()

# Load environment variables
load_dotenv()

llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

if "instance" not in st.session_state:
  llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")
  st.session_state.instance = RAGInstance(
      filenames=["USA_Tech_Student_Profiles.csv"],
      llm=llm
  )
  with st.spinner("Ingesting data..."):
      st.session_state.instance.inngest()

instance = st.session_state.instance

if "initialized" not in st.session_state:
  with st.spinner("Ingesting data..."):
      instance.inngest()
  st.session_state.initialized = True

if st.session_state.initialized:
  if "messages" not in st.session_state:
      st.session_state.messages = []

  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  # Accept user input
  if user_query := st.chat_input("Say something"):
      # Add user message to chat history
      st.session_state.messages.append({"role": "user", "content": user_query})
      
      # Display user message in chat message container
      with st.chat_message("user"):
          st.markdown(user_query)
      
      # Check for exit condition
      if user_query.lower() == 'exit':
          with st.chat_message("assistant"):
              st.markdown("Thank you!")
          st.session_state.messages.append({"role": "assistant", "content": "Thank you!"})
      else:
        # Get response from RAG instance
        with st.chat_message("assistant"):
          if str(user_query) and len(str(user_query).strip())>2:
            with st.spinner("Thinking..."):
              rewritten_query, result = instance.query(str(user_query))
            st.markdown(rewritten_query)
            st.markdown(result)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": result})