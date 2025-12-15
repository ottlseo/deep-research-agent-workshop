import asyncio
from utils.strands_sdk_utils import strands_utils
from prompts.template import apply_prompt_template
from tools.python_repl_tool import python_repl_tool
from tools.bash_tool import bash_tool

agent_name = "toy_agent"

agent = strands_utils.get_agent(
    agent_name=agent_name,
    system_prompts=apply_prompt_template(prompt_name=agent_name, prompt_context={"AGENT_NAME": agent_name}),
    model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0", # 사용할 LLM 모델 ID
    enable_reasoning=False, # 추론 기능 비활성화 (빠른 응답)
    prompt_cache_info=(False, None), # 프롬프트 캐싱 비활성화 (False, None), 활성화 시 (True, "default")
    tool_cache=False, # 툴 캐싱 비활성화
    streaming=True, # 실시간 응답 스트리밍 활성화
    tools=[python_repl_tool, bash_tool]
)

if __name__ == "__main__":
    user_input = "Hello world 를 프린팅하는 파이썬 코드를 작성하고 실행시켜 줄래?"

    async def run_streaming():
        async for event in strands_utils.process_streaming_response_yield(
            agent=agent,
            message=user_input,
            agent_name=agent_name,
            source=agent_name
        ):
            strands_utils.process_event_for_display(event)

    asyncio.run(run_streaming())
