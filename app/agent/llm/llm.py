import os
from dotenv import load_dotenv
from autogen_agentchat.agents import (
    AssistantAgent
)
from autogen_agentchat.messages import (
    TextMessage
)
from autogen_ext.models.openai import (
    OpenAIChatCompletionClient
)
from autogen_core.models import (
    ModelInfo
)
from autogen_core import (
    CancellationToken
)


load_dotenv()

class LLM:

    def __init__(self):
        self.model_name = os.getenv(
            "MODEL_NAME"
        )

        self.api_key = os.getenv(
            "OPENROUTER_API_KEY"
        )

        self.model_client = OpenAIChatCompletionClient(

            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
            model=self.model_name,
            temperature=0,
            model_info=ModelInfo(
                vision=False,
                function_calling=False,
                json_output=True,
                family=self.model_name,
                structured_output=False,
            ),
        )

        self.agent = AssistantAgent(
            name="AgentLLM",
            model_client=self.model_client,
            system_message="""
            You are a helpful AI assistant.
            Answer accurately and concisely.
            """,
        )

    async def ask(
        self,
        prompt: str,
    ):

        response = await self.agent.on_messages(

            messages=[
                TextMessage(
                    content=prompt,
                    source="user",
                )
            ],

            cancellation_token=
            CancellationToken(),
        )

        return response.chat_message.content


llm = LLM()