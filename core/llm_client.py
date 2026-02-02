import requests
import json
import time
from core.logger import setup_logger

logger = setup_logger("LLMClient")


class LLMClient:
    def __init__(
        self,
        model="llama3.1:8b",
        base_url="http://127.0.0.1:11434"
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()
        self.session.trust_env = False

        logger.info(f"LLM initialized | model={self.model} | url={self.base_url}")

    def chat(self, messages):
        logger.info("Preparing prompt for LLM")

        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user").upper()
            content = msg.get("content", "")
            prompt_parts.append(f"{role}:\n{content}")

        prompt = "\n\n".join(prompt_parts) + "\n\nASSISTANT:\n"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True
        }

        logger.info("Calling Ollama API (streaming enabled)")
        start_time = time.time()

        response = self.session.post(
            f"{self.base_url}/api/generate",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            stream=True,
            timeout=600
        )

        if response.status_code != 200:
            logger.error(f"Ollama error {response.status_code}: {response.text}")
            raise RuntimeError(
                f"Ollama error {response.status_code}: {response.text}"
            )

        output = []

        for line in response.iter_lines():
            if not line:
                continue

            chunk = json.loads(line.decode("utf-8"))

            if "response" in chunk:
                output.append(chunk["response"])

            if chunk.get("done"):
                break

        duration = round(time.time() - start_time, 2)
        logger.info(f"Ollama completed in {duration}s")

        return "".join(output)
