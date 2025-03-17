from flask import Flask, request, jsonify
import os
from flask_cors import CORS
from langchain.prompts import PromptTemplate
from deep_translator import GoogleTranslator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi


app = Flask(__name__)
CORS(app, origins="chrome-extension://*")

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

def transcribe_audio(video_id):
    """Transcribes the audio using youtube API and videoID"""
    try:
        text = ""
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        for i in transcript:
            text += i["text"] + " "
        return text
    except Exception as e:
        return None

def summarize_text(text):
    """Generates a summary of the given text in the specified language."""
    if not text:
        return None

    try:
        # Define the prompt template correctly
        chunks_prompt = """Summarize the following text.
                        Keep the summary under 500 words while maintaining clarity and coherence.
                        Ensure the summary captures key points, main arguments, and essential details 
                        while preserving the original intent and tone.
                        Format the response naturally and fluently while avoiding unnecessary details 
                        or repetition.

                        Input Text:
                        {text}
                        """
        map_prompt_template = PromptTemplate(
            input_variables=["text"],
            template = chunks_prompt
        )

        prompt_template = PromptTemplate(
            input_variables=["text"],
            template='''Provide a final summary of the entire text.
                        Keep the final summary under 1000 words while maintaining clarity and coherence.
                        Ensure the summary captures key points, main arguments, and essential details 
                        while preserving the original intent and tone.
                        Format the response naturally and fluently while avoiding unnecessary details 
                        or repetition.

                        Input Text:
                        {text}'''
        )

        # Load the LLM model (Ensure API access is set up correctly)
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.create_documents([text])

        # Load the summarization chain
        chain = load_summarize_chain(
            llm,
            chain_type="map_reduce",
            map_prompt=map_prompt_template,  # Ensure the prompt is passed correctly
            combine_prompt=prompt_template,  # Needed for map_reduce method
            verbose=False
        )

        # Run the chain on the text chunks
        output_summary = chain.run(chunks)

        return output_summary
    except Exception as e:
        print(f"Summarization error: {e}")
        return None




def translate_text(text, target_lang="en"):
    """Translates text using GoogleTranslator."""
    if not text:
        return None

    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        print(f"Translation error: {e}")
        return None

@app.route("/translate", methods=["GET"])
def translate():
    """API Endpoint: Extracts, Transcribes, Summarizes & Translates Video"""
    video_id = request.args.get("videoID")
    target_lang = request.args.get("lang", "en")  # Default to English if not provided

    if not video_id:
        return jsonify({"error": "Missing videoID parameter"}), 400

    print(f"Processing Video ID: {video_id} | Target Language: {target_lang}")
    
    # Transcribe audio
    transcript = transcribe_audio(video_id)
    if not transcript:
        return jsonify({"error": "Failed to transcribe audio"}), 500

    # Summarize Transcript
    summary = summarize_text(transcript)
    if not summary:
        return jsonify({"error": "Failed to summarize text"}), 500

    # Translate Summary
    translated = translate_text(summary, target_lang)
    if not translated:
        return jsonify({"error": "Failed to translate text"}), 500

    return jsonify({"translated": translated})

if __name__ == "__main__":
    app.run(debug=True)