


"""
Entry point script for the Strands Agent Demo.
"""
import os
import shutil
import asyncio
import argparse
from dotenv import load_dotenv
from utils.strands_sdk_utils import strands_utils
from graph.builder import build_graph

# Load environment variables
load_dotenv()

# Import event queue for unified event processing
from utils.event_queue import clear_queue 

def remove_artifact_folder(folder_path="./artifacts/"):
    """
    ./artifact/ 폴더가 존재하면 삭제하는 함수

    Args:
        folder_path (str): 삭제할 폴더 경로
    """
    if os.path.exists(folder_path):
        print(f"'{folder_path}' 폴더를 삭제합니다...")
        try:
            shutil.rmtree(folder_path)
            print(f"'{folder_path}' 폴더가 성공적으로 삭제되었습니다.")
        except Exception as e: print(f"오류 발생: {e}")
    else:
        print(f"'{folder_path}' 폴더가 존재하지 않습니다.")

def _setup_execution():
    """Initialize execution environment"""
    remove_artifact_folder()
    clear_queue()
    print("\n=== Starting Queue-Only Event Stream ===")

def _print_conversation_history():
    """Print final conversation history"""
    print("\n=== Conversation History ===")
    from graph.nodes import _global_node_states
    shared_state = _global_node_states.get('shared', {})
    history = shared_state.get('history', [])

    if history:
        for hist_item in history:
            print(f"[{hist_item['agent']}] {hist_item['message']}")
    else:
        print("No conversation history found")

async def graph_streaming_execution(payload):
    """Execute full graph streaming workflow using new graph.stream_async method"""

    _setup_execution()

    # Get user query from payload
    user_query = payload.get("user_query", "")
        
    # Build graph and use stream_async method
    graph = build_graph()
    
    #########################
    ## modification START  ##
    #########################

    # Stream events from graph execution
    async for event in graph.stream_async(
        {
            "request": user_query,
            "request_prompt": f"Here is a user request: <user_request>{user_query}</user_request>"
        }
    ):
        yield event

    #########################
    ## modification END    ##
    #########################
    
    _print_conversation_history()
    print("=== Queue-Only Event Stream Complete ===")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Strands Agent Demo')
    parser.add_argument('--user_query', type=str, help='User query for the agent')
    
    args, unknown = parser.parse_known_args()

    #########################
    ## modification START  ##
    #########################

    # Use argparse values if provided, otherwise use predefined values
    if args.user_query:
        payload = {
            "user_query": args.user_query,
        }
    else:
        # Full comprehensive analysis query (main version):
        payload = {
            "user_query": """
                            나는 Yummy food의 마케팅 담당자야. 우리회사에서 만든 식품을 여러 매체에 광고하고 있어. 데이터의 종류는 소비자 구매 이력이 있는 데이터, 매체별 광고 데이터야.
                            소비자 구매 패턴과 함께 소비자 분석, 광고 분석 보고서를 pdf로 작성해줘.

                            보고서를 작성할 때는 다음 내용들을 포함해서 작성해.
                            1/ 우리회사에서 만든 식품을 여러 매체에 광고하고 있어. 우리 상품에 대한 분석을 하고 소비자 분석을 하고 싶어. 
                            2/ 광고 매출에 대한 인사이트는 보고서의 맨 앞에 \"x억원의 광고 집행 예산을 4개의 매체(예: 아마존, 컬리, 네이버, 쿠팡)에 n일동안 카테고리(신선식품, 간편식, 건강식품)에 대하여 광고를 집행한 결과입니다. 종합해보면..\"과 같은 개요를 작성해줘. 
                            3/ 어떤 상품이 어떤 소비자에게 인기가 있었는지도 분석해줘. 
                            4/ 통합 분석한 내용을 pdf 리포트로 작성해줘. 분석대상은 './data/*' 파일 이야.
                        """
        }

    #########################
    ## modification END    ##
    #########################

    remove_artifact_folder()

    # Use full graph streaming execution for real-time streaming with graph structure
    async def run_streaming():
        async for event in graph_streaming_execution(payload):
            strands_utils.process_event_for_display(event)

    asyncio.run(run_streaming())


# """
# Entry point script for the Strands Agent Demo.
# """
# import os
# import shutil
# import asyncio
# import argparse
# from dotenv import load_dotenv
# from utils.strands_sdk_utils import strands_utils
# from graph.builder import build_graph

# # Load environment variables
# load_dotenv()

# # Observability
# from opentelemetry import trace, context
# from utils.agentcore_observability import set_session_context, add_span_event

# # Import event queue for unified event processing
# from utils.event_queue import clear_queue 

# def remove_artifact_folder(folder_path="./artifacts/"): # ./artifact/ 폴더가 존재하면 삭제하는 함수
#     if os.path.exists(folder_path):
#         print(f"'{folder_path}' 폴더를 삭제합니다...")
#         try:
#             shutil.rmtree(folder_path)
#             print(f"'{folder_path}' 폴더가 성공적으로 삭제되었습니다.")
#         except Exception as e: print(f"오류 발생: {e}")
#     else:
#         print(f"'{folder_path}' 폴더가 존재하지 않습니다.")

# def _setup_execution(): # Initialize execution environment
#     remove_artifact_folder()
#     clear_queue()
#     print("\n=== Starting Queue-Only Event Stream ===")


# def _print_conversation_history(): # Print final conversation history
#     print("\n=== Conversation History ===")
#     from graph.nodes import _global_node_states
#     shared_state = _global_node_states.get('shared', {})
#     history = shared_state.get('history', [])

#     if history:
#         for hist_item in history:
#             print(f"[{hist_item['agent']}] {hist_item['message']}")
#     else:
#         print("No conversation history found")

# async def graph_streaming_execution(payload): # Execute full graph streaming workflow using new graph.stream_async method
#     _setup_execution()

#     # Get user query from payload
#     user_query = payload.get("user_query", "")
#     session_id = payload.get("session-id", "default")
#     context_token = set_session_context(session_id)

#     try:
#         # Get tracer for main application
#         tracer = trace.get_tracer(
#             instrumenting_module_name=os.getenv("TRACER_MODULE_NAME", "insight_extractor_agent"),
#             instrumenting_library_version=os.getenv("TRACER_LIBRARY_VERSION", "1.0.0")
#         )
#         with tracer.start_as_current_span("insight_extractor_session") as span:   
            
#             # Build graph and use stream_async method
#             graph = build_graph()
            
#             # Stream events from graph execution
#             async for event in graph.stream_async(
#                 {
#                     "request": user_query,
#                     "request_prompt": f"Here is a user request: <user_request>{user_query}</user_request>"
#                 }
#             ):
#                 yield event

#             _print_conversation_history()
#             print("=== Queue-Only Event Stream Complete ===")

#             # Add Event
#             add_span_event(span, "user_query", {"user-query": str(user_query)}) 

#     finally:
#         context.detach(context_token)

# if __name__ == "__main__":
#     # Parse command line arguments
#     parser = argparse.ArgumentParser(description='Strands Agent Demo')
#     parser.add_argument('--user_query', type=str, help='User query for the agent')
#     parser.add_argument('--session_id', type=str, default='insight-extractor-1', help='Session ID')

#     args, unknown = parser.parse_known_args()
    
#     # Use argparse values if provided, otherwise use predefined values
#     if args.user_query:
#         payload = {
#             "user_query": args.user_query,
#             "session-id": args.session_id
#         }
#     else:
#         # Full comprehensive analysis query (main version):
#         payload = {
#             "user_query": "너가 작성할 것은 moon market 의 판매 현황 보고서야. 세일즈 및 마케팅 관점으로 분석을 해주고, 차트 생성 및 인사이트도 뽑아서 pdf 파일로 만들어줘. 분석대상은 './data/Dat-fresh-food-claude.csv' 파일 입니다.",
#             "session-id": "insight-extractor-1"
#         }
#     remove_artifact_folder()

#     # Use full graph streaming execution for real-time streaming with graph structure
#     async def run_streaming():
#         async for event in graph_streaming_execution(payload):
#             strands_utils.process_event_for_display(event)

#     asyncio.run(run_streaming())
