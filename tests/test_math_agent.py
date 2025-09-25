import asyncio
from datetime import datetime
from typing import  Any, Union

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from langchain_core.messages import ToolMessage, AIMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# Import the benchmark test cases
from math_agent_test_cases import BENCHMARK_TEST_CASES

load_dotenv()
LLM = ChatOpenAI(model="gpt-4o")
server_params = StdioServerParameters(
    command="python",
    args=["mcp_servers/math_tools.py"]
)

class ConversationCapture:
    """Class to capture and format conversation for output"""
    def __init__(self):
        self.messages = []
        self.steps = []
        self.final_answer = None
        
    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        
    def add_step(self, step: str):
        self.steps.append(step)
        
    def set_final_answer(self, answer: Any):
        self.final_answer = answer
        
    def format_for_output(self) -> str:
        output = "=" * 40
        output += "HUMAN MESSAGE"
        output += "=" * 40 + "\n"
        output += f"{self.messages[0]['content']}\n\n"
        if self.steps:
            output += "=" * 40
            output += f"TOOL USAGE"
            output += "=" * 40 + "\n\n"
            for i, step in enumerate(self.steps, 1):
                output += f"{i}. {step}\n"
            output += "\n"
            
        output += "=" * 40
        output += "FINAL ANSWER"
        output += "=" * 40 + "\n"
        output += f"{self.final_answer}\n\n"
        return output


async def run_test_case(message: str) -> tuple[Any, ConversationCapture]:
    """Run a single test case and capture the conversation"""
    capture = ConversationCapture()
    capture.add_message("user", message)
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session=session)
                
                AGENT = create_react_agent(LLM, tools=tools)
                
                # We'll use the callback mechanism to capture the agent's steps
                
                response = await AGENT.ainvoke({"messages": message})
                for m in response['messages'][:-1]:
                    m.pretty_print()
                    if isinstance(m, Union[ToolMessage, AIMessage]):
                        capture.add_step(m.tool_calls if hasattr(m, "tool_call") else m.content)
                        
                # Extract the final answer from the agent's response
                final_answer = None
                if response and "messages" in response and len(response["messages"]) > 0:
                    ai_message = response["messages"][-1]
                    capture.add_message("assistant", ai_message.content)
                    
                    # Try to extract a numerical answer from the text
                    import re
                    number_pattern = r'[-+]?\d*\.\d+|\d+'
                    matches = re.findall(number_pattern, ai_message.content)
                    if matches:
                        # Take the last number in the response as the answer
                        try:
                            final_answer = float(matches[-1])
                            # Convert to int if it's a whole number
                            if final_answer == int(final_answer):
                                final_answer = int(final_answer)
                        except ValueError:
                            final_answer = None
                
                capture.set_final_answer(final_answer)
                return final_answer, capture
    except Exception as e:
        print(f"Error running test case: {e}")
        capture.add_step(f"ERROR: {str(e)}")
        capture.set_final_answer(None)
        return None, capture


async def run_benchmark_tests():
    """Run all benchmark tests and save results to file"""
    results = {
        "summary": {
            "total_tests": 0,
            "passed_tests": 0,
            "categories": {}
        },
        "details": {}
    }
    
    output_file = f"math_agent_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(output_file, "w") as f:
        f.write(f"MATH AGENT TEST RESULTS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        for category_data in BENCHMARK_TEST_CASES:
            category = category_data["category"]
            test_cases = category_data["test_cases"]
            
            f.write(f"CATEGORY: {category}\n")
            f.write("=" * 80 + "\n\n")
            
            category_results = {
                "total": len(test_cases),
                "passed": 0,
                "tests": []
            }
            
            for test_case in test_cases:
                message = test_case["message"]
                expected = test_case["expected"]
                
                print(f"Running test: {message}")
                actual, capture = await run_test_case(message)
                
                # Check if the test passed
                passed = False
                if expected is None and actual is None:
                    passed = True
                elif expected is not None and actual is not None:
                    # Allow small floating point differences
                    if isinstance(expected, float) or isinstance(actual, float):
                        passed = abs(float(expected) - float(actual)) < 0.0001
                    else:
                        passed = expected == actual
                
                # Update results
                if passed:
                    category_results["passed"] += 1
                
                test_result = {
                    "message": message,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed
                }
                category_results["tests"].append(test_result)
                
                # Write the conversation to file
                f.write(capture.format_for_output())
                f.write(f"EXPECTED: {expected}\n")
                f.write(f"ACTUAL: {actual}\n")
                f.write(f"PASSED: {passed}\n\n")
                f.write("-" * 80 + "\n\n")
            
            # Update summary
            results["summary"]["total_tests"] += category_results["total"]
            results["summary"]["passed_tests"] += category_results["passed"]
            results["summary"]["categories"][category] = {
                "total": category_results["total"],
                "passed": category_results["passed"],
                "pass_rate": f"{(category_results['passed'] / category_results['total']) * 100:.1f}%"
            }
            
            results["details"][category] = category_results
            
            # Write category summary
            f.write(f"CATEGORY SUMMARY: {category}\n")
            f.write(f"Total tests: {category_results['total']}\n")
            f.write(f"Passed tests: {category_results['passed']}\n")
            f.write(f"Pass rate: {(category_results['passed'] / category_results['total']) * 100:.1f}%\n\n")
            f.write("=" * 80 + "\n\n")
        
        # Write overall summary
        overall_pass_rate = (results["summary"]["passed_tests"] / results["summary"]["total_tests"]) * 100
        f.write("OVERALL SUMMARY\n")
        f.write("=" * 80 + "\n")
        f.write(f"Total tests: {results['summary']['total_tests']}\n")
        f.write(f"Passed tests: {results['summary']['passed_tests']}\n")
        f.write(f"Overall pass rate: {overall_pass_rate:.1f}%\n\n")
        
        # Write category breakdown
        f.write("CATEGORY BREAKDOWN\n")
        for category, stats in results["summary"]["categories"].items():
            f.write(f"{category}: {stats['passed']}/{stats['total']} ({stats['pass_rate']})\n")
    
    print(f"Test results saved to {output_file}")
    return results


if __name__ == "__main__":
    asyncio.run(run_benchmark_tests())