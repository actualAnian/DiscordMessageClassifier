from abc import ABC, abstractmethod
from typing import Optional, Dict

class ClassifierInterface(ABC):
    @abstractmethod
    def classify(self, text: str, image_path: Optional[str] = None) -> Dict:
        """
        Classifies a message based on provided text (and optional image).

        Args:
            text (str): The message text to classify.

        Returns:
            Dict: The classification result (e.g., {"category": 1, "label": "Installation"}).
        """
        pass
    @abstractmethod
    def get_text_from_image_url(self, image_url: str) -> str:
        """
        Extracts text from an image URL using OCR.

        Args:
            image_url (str): The URL of the image to extract text from.
        Returns:
            str: The extracted text from the image.
        """
        pass
    @abstractmethod
    def prepare_prompt(self, message: str, categories, examples, image_text: str = None) -> list:
        """
        Prepares the prompt for classification.
        Args:
            message (str): The message to classify.
            categories (list): List of categories.
            examples (list): List of examples.
            image_text (str, optional): Text extracted from an image, if any.
            Returns:
            list: The prepared prompt as a list of messages.
            """
        pass
    @abstractmethod
    def get_handled_image_extensions(self) -> list:
        """
        Returns a list of handled image extensions.
        Returns:
            list: List of handled image extensions (e.g., ["png", "jpg", "jpeg", "webp"]).
        """
        pass


