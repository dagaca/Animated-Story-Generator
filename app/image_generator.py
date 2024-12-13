from time import sleep
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
client = InferenceClient(model="black-forest-labs/FLUX.1-dev", token=HF_TOKEN)

def generate_image(prompt, output_path, retries=5, initial_delay=10):
    """
    Generates an image using the Hugging Face FLUX.1 model with retry logic and backoff.

    Args:
        prompt (str): Text prompt for image generation.
        output_path (str): Path to save the generated image.
        retries (int): Maximum number of retries for busy model errors.
        initial_delay (int): Initial delay in seconds between retries.

    Raises:
        RuntimeError: If the image generation fails after all retries.
    """
    delay = initial_delay
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1}: Generating image for prompt: {prompt}")
            image = client.text_to_image(prompt)
            image.save(output_path)
            return
        except Exception as e:
            if "Model too busy" in str(e) and attempt < retries - 1:
                print(f"Model too busy. Retrying in {delay} seconds...")
                sleep(delay)
                delay *= 2  # Exponential backoff
                continue
            raise RuntimeError(f"Failed to generate image: {e}")
