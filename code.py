pip install openai==0.28

'''
1. Program Initialization
Libraries: re, math.pow, requests, googlesearch, and openai.
Purpose: Provide essential functions for regex processing, mathematical computations, internet searches, and API interactions.
'''

import re
from typing import Callable, Dict, Any
from math import pow
from googlesearch import search
import requests
import openai

'''
2. Tool Interface
Define: Tool class with a process method to be implemented by subclasses.
Purpose: Create a common interface for different tools (Math, Internet Search, OpenAI API).
'''

# Define a Tool interface
class Tool:
    def process(self, input_data: Any) -> Any:
        raise NotImplementedError("Subclasses should implement this method")

'''
3. MathTool Class
Step: Implements the process method to securely evaluate mathematical expressions.
Purpose: Solve math-related queries using eval restricted to pow.
'''

# Math Tool for mathematical computations
class MathTool(Tool):
    def process(self, input_data: str) -> Any:
        try:
            # Evaluate the math expression securely
            return eval(input_data, {"__builtins__": None}, {"pow": pow})
        except Exception as e:
            return f"Error in math computation: {str(e)}"

'''
4. InternetSearchTool Class
Step: Uses the googlesearch library to fetch the top result for a search query.
Purpose: Address questions requiring an internet search (e.g., definitions, fact-finding)
'''

# Internet Search Tool
class InternetSearchTool(Tool):
    def process(self, input_data: str) -> Any:
        try:
            # Perform a Google search and return the top result
            results = list(search(input_data, num=1))  # Use 'num' to fetch the top result
            if results:
                # Return the title of the first result
                return f"Top result: {results[0]}"
            else:
                return "No results found."
        except Exception as e:
            return f"Error in internet search: {str(e)}"

'''
5. OpenAITool Class
Step: Uses OpenAI API to respond to conversational or creative queries.
Purpose: Handle generalized or complex queries
'''

# OpenAI API Tool for conversational responses
class OpenAITool(Tool):
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key

    def process(self, input_data: str) -> Any:
        try:
            # Query OpenAI API for a response
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use the latest model
                messages=[{"role": "user", "content": input_data}],
                max_tokens=150
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            return f"Error with OpenAI API: {str(e)}"

'''
6. Intelligent Generative System
Initialization
Combine the tools (math, internet, openai) in a Dict.
Purpose: Provide a centralized system for tool-based query processing.

Tool Selection (determine_tool)
Analyze query using regex to identify the appropriate tool:
MathTool: Regex checks for arithmetic symbols or math-related terms.
InternetSearchTool: Regex checks for WH-questions or famous entities.
OpenAITool: Defaults to handling conversational or general queries.
Purpose: Route the query to the correct tool.

Handle Complex Queries
Parse and split a complex query (e.g., 5 multiplied by 10) into parts, resolve subqueries using appropriate tools, and combine results.
Purpose: Process multi-step operations intelligently.

Process Query
For each query:
Identify the tool using determine_tool.
Call the selected tool’s process method with the query.
Purpose: Central query-processing mechanism
'''

# Combine outputs intelligently
class IntelligentGenerativeSystem:
    def __init__(self, openai_api_key: str):
        self.tools: Dict[str, Tool] = {
            "math": MathTool(),
            "internet": InternetSearchTool(),
            "openai": OpenAITool(openai_api_key)
        }

    def determine_tool(self, query: str) -> Callable[[str], Any]:
        # Regex patterns for tools
        if re.search(r"\d+\s*(\*|\+|\-|\/|\^|pow|raise)\s*\d+", query, re.IGNORECASE):
            return self.tools["math"].process
        elif re.search(r"who|what|when|where|why|how|\bTom Cruise\b|age", query, re.IGNORECASE):
            return self.tools["internet"].process
        else:
            return self.tools["openai"].process  # Use OpenAI for general queries

    def handle_complex_query(self, query: str) -> Any:
        try:
            # Identify subqueries for complex queries
            matches = re.findall(r"([\w\s]+)(?: multiplied by| \* )(\d+)", query)
            if matches:
                first_query, multiplier = matches[0]
                tool = self.determine_tool(first_query)
                if tool:
                    result = tool(first_query)
                    return self.tools["math"].process(f"{result} * {multiplier}")
            return "Query not understood."
        except Exception as e:
            return f"Error in processing complex query: {str(e)}"

    def process_query(self, query: str) -> Any:
        # Handle simple and complex queries
        tool = self.determine_tool(query)
        return tool(query)

    def welcome_message(self):
        print("Welcome to the Intelligent Generative System!")
        print("How may I assist you today? Please enter your query below.")

'''
7. User Interaction (main)
Step 1: Input API Key Prompt the user for their OpenAI API key.
Step 2: Welcome Message Display a welcome message to guide the user.
Step 3: Continuous Query Processing Loop to process user inputs: Take user query as input.
Process the query using process_query.
Display the result.
Ask if the user has additional queries or wants to exit
'''

#main
if __name__ == "__main__":
    openai_api_key = input("Please enter your OpenAI API key: ")
    system = IntelligentGenerativeSystem(openai_api_key)

    # Show the welcome message
    system.welcome_message()

    while True:
        # Ask the user for input
        user_input = input("You: ")

        # Process the user's query
        print(f"Response: {system.process_query(user_input)}\n")

        # Ask if the user has another query
        another_query = input("Do you have any other query? (Y/N): ").strip().lower()
        if another_query == 'y':
            continue
        elif another_query == 'n':
            exit_choice = input("Do you want to exit? (Y/N): ").strip().lower()
            if exit_choice == 'y':
                print("Thank you for using the Intelligent Generative System! Goodbye!")
                break
            else:
                print("Alright, let's continue!")
        else:
            print("Invalid choice. Exiting the system.")
            break
