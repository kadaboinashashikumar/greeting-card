from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import asyncio
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    logger.error("OPENAI_API_KEY environment variable is not set")
    raise ValueError("OPENAI_API_KEY environment variable is not set")
else:
    logger.info("OpenAI API key loaded successfully")

llm = ChatOpenAI(model="gpt-4o", temperature=1)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a creative greeting card generator. If the input name is a real animal name (e.g., Dog, Lion, Cat), treat it as an animal and generate the greeting accordingly. Avoid implying human-to-human relationships or companionship, and focus on the animal's own experience (e.g., fun, joy, playfulness). For pet names or human-like nicknames (e.g., Bunny, Puppy), treat them as human names. The first sentence should be a wish based on the occasion (e.g., birthday, anniversary), and the message should be warm, friendly, and visually appealing with relevant emojis."),
    ("system", "If the input is a single word or lacks necessary details (such as the occasion or context), respond with: 'Could you please provide more information, such as the occasion or additional details, to create a personalized greeting?'"),
    ("system", "If the input is unclear, nonsensical, or consists of random characters (e.g., '--------------'), respond with: 'Sorry, the provided input is not clear. Please provide a valid and clear input for your personalized greeting.'"),
    ("system", "Always check if the input contains both a name and a greeting type. If it doesn't, prompt the user for missing information."),
    ("system", "If you encounter ambiguity about whether a name is a real animal or a human-like nickname, respond with: 'I'm not sure if this is a human name or an animal name. Could you please clarify or provide more details?'"),
    ("user", "{input}")
])

logger.info("OpenAI model and prompt template initialized")
last_generated_greeting = None

@app.route('/generate-greeting', methods=['POST'])
async def generate_greeting_post():
    global last_generated_greeting
    user_input = request.json.get('input')

    if not user_input or len(user_input.strip()) < 2:
        logger.warning("Invalid input provided in the POST request")
        return jsonify({"error": "Invalid input. Please enter a longer message."}), 400

    logger.info(f"Received valid input: {user_input}")

    m_input = f"{user_input}. Make the first greeting in bold and then continue the remaining text on the next line."
    chain = prompt | llm

    try:
        response = await asyncio.to_thread(chain.invoke, {"input": m_input})
        logger.info("Greeting generated by OpenAI model")

        response_text = response.content.replace('**', '')

        logger.debug(f"Raw response from OpenAI: {response_text}")

        if not response_text.strip():
            logger.error("Received empty response from OpenAI model")
            return jsonify({"error": "Failed to generate a greeting. Please try again with a clearer message."}), 500

        response_lines = response_text.split('!', 1)
        if len(response_lines) > 1:
            first_sentence = f"<b>{response_lines[0]}!</b>"
            remaining_message = response_lines[1].replace('. ', '<br><br>')
        else:
            first_sentence = f"<b>{response_text}</b>"
            remaining_message = ""

        if first_sentence.strip() and remaining_message.strip():
            generated_greeting = f"{first_sentence}<br><br>{remaining_message}<br><br><i>Best wishes from HR Dept. - T.A.C</i>"
        else:
            generated_greeting = f"{first_sentence}<br><br>{remaining_message}"

        last_generated_greeting = generated_greeting

        logger.info("Formatted greeting generated successfully")

        return jsonify({"message": "Greeting generated successfully", "greeting": generated_greeting})

    except Exception as e:
        logger.error(f"Error during greeting generation: {e}")
        return jsonify({"error": "An error occurred while generating the greeting."}), 500

@app.route('/retrieve-greeting', methods=['GET'])
def retrieve_greeting():
    if last_generated_greeting is None:
        logger.warning("No greeting available to retrieve")
        return jsonify({"error": "No greeting available. Generate a greeting first."}), 404

    logger.info("Returning last generated greeting")
    return jsonify({"message": "Greeting retrieved successfully", "greeting": last_generated_greeting})

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(host='127.0.0.1', port=8000)