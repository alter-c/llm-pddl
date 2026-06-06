import os
from openai import OpenAI
from typing import Optional

class LLM:
    def __init__(
        self, 
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        temperature: float = 0.0,
        timeout: int = 300,
        **kwargs
    ):
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.kwargs = kwargs

        self.provider = self._detect_provider(self.model)
        self.api_key, self.base_url = self._resolve_credentials(
            self.provider, api_key, base_url
        )
        self.client = self._create_client()
    
    def _detect_provider(self, model: str) -> str:
        if "deepseek" in model.lower():
            return "deepseek"
        elif "gpt" in model.lower():
            return "openai"
        elif "qwen" in model.lower():
            return "qwen"
        else:
            raise ValueError(f"{model} not supported.")
    
    def _resolve_credentials(
            self, 
            provider: str, 
            api_key: Optional[str], 
            base_url: Optional[str]
        ) -> tuple[str, str]:
        if provider == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            base_url = "https://api.deepseek.com"
        elif provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = "https://api.bianxie.ai/v1"
        elif provider == "qwen":
            api_key = os.getenv("DASHSCOPE_API_KEY")
            base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        else:
            api_key = self.api_key or os.getenv("LLM_API_KEY")
            base_url = self.base_url or os.getenv("LLM_BASE_URL")
        return api_key, base_url
    
    def _create_client(self) -> OpenAI:
        return OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout,
        )

    def query(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        try:
            if system_prompt is None:
                system_prompt = "You are an expert in AI planning"

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"LLM query failed: {e}")
