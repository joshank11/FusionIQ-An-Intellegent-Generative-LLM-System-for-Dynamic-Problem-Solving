**FusionIQ: An Intellegent Generative LLM System for Dynamic Problem Solving**

This is an **Intelligent Generative LLM System** that is capable of taking a request coming in from the user and then using the right set of tools to solve the problem of the user. 
So for example, if a user asks a question "How rich is Warren Buffett", the system knows it needs to lookup the internet and get the answer from an internet search made available to the LLM.
If the user asks a math question "What is 23 raise to 3" then it knows it needs to send this request to a _Math Tool_ for processing, and then the LLM should read the processed outputs and respond to the user.
This intelligent system is capable of handling more complex user requests which are a _combination of two or more tools_, 
so for example, for the user query "Tell me Tom Cruise's wife's age multiplied by 74", the system first uses the _internet search tool_ to get Tom Cruise's wife's age and then multiply that by 74 by _math tool_ to give the final response.
