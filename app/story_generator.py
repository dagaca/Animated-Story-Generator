"""
This module handles story generation and sentence splitting using OpenAI API.
"""
import openai
import re
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenAI API key setup
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_story(prompt, sentence_count):
    """
    Generates a story based on the provided prompt using GPT-4 and limits it to a specific number of sentences.

    Args:
        prompt (str): The input prompt for story generation.
        sentence_count (int): Desired number of sentences in the story.

    Returns:
        str: The generated story.

    Raises:
        ValueError: If the API response does not contain the expected content.
    """
    # Construct the detailed prompt with the sentence count instruction
    detailed_prompt = (
        f"{prompt} Please generate a story that is approximately {sentence_count} sentences long."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a creative storyteller for children."},
                {"role": "user", "content": detailed_prompt}
            ],
            max_tokens=500,
            temperature=0.7  # Adjust creativity level (0.7 is moderately creative)
        )

        # Extract and return the story content
        story = response.get('choices', [{}])[0].get('message', {}).get('content', '').strip()

        if not story:
            raise ValueError("The API response did not contain a valid story.")

        return story

    except Exception as e:
        raise RuntimeError(f"Failed to generate story: {e}")

def split_story_into_sentences(story, max_sentences):
    """
    Splits the story into individual sentences using regex and limits the number of sentences.

    Args:
        story (str): The story to split.
        max_sentences (int): Maximum number of sentences to return.

    Returns:
        list: A list of sentences.

    Raises:
        ValueError: If the input story is invalid or empty.
    """
    try:
        # Ensure the story is a valid non-empty string
        if not isinstance(story, str) or not story.strip():
            raise ValueError("Story must be a non-empty string.")

        # Split the story into sentences
        sentences = re.split(r'(?<=[.!?]) +', story.strip())

        # Limit the number of sentences to the specified max_sentences
        return sentences[:max_sentences]

    except Exception as e:
        raise RuntimeError(f"Failed to split story into sentences: {e}")
