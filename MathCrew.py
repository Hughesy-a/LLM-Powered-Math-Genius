from textwrap import dedent
from crewai import Agent, Task, Crew
from tools import ExaSearchToolset
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

# Call Gemini model
llm = ChatGoogleGenerativeAI(
    model='gemini-1.5-pro',
    verbose=True,
    temperature=0.8,
    google_api_key=os.getenv('GOOGLE_API_KEY')
)

true = "true"

class MathAgents:
    def math_genius_agent1(self):
        return Agent(
            role="Mathematical Genius",
            goal="Solve any math problem you see",
            tools=ExaSearchToolset.tools(),
            backstory=dedent("""\
                You're a mathematical genius with a passion for solving complex problems. 
                Your expertise lies in tackling challenging mathematical equations, 
                analyzing data sets, and deriving insights from numerical data."""),
            verbose=True,
            llm=llm
        )
    
    def math_genius_agent2(self):
        return Agent(
            role="Mathematical Genius",
            goal="Solve any math problem you see",
            tools=ExaSearchToolset.tools(),
            backstory=dedent("""\
                You're a mathematical genius with a passion for solving complex problems. 
                Your expertise lies in tackling challenging mathematical equations, 
                analyzing data sets, and deriving insights from numerical data."""),
            verbose=True,
            llm=llm
        )
    
    def another_equation_decider(self):
        return Agent(
            role="Next Step Decider",
            goal="Decide if there is another equation to solve based on the response of the user",
            backstory=dedent("""\
                You are the next step decider. Based on the user input, you will decide on whether 
                the user wants to add something to the equation or not. To do this you will either 
                respond with 'true' or 'false' as an answer."""),
            verbose=True,
            llm=llm
        )

class MathTasks:
    def math_problem_task1(self, agent, equation):
        return Task(
            description=dedent(f"""\
                Your task is to solve the following math problem:

                Equation: {equation}"""),
            expected_output=dedent("The equation and solution to the math problem"),
            agent=agent,
        )
    
    def math_problem_task2(self, agent, equation, user_input):
        return Task(
            description=dedent(f"""\
                If and only if there is additional input from the user, then your task is to solve the following math problem. 
                If there is no additional input from the user, then end your task here.

                Equation: {equation}
                User Input: {user_input}"""),
            expected_output=dedent("The equation and solution to the math problem if user input is provided. If no user input is provided, then end your task here."),
            agent=agent
        )
    
    def deciding_task(self, agent, user_input):
        return Task(
            description=dedent(f"""\
                Based on the user input, you will decide on whether 
                the user wants to add something to the equation or not. 

                User Input: {user_input}"""),
            expected_output=dedent("To do this you will either respond with 'true' or 'false' as an answer."),
            agent=agent
        )
    




    
def run():
    equation = input("Enter a math problem: \n")

    tasks = MathTasks()
    agents = MathAgents()

    # Create agent
    math_genius_agent1 = agents.math_genius_agent1()
    math_genius_agent2 = agents.math_genius_agent2()
    another_equation_decider = agents.another_equation_decider()

    # Create tasks
    math_problem_task1 = tasks.math_problem_task1(math_genius_agent1, equation)

    # Create Crew
    crew1 = Crew(
        agents=[math_genius_agent1],
        tasks=[math_problem_task1]
    )

    result1 = crew1.kickoff()
    print("result from crew1")
    print(result1)
    input2 = input("Are there any changes you wish to make?:")

    deciding_task = tasks.deciding_task(agents.another_equation_decider(), input2)
    crew2 = Crew(
        agents=[another_equation_decider],
        tasks=[deciding_task]
    )
    
    if (crew2.kickoff() == "true"):
        math_problem_task2 = tasks.math_problem_task2(math_genius_agent2, equation, input2)
        math_problem_task2.context = [math_problem_task1]

        crew3 = Crew(
            agents=[math_genius_agent2],
            tasks=[math_problem_task2]
        )

        
        result2 = crew3.kickoff()
        print("Here is the Final Result:")
        print(result2)
    else:
        print("Here is the Final Result:")
        print(result1)    

if __name__ == '__main__':
    run()
