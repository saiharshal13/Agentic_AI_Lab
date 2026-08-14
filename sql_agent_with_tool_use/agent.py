from langchain_ollama import ChatOllama
from sql_tool import run_sql
import re

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

print("SQL ReAct Agent is ready!")

while True:
    question = input("\nAsk a question (or type exit): ")

    if question.lower() == "exit":
        break

    prompt = f"""
You are a ReAct SQL Agent.

Database table: students
Columns: id, name, department, year

Rules:
- For 4th year students, use WHERE year = 4.
- For counting students, use COUNT(*).
- For names, use SELECT name.
- For department searches, ignore capitalization and spaces.
- Always use the SQL tool.
- Never invent results.

User question:
{question}

Return ONLY this format:

Thought: short reasoning
Action: SQL_QUERY

Example:
Thought: I need the names of 4th year students.
Action: SELECT name FROM students WHERE year = 4;
"""

    response = llm.invoke(prompt).content

    print("\n" + response)

    # Find SQL inside a code block first
    sql_match = re.search(
        r"```sql\s*(.*?)\s*```",
        response,
        re.IGNORECASE | re.DOTALL
    )

    if sql_match:
        query = sql_match.group(1).strip()
    else:
        # Find SELECT statement
        sql_match = re.search(
            r"(SELECT\s+.*?;)",
            response,
            re.IGNORECASE | re.DOTALL
        )

        if not sql_match:
            print("Could not find SQL query.")
            continue

        query = sql_match.group(1).strip()

    print("\nAction: Running SQL Tool...")

    result = run_sql(query)

    print("Observation:", result)

    final_prompt = f"""
User question:
{question}

SQL query:
{query}

Database result:
{result}

Give a short final answer using ONLY the database result.
Do not invent information.
"""

    final_answer = llm.invoke(final_prompt).content

    print("\nFinal Answer:", final_answer)