from pydantic import BaseModel, Field # For creating data models for structured output
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
import pandas as pd
import re
import json

class RAGInstance:
  def __init__(self, filenames, llm):
    self.files = filenames
    self.vectorstore = None
    self.llm = llm
    self.conversation_history = []
  
  def inngest(self):
    embeddings = OpenAIEmbeddings()
    chunks = []
    for file in self.files:
      df = pd.read_csv(file)
      for index, row in df.iterrows():
        chunk_text = f"""
        Student name: {row['Name']}
        University name: {row['University']}
        Major: {row['Major']}
        Graduation Year: {row['Graduation Year']}
        Skills: {row['Skills']}
        Achievements: {row['Achievements']}
        Experience: {row['Experience']}
        Email ID: {row['Email ID']}
        """
        doc = Document(page_content=chunk_text.strip())
        chunks.append(doc)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    self.vectorstore = vectorstore

  def query(self, query):
    if self.vectorstore is None:
        raise ValueError("Vectorstore not initialized. Did you call inngest()?")
    self.conversation_history.append({"role": "user", "content": query})

    # Helper: robustly interpret LLM classifier output
    def _parse_rewritten_output(output: str):
      """
      Accepts potentially messy model output and returns one of:
        {"mode": "follow_up"}
        {"mode": "follow_up_search", "search": "..."}
        {"mode": "new", "keywords": "..."}

      Tolerates:
        - Extra lines, code fences, backticks
        - Plain strings like "python students"
        - Literal follow_up token in any casing
        - JSON object containing follow_up_search even if mixed in text
      """
      import re
      s = (output or "").strip()
      # Strip code fences/backticks
      s = re.sub(r"^```[a-zA-Z]*\n|\n```$", "", s).strip()
      s = s.replace("```", "").strip()

      lower = s.lower()
      # 1) If it clearly indicates follow_up (standalone token somewhere)
      if re.search(r"\bfollow_up\b", lower):
        # But prefer follow_up_search if a JSON object is present
        pass

      # 2) Try to extract a JSON object that contains follow_up_search
      json_obj_match = re.search(r"\{[\s\S]*?\}\s*$", s)
      if json_obj_match:
        json_candidate = json_obj_match.group(0)
        try:
          obj = json.loads(json_candidate)
          if isinstance(obj, dict) and "follow_up_search" in obj:
            val = obj["follow_up_search"]
            if isinstance(val, str) and val.strip():
              return {"mode": "follow_up_search", "search": val.strip()}
        except Exception:
          pass

      # 3) Sometimes the line with follow_up_search is missing a closing brace
      line_match = re.search(r"\{\s*\"follow_up_search\"\s*:\s*\"([^\"]+)\"", s)
      if line_match:
        return {"mode": "follow_up_search", "search": line_match.group(1).strip()}

      # 4) If contains follow_up token (and no valid JSON), treat as follow_up
      if re.search(r"\bfollow_up\b", lower):
        return {"mode": "follow_up"}

      # 5) Otherwise, try to pick a quoted string as keywords
      quoted = re.findall(r'"([^\"]+)"', s)
      if quoted:
        return {"mode": "new", "keywords": quoted[0].strip()}

      # 6) Fallback: use the whole string as keywords
      return {"mode": "new", "keywords": s.strip('"`').strip()}

    if len(self.conversation_history) >= 3:
      last_query = self.conversation_history[-3]["content"]
      recent_history = json.dumps(self.conversation_history[-2:])
    else:
      last_query = ""
      recent_history = ""
    
    # Rewriting the query to be 'searchable'
    def generateRewritten():
      rewritten_query = self.llm.invoke(f"""
    You are a query classifier and rewriter for a student profile search system. The system includes structured student data with:
    - Name, University, Major, Graduation Year, Skills, Achievements, Experience, Email ID.

    ---

    ### 🔧 Your task:

    Classify each user query into one of three types:

    1. **"new"** → A brand new query. Generate a 4–5 keyword **search query string**.
    2. **"follow_up_search"** → A follow-up that depends on previous context AND needs a vector database search.
    3. **"follow_up"** → A follow-up question that ONLY relies on the previous assistant response (no new search needed).

    ---

    ### 📌 Rules:

    - If **no valid prior assistant + user message history**, it is always `"new"`.
    - Use `"follow_up"` only when the answer can be fully derived from the previous assistant reply (e.g. pronouns, "what about them", clarifications).
    - Use `"follow_up_search"` when the follow-up **references earlier students** but needs new search info (e.g. asking for new attributes like "Do they have startup experience?").
    - Use `"new"` for queries that **change the scope**, even if they sound conversational (e.g. “Cool, now show me…”).

    ---

    ### ✅ Multi-turn Examples:

    #### 🔄 Example 1 — Basic New → Follow-up (no search needed)

    **Turn 1:**
    User: "List students with Python and JavaScript skills"  
    Assistant: (shows matching profiles)  

    **Turn 2:**
    User: "What about their leadership experience?"  
    → Output: `"follow_up"`

    ---

    #### 🔄 Example 2 — New → Follow-up with new vector search

    **Turn 1:**
    User: "Find students skilled in machine learning and deep learning"  
    Assistant: (shows results)  

    **Turn 2:**
    User: "Do they have any startup experience?"  
    → Output: `{{"follow_up_search": "startup experience machine learning deep learning"}}`

    ---

    #### 🔄 Example 3 — Follow-up that shouldn't be

    **Turn 1:**
    User: "Show students from Stanford"  
    Assistant: (shows profiles)

    **Turn 2:**
    User: "Now give me students from MIT"  
    → Output: `"mit university students"`

    > 🔍 Although this is conversational ("Now give me..."), it is a NEW query — different university, different search.

    ---

    #### 🔄 Example 4 — Long chain, shift in topic

    **Turn 1:**
    User: "Show me data science students from Harvard"  
    Assistant: (returns results)

    **Turn 2:**
    User: "Do they have internships?"  
    → Output: `{{"follow_up_search": "internship experience data science harvard"}}`

    **Turn 3:**
    User: "Cool, now find students with cybersecurity experience from Purdue"  
    → Output: `"cybersecurity experience purdue university"`

    > 💡 Turn 3 is a NEW query even though it's part of the same thread.

    ---

    #### 🔄 Example 5 — No context, must be NEW

    **Turn 1:**
    User: "Give me students who have worked at Google for software development"  
    (No prior history)  
    → Output: `"google software development experience"`

    ---

    ### 🧾 Input:

    - Current user query: {query}
    {f"- Last query was: {last_query}" if last_query else ""}
    {f"- Conversation history: {recent_history}" if recent_history else ""}

    ---

    ### 💬 Output format:

    - If it's a **follow-up with no new search needed**, return exactly: `follow_up`
    - If it's a **follow-up that needs search**, return: `{{"follow_up_search": "<your query>"}}`
    - If it's a **new query**, return the 4–5 word searchable string: `"<your query>"`

    Classify now:
    """).content.strip()
      return rewritten_query
    
    rewritten_query = generateRewritten()
    parsed = _parse_rewritten_output(rewritten_query)
    if parsed.get("mode") == "follow_up_search":
      search_query = parsed["search"]
      # Retrieving beneficial context from database
      context = self.vectorstore.similarity_search_with_score(search_query, k=10)

      # Summing up the context into a string
      context_stringified = """"""
      for retrievedDoc in context:
        if float(retrievedDoc[1])<0.50:
          context_stringified += f"{retrievedDoc[0].page_content}\nHit score: {str(retrievedDoc[1])}\n\n"

      # Invoking LLM
      result = self.llm.invoke(f"""
        You are a student profile assistant helping with recruitment and connections.
        
        Available context:
        {context_stringified}
        
        Conversation history:
        {json.dumps(self.conversation_history)}  # Keep more context
        
        Current query: {query}
        
        Instructions:
        1. Answer based on the available context
        2. For follow-up questions (using "they", "them", etc.), refer to the students from the previous response
        3. When evaluating suitability (like for startups), consider:
            - Relevant technical skills
            - Experience that translates to the domain
            - Major/background alignment
            - Demonstrated initiative or leadership
        4. Be specific about why the profiles match the query
        5. If you cannot find relevant information, explain what's missing
        6. For questions about interests/likelihood, make reasonable inferences from their background
        
        Current query: {query}
      """).content
    elif parsed.get("mode") == "follow_up":
      result = self.llm.invoke(f"""
        You are a student profile assistant helping with recruitment and connections.
        
        Conversation history:
        {json.dumps(self.conversation_history)}
        
        Current query: {query}

        The user has asked a follow up question to the previous assistant reply.
        Use the conversation history as context to produce a reply back to the user
        
        Instructions:
        1. Answer based on the available context
        2. For follow-up questions (using "they", "them", etc.), refer to the students from the previous response
        3. When evaluating suitability (like for startups), consider:
            - Relevant technical skills
            - Experience that translates to the domain
            - Major/background alignment
            - Demonstrated initiative or leadership
        4. Be specific about why the profiles match the query
        5. If you cannot find relevant information, explain what's missing
        6. For questions about interests/likelihood, make reasonable inferences from their background
      """).content
    else:
      # Retrieving beneficial context from database
      keywords = parsed.get("keywords", rewritten_query)
      context = self.vectorstore.similarity_search_with_score(keywords, k=10)

      # Summing up the context into a string
      context_stringified = """"""
      for retrievedDoc in context:
        if float(retrievedDoc[1])<0.45:
          context_stringified += f"{retrievedDoc[0].page_content}\nHit score: {str(retrievedDoc[1])}\n\n"

      # Invoking LLM
      result = self.llm.invoke(f"""
        You are a student profile assistant helping with recruitment and connections.
        
        Available context:
        {context_stringified}
        
        Conversation history:
        {json.dumps(self.conversation_history)}  # Keep more context
        
        Current query: {query}
        
        Instructions:
        1. Answer based on the available context
        2. For follow-up questions (using "they", "them", etc.), refer to the students from the previous response
        3. When evaluating suitability (like for startups), consider:
            - Relevant technical skills
            - Experience that translates to the domain
            - Major/background alignment
            - Demonstrated initiative or leadership
        4. Be specific about why the profiles match the query
        5. If you cannot find relevant information, explain what's missing
        6. For questions about interests/likelihood, make reasonable inferences from their background
        
        Current query: {query}
      """).content
    
    self.conversation_history.append({"role": "assistant", "content": result})
    return [rewritten_query, result]