# Greeting Generator API

This Flask-based API generates creative greetings using OpenAI's GPT model. It's designed to create personalized messages for various occasions, handling both human and animal names.

## Features

- Generate personalized greetings based on user input
- Handle both human and animal names
- Retrieve the last generated greeting
- Logging for easy debugging and monitoring

## Requirements

- Python 3.7+
- Flask
- python-dotenv
- langchain
- langchain_openai

## Installation

1. Clone this repository:
 

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. The API will be available at `http://127.0.0.1:8000`.

### Endpoints

#### Generate Greeting

- **URL**: `/generate-greeting`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "input": "Birthday for John"
  }
  ```
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "message": "Greeting generated successfully",
      "greeting": "<b>Happy Birthday, John!</b><br><br>May your day be filled with joy, laughter, and wonderful surprises! 🎉🎂"
    }
    ```

#### Retrieve Last Greeting

- **URL**: `/retrieve-greeting`
- **Method**: `GET`
- **Success Response**:
  - **Code**: 200
  - **Content**: 
    ```json
    {
      "message": "Greeting retrieved successfully",
      "greeting": "<b>Happy Birthday, John!</b><br><br>May your day be filled with joy, laughter, and wonderful surprises! 🎉🎂"
    }
    ```
- **Error Response**:
  - **Code**: 404
  - **Content**: 
    ```json
    {
      "error": "No greeting available. Generate a greeting first."
    }
    ```

## Error Handling

The API includes error handling for various scenarios, such as invalid input or issues with the OpenAI API. Appropriate error messages and status codes are returned in these cases.

## Logging

The application uses Python's `logging` module to log information, warnings, and errors. This helps with debugging and monitoring the application's behavior.

## Configuration

The application uses environment variables for configuration. Make sure to set the `OPENAI_API_KEY` in your `.env` file or environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
