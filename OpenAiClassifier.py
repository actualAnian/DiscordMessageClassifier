from ClassifierInterface import ClassifierInterface
import json
from openai import OpenAI
from typing import Dict

class OpenAIClassifier(ClassifierInterface):
    def __init__(self, model: str):
        self.client = OpenAI()  # Assumes OPENAI_API_KEY is set
        self.model = model

    def classify(self, message: str) -> Dict:
        response = self.client.responses.create(
            model=self.model,
            input=message,
            temperature=1
        )

        try:
            return json.loads(response.output_text)
        except json.JSONDecodeError:
            return {"category": None, "label": response.output_text}

    def get_text_from_image_url(self, image_url: str) -> str:
        prompt = "Please read all the text in this image and return it as plain text."
        response = self.client.responses.create(
            model="gpt-5-nano",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_image", "image_url": image_url}
                    ]
                }
            ]
        )
        return response.output_text
    def prepare_prompt(self, message: str, categories, examples, image_text: str = "") -> list:
        categories_text = "\n".join([f'{c["id"]} – {c["label"]}: {c["description"]}' for c in categories])

        system_prompt = f"""
    You are a classifier. Classify the message using the text in the message, and choose the most appropriate category.
    Here are the available categories:

    {categories_text}

    Respond in valid JSON with two keys: "category" (number) and "label" (text).
    Below are some examples of messages and their correct classification.
    """

        messages = [{ "role": "developer", "content": [{"type": "input_text", "text": system_prompt,}]}]

        # --- ADD FEW-SHOT TEXT EXAMPLES ---
        for ex in examples:
            messages.append({ "role": "user", "content": [{"type": "input_text", "text": "Example: " + ex["text"]}], })
            messages.append({"role": "assistant", "content": [{"type": "output_text", "text": json.dumps(ex["output"])}]})

        messages.append({"role": "developer", "content": [{"type": "input_text", "text": "--- End of examples ---"}]})

        # --- THE REAL MESSAGE TO CLASSIFY ---
        messages.append({ "role": "user", "content": [{"type": "input_text", "text": f"Message: {message + ' ' + image_text}"}],})
        return messages

    def get_handled_image_extensions(self) -> list:
        return ["png", "jpeg", "webp"]