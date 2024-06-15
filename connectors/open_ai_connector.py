from typing import List, Dict
import openai
import os


# Default Model Params

MODEL_TEMPERATURE = 0
REPLY_MAX_TOKENS = 1000


class OpenaiConnector:
    def __init__(self, api_key: str, model: str) -> None:
        """
        Initializes an instance of OpenaiManager.

        Args:
            api_key (str): API key for OpenAI.
        """
        os.environ["OPENAI_API_KEY"] = api_key
        openai.api_key = os.environ["OPENAI_API_KEY"]
        self.total_tokens_consumed = 0
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model

    def update_cost(self, tokens_consumed: int) -> None:
        """
        Updates the total tokens consumed and total USD spent.

        Args:
            tokens_consumed (int): Number of tokens consumed in the API call.
        """
        self.total_tokens_consumed += tokens_consumed

    def get_gpt_reply(self,
                      prompt: List[Dict[str, str]],
                      temperature: float = MODEL_TEMPERATURE,
                      max_tokens: int = REPLY_MAX_TOKENS) -> str:
        """Generates a GPT reply based on the given prompt.

        Args:
            prompt (List[Dict[str, str]]): A list of messages in the conversation prompt.
            model (str): The model to use for generating the reply. Defaults to OPEN_AI_MODEL.
            temperature (float): Controls the randomness of the reply. Higher values make the output more random. Defaults to MODEL_TEMPERATURE.
            max_tokens (int): The maximum number of tokens in the generated reply. Defaults to REPLY_MAX_TOKENS.
            top_p (float): Controls the diversity of the reply. Higher values make the output more focused. Defaults to MODEL_TOP_P.
            frequency_penalty (float): Controls the penalty for frequently used tokens. Higher values discourage repetition. Defaults to MODEL_FREQUENCY_PENALTY.
            presence_penalty (float): Controls the penalty for new tokens based on their presence in the prompt. Higher values discourage introducing new topics. Defaults to MODEL_PRESENCE_PENALTY.

        Returns:
            str: The generated GPT reply.
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=prompt,
            temperature=temperature,
            max_tokens=max_tokens,


        )

        # self.update_cost(response.usage['total_tokens'])
        return response.choices[0].message.content

