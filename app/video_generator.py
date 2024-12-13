"""
This module handles video creation by generating images for each sentence,
synthesizing audio for each sentence, and synchronizing them into a video.
"""
import os
import tempfile
import pyttsx3
import comtypes.client
import uuid
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from dotenv import load_dotenv
from .image_generator import generate_image

# Load environment variables
load_dotenv()

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")  # Default to "output" if not set
TEMP_DIR = os.getenv("TEMP_DIR", "temp")  # Default to "temp" if not set

def synthesize_audio(text, output_path, rate=100):
    """
    Synthesizes audio from text and saves it as a WAV file.

    Args:
        text (str): The text to synthesize into speech.
        output_path (str): Path to save the synthesized audio file.
        rate (int): Speaking rate (words per minute). Defaults to 100.

    Raises:
        RuntimeError: If audio synthesis fails due to an unexpected error.
    """
    try:
        # Initialize COM library
        comtypes.CoInitialize()

        # Initialize the text-to-speech engine
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)  # Adjust speaking rate

        # Save the synthesized speech to a file
        engine.save_to_file(text, output_path)
        engine.runAndWait()

    except Exception as e:
        # Raise a runtime error with the cause of the failure
        raise RuntimeError(f"Audio synthesis failed for text: {text}. Error: {e}")

    finally:
        # Ensure COM library is uninitialized
        comtypes.CoUninitialize()


def create_story_video(sentences, rate, fps=24):
    """
    Creates a synchronized video with visuals and audio for each sentence.

    Args:
        sentences (list): Sentences for which images and audio are generated.
        rate (int): Speaking rate for the audio.
        fps (int): Frames per second for the video.

    Returns:
        str: Path to the generated video.

    Raises:
        RuntimeError: If any error occurs during video creation.
    """
    video_id = str(uuid.uuid4())
    output_path = os.path.join(OUTPUT_DIR, f"{video_id}.mp4")

    try:
        # Create temporary directory
        with tempfile.TemporaryDirectory(dir=TEMP_DIR) as temp_subdir:
            clips = []

            for i, sentence in enumerate(sentences):
                try:
                    # Paths for intermediate files
                    image_path = os.path.join(temp_subdir, f"frame_{i}.png")
                    audio_path = os.path.join(temp_subdir, f"audio_{i}.wav")

                    # Generate image and audio for the sentence
                    generate_image(sentence, image_path)
                    synthesize_audio(sentence, audio_path, rate)

                    # Create a video clip for the sentence
                    audio_clip = AudioFileClip(audio_path)
                    duration = audio_clip.duration

                    image_clip = (
                        ImageClip(image_path)
                        .set_duration(duration)
                        .set_audio(audio_clip)
                        .resize(height=720)
                        .set_fps(fps)
                    )
                    clips.append(image_clip)

                except Exception as e:
                    raise RuntimeError(f"Error processing sentence '{sentence}': {e}")

            # Concatenate all clips into a single video
            final_video = concatenate_videoclips(clips, method="compose")
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=fps)

    except Exception as e:
        raise RuntimeError(f"Failed to create story video. Error: {e}")

    return output_path
