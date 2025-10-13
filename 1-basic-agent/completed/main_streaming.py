import os, sys
# from dotenv import load_dotenv
import asyncio
from utils.strands_sdk_utils import strands_utils
from prompts.template import apply_prompt_template

agent_name = "toy_agent"

user_input = "안녕 만나서 반가워. 나는 지금 Strands Agents SDK 공부중이야."

if __name__ == "__main__":
    
    agent = strands_utils.get_agent(
        agent_name=agent_name,
        system_prompts=apply_prompt_template(prompt_name=agent_name, prompt_context={"AGENT_NAME": agent_name}),
        agent_type="claude-sonnet-3-7", # 사용할 LLM 모델 (고성능 추론) 
        enable_reasoning=False, # 추론 기능 비활성화 (빠른 응답) 
        prompt_cache_info=(False, None), # 프롬프트 캐싱 비활성화 (False, None), 활성화 시 (True, "default") 
        streaming=True, # 실시간 응답 스트리밍 활성화
    )

    async def run_streaming():
        full_text = ""
        async for event in strands_utils.process_streaming_response_yield(
            agent=agent,
            message=user_input,
            agent_name=agent_name,
            source=agent_name
        ):
            strands_utils.process_event_for_display(event)

            if event.get("event_type") == "text_chunk":
                full_text += event.get("data", "")
            
        response = {"text": full_text}

        print (f'\nResponse: {response["text"]}')
    
    asyncio.run(run_streaming())
