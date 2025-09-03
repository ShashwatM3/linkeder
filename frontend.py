from langchain_openai import ChatOpenAI  # For creating the LLM model instances
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from backend import RAGInstance
from rich.markdown import Markdown
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner

load_dotenv()

llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini")

instance = RAGInstance(
  filenames=["USA_Tech_Student_Profiles.csv"],
  llm=llm
)

console = Console()
with Live(Spinner("dots", text="Inngesting data..."), console=console, refresh_per_second=10):
  instance.inngest()
console.print("[green]Operation complete! Let's get QUERYING..[/green]")
console.print()

while True:
  user_query = input("Query — ")
  if user_query.lower() == 'exit':
    console.print()
    console.print("Thank you!")
    break
  result = instance.query(user_query)
  # context = instance.query(user_query)
  console.print(Markdown(result))
  console.print()
  console.print()