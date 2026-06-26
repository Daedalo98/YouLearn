# ai_manager.py
from google import genai
from google.genai import types
from openai import OpenAI # Ensure you have openai installed: pip install openai
import requests
import json

class Manager:
    # 🚨 Removed the Singleton (__new__) pattern to ensure user isolation

    def __init__(self, gemini_api_key="", openai_api_key=""):
        """Initialize clients only if the user provided the respective keys."""
        self.gemini_client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None
        self.openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None

    def get_models(self):
        """Returns recommended Gemini, OpenAI, and local Ollama models."""
        models = []
        
        # Add Gemini Models if client exists
        if self.gemini_client:
            models.extend(["gemini-2.5-flash", "gemini-2.5-pro", "gemini-embedding-001"])
            
        # Add OpenAI Models if client exists
        if self.openai_client:
            models.extend(["gpt-4o-mini", "gpt-4o", "text-embedding-3-small", "text-embedding-3-large"])

        # Add Ollama Models
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                for m in data.get("models", []):
                    models.append(m["name"])
        except Exception as e:
            pass # Silently fail if Ollama is not running
            
        return models

    # Helper routing functions
    def is_gemini_model(self, model_name):
        return model_name.startswith("gemini")
        
    def is_openai_model(self, model_name):
        return model_name.startswith("gpt") or model_name.startswith("text-embedding") or model_name.startswith("o1")

    def generate_stream(self, prompt, system_prompt, model_name="gemini-2.5-flash", temperature=1.0, max_tokens=None):
        """Routes the streaming request based on the model name prefix."""
        
        # --- OPENAI ROUTE ---
        if self.is_openai_model(model_name):
            if not self.openai_client:
                yield "Error: OpenAI client not initialized. Check your API key."
                return
            try:
                response = self.openai_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        yield chunk.choices[0].delta.content
                return
            except Exception as e:
                yield f"\n\nError generating response from OpenAI: {e}"
                return

        # --- GEMINI ROUTE ---
        elif self.is_gemini_model(model_name):
            if not self.gemini_client:
                yield "Error: Gemini client not initialized. Check your API key."
                return
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    max_output_tokens=max_tokens if max_tokens else None
                )
                response = self.gemini_client.models.generate_content_stream(
                    model=model_name,
                    contents=prompt,
                    config=config
                )
                for chunk in response:
                    if chunk.text:
                        yield chunk.text
                return
            except Exception as e:
                yield f"\n\nError generating response from Gemini: {e}"
                return

        # --- OLLAMA ROUTE (Fallback) ---
        else:
            try:
                options = {"temperature": temperature}
                if max_tokens: options["num_predict"] = max_tokens
                
                response = requests.post("http://localhost:11434/api/generate", json={
                    "model": model_name,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": True,
                    "options": options
                }, stream=True)
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            yield chunk["response"]
                return
            except Exception as e:
                yield f"\n\nError generating response from Ollama: {e}"
                return

    # NOTE: You will apply this exact same `if/elif/else` routing pattern 
    # to your `generate_sync`, `get_embedding`, and `get_embeddings_batch` functions. 
    # For OpenAI embeddings, the call is `self.openai_client.embeddings.create(input=text, model=model_name).data[0].embedding`