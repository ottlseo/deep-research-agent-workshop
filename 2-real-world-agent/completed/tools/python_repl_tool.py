import sys
import logging
import subprocess
from typing import Any, Annotated
from strands.types.tools import ToolResult, ToolUse
from src.tools.decorators import log_io


# Simple logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TOOL_SPEC = {
    "name": "python_repl_tool",
    "description": "Use this to execute python code and do data analysis or calculation. If you want to see the output of a value, you should print it out with `print(...)`. This is visible to the user.",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The python code to execute to do further analysis or calculation."
                }
            },
            "required": ["code"]
        }
    }
}

class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class PythonREPL:
    def __init__(self):
        pass

    def run(self, command):
        try:
            # 입력된 명령어 실행
            result = subprocess.run(
                [sys.executable, "-c", command],
                capture_output=True,
                text=True,
                timeout=600  # 타임아웃 설정
            )
            # 결과 반환
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Exception: {str(e)}"

repl = PythonREPL()

@log_io
def handle_python_repl_tool(code: Annotated[str, "The python code to execute to do further analysis or calculation."]):
    """
    Use this to execute python code and do data analysis or calculation. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user.
    """
    print()  # Add newline before log
    logger.info(f"{Colors.GREEN}===== Executing Python code ====={Colors.END}")
    try:
        result = repl.run(code)
    except BaseException as e:
        error_msg = f"Failed to execute. Error: {repr(e)}"
        logger.debug(f"{Colors.RED}Failed to execute. Error: {repr(e)}{Colors.END}")
        return error_msg

    # Truncate code to first 7 lines for context efficiency
    code_lines = code.split('\n')
    if len(code_lines) > 7:
        code_preview = '\n'.join(code_lines[:7])
        code_summary = f"{code_preview}\n... ({len(code_lines) - 7} more lines omitted)"
    else:
        code_summary = code

    result_str = f"Successfully executed:\n||{code_summary}||{result}"
    logger.info(f"{Colors.GREEN}===== Code execution successful ====={Colors.END}")
    return result_str

# Function name must match tool name
def python_repl_tool(tool: ToolUse, **kwargs: Any) -> ToolResult:
    tool_use_id = tool["toolUseId"]
    code = tool["input"]["code"]

    # Use the existing handle_python_repl_tool function
    result = handle_python_repl_tool(code)

    # Check if execution was successful based on the result string
    if "Failed to execute" in result:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": result}]
        }
    else:
        return {
            "toolUseId": tool_use_id,
            "status": "success",
            "content": [{"text": result}]
        }
