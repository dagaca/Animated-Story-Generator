"""
This module provides the API endpoint to generate an animated story video
using the OpenAI API. The story includes AI-generated visuals and audio for
each sentence, creating a dynamic and engaging storytelling experience.
"""
from flask import request, jsonify
from app import app
from .story_generator import generate_story, split_story_into_sentences
from .video_generator import create_story_video
from .rate_mapper import get_speech_rate


@app.route('/generate_story', methods=['POST'])
def generate_story_video():
    """
    API endpoint that generates an animated story video based on a user-provided prompt.

    ---
    tags:
      - Story Generator
    summary: Generate an animated story video
    description: >
        This API endpoint generates an animated story video based on a user-provided prompt.
        The story is split into sentences, and for each sentence, visuals and audio are generated.
        The result is synchronized into a cohesive video.

    parameters:
      - name: body
        in: body
        required: true
        description: JSON object containing the user-provided input for the story generation.
        schema:
          type: object
          properties:
            prompt:
              type: string
              description: The text prompt to generate the story.
              example: "Once upon a time, a brave knight went on an adventure."
            rate:
              type: string
              description: >
                The speed of the narration. Options are:
                - "slow" for slower speech (50 WPM),
                - "normal" for standard speech (100 WPM),
                - "fast" for faster speech (150 WPM).
              example: "normal"
            sentence_count:
              type: integer
              description: The desired number of sentences in the story.
              example: 5

    responses:
      200:
        description: Successfully generated the animated story video.
        content:
          application/json:
            schema:
              type: object
              properties:
                prompt:
                  type: string
                  description: The original prompt provided by the user.
                  example: "Once upon a time, a brave knight went on an adventure."
                story:
                  type: string
                  description: The full story generated from the prompt.
                  example: "Once upon a time, a brave knight embarked on an exciting journey..."
                sentences:
                  type: array
                  items:
                    type: string
                  description: The story split into individual sentences.
                video_url:
                  type: string
                  description: The URL of the generated animated story video.
                  example: "output\\abc12345-6789-1011-1213-abcdef123456.mp4"
      400:
        description: Bad request due to missing or invalid input data.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: A message describing the invalid input.
                  example: "Prompt must be provided."
      500:
        description: Internal server error due to an unexpected issue during processing.
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: A message describing the internal server error.
                  example: "An unexpected error occurred."
    """
    try:
        app.logger.info("Received request to generate animated story video")
        data = request.json
        prompt = data.get("prompt")
        rate = data.get("rate", "normal").lower()  # Default to "normal"
        sentence_count = data.get("sentence_count", 5)  # Default to 5 sentences

        # Validate required fields
        if not prompt:
            app.logger.error("Prompt must be provided")
            return jsonify({"error": "Prompt must be provided"}), 400

        # Map rate to numeric value using utility function
        try:
            selected_rate = get_speech_rate(rate)
        except ValueError as ve:
            app.logger.error("Invalid rate provided")
            return jsonify({"error": str(ve)}), 400

        # Generate the story
        story = generate_story(prompt, sentence_count)

        # Split the story into sentences and limit by sentence_count
        sentences = split_story_into_sentences(story, sentence_count)

        # Create the animated story video
        video_path = create_story_video(sentences, rate=selected_rate)

        app.logger.info("Animated story video generated successfully")
        return jsonify({
            "prompt": prompt,
            "story": story,
            "sentences": sentences,
            "video_url": f"{video_path}"
        }), 200

    except ValueError as ve:
        app.logger.error('ValueError: %s', str(ve), exc_info=True)
        return jsonify({'error': 'Invalid input data format'}), 400
    except Exception as e:
        app.logger.error('An error occurred: %s', str(e), exc_info=True)
        return jsonify({'error': 'An unexpected error occurred'}), 500
