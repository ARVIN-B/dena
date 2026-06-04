import os
import json
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


DEFAULT_SYSTEM_MESSAGE = """
You are a helpful AI assistant.
Answer accurately and concisely.
"""


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

    def _build_agent(
        self,
        system_message: str | None = None,
    ):
        return AssistantAgent(
            name="AgentLLM",
            model_client=self.model_client,
            system_message=system_message or DEFAULT_SYSTEM_MESSAGE,
        )

    async def ask(
        self,
        prompt: str,
        system_message: str | None = None,
    ):

        agent = self._build_agent(
            system_message=system_message,
        )

        response = await agent.on_messages(

            messages=[
                TextMessage(
                    content=prompt,
                    source="user",
                )
            ],

            cancellation_token=
            CancellationToken(),
        )

        content = response.chat_message.content

        if isinstance(
            content,
            str,
        ):
            return content

        if hasattr(
            content,
            "model_dump_json",
        ):
            return content.model_dump_json()

        if hasattr(
            content,
            "model_dump",
        ):
            return json.dumps(
                content.model_dump(),
                ensure_ascii=False,
            )

        return str(content)


llm = LLM()


async def ask_llm(
    prompt: str,
    system_message: str | None = None,
):

    return await llm.ask(
        prompt,
        system_message=system_message,
    )
