# Animated-Story-Generator

## Overview
The **Animated Story Generator** is a Flask-based API application that creates engaging animated videos from user-provided story prompts. Each story is split into sentences, visualized using AI-generated images, and narrated with synthesized speech.

---

## Features
- **AI Story Generation**: Creates stories based on prompts using OpenAI GPT-4.
- **Custom Sentence Count**: Users can specify the desired number of sentences in the story.
- **Narration Speed**: Choose between `slow`, `normal`, and `fast` narration rates.
- **Video Creation**: Generates videos with synchronized images and audio for each sentence.
- **Temporary File Management**: Uses temporary directories to manage intermediate files, ensuring cleanup after processing.

---

## API Endpoint
### `POST /generate_story`
Generates an animated story video based on the provided prompt.

#### Request Body
```json
{
    "prompt": "Once upon a time, a brave knight went on an adventure.",
    "rate": "normal",
    "sentence_count": 5
}
```
- **prompt** *(string, required)*: The input text to generate the story.
- **rate** *(string, optional)*: Narration speed. Options are `slow`, `normal`, and `fast` (default: `normal`).
- **sentence_count** *(integer, optional)*: Number of sentences in the story (default: 5).

#### Response Body
```json
{
    "prompt": "Once upon a time, a brave knight went on an adventure.",
    "story": "Once upon a time...",
    "sentences": ["Once upon a time...", "He went on an adventure..."],
    "video_url": "output\\abc12345-6789-1011-1213-abcdef123456.mp4"
}
```
- **prompt**: The original user-provided prompt.
- **story**: The generated story text.
- **sentences**: An array of individual sentences from the story.
- **video_url**: Path to the generated video file.

---

## Setup
### Prerequisites
- Python 3.8+

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/animated-story-generator.git
   cd animated-story-generator
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - Create a `.env` file in the root directory:
     ```env
      OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
      HF_TOKEN="YOUR_HF_TOKEN"
      LOG_DIR=logs
      LOG_FILE=app.log
      OUTPUT_DIR=output
      TEMP_DIR=temp
     ```

### Run the Application
Start the Flask server:
```bash
python run.py
```
By default, the server runs on `http://127.0.0.1:5000`.

---

## Project Structure
```
animated-story-generator/
├── app/
│   ├── __init__.py         # Flask app initialization
│   ├── routes.py           # API routes
│   ├── story_generator.py  # Story generation logic
│   ├── video_generator.py  # Video creation logic
│   ├── image_generator.py  # Image generation logic
│   ├── rate_mapper.py      # Narration rate mapping
├── config/
│   ├── log_config.py       # Logging configuration
├── output/
│   ├── uuid.mp4            # Generated video files
├── temp/                   # Temporary directory for intermediate files
├── logs/                   # Log files directory
├── .env                    # Environment variables
├── requirements.txt        # Python dependencies
├── run.py                  # Entry point for the application
└── README.md               # Documentation
```

---

## Swagger UI

Add a screenshot of the Swagger UI showing the '/generate_story' endpoint.

![image](https://github.com/user-attachments/assets/4d7e4cfe-15c5-4bb1-abbc-ddbcfdb28cac)

## Example Request

### Request Example 1: Slow Speed, 2 Sentences

![1](https://github.com/user-attachments/assets/1616c917-c5ae-48cf-9032-387d68fdd550)

### Request Example 2: Normal Speed, 3 Sentences

![2](https://github.com/user-attachments/assets/7f2a2212-9a56-4083-9998-460e8c3c104b)

### Request Example 3: Fast Speed, 4 Sentences

![3](https://github.com/user-attachments/assets/47781276-895a-45f4-bc1e-892720674eea)

---

## Logging
Logs are stored in the `logs` directory with details about:
- Requests received
- Processing status
- Errors encountered

---

## Error Handling
- **400 Bad Request**: Bad request due to missing or invalid input data.

- **500 Internal Server Error**: 	Internal server error due to an unexpected issue during processing.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
