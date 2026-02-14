<<<<<<< HEAD
import os
import random
from dotenv import load_dotenv
import gradio as gr

# Load environment variables
load_dotenv()

# Import your custom modules
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# --- Energy Detection Logic ---
def get_energy_context(user_text):
    low_energy_cues = ["tired", "exhausted", "burnout", "overwhelmed", "stressed", "too much", "can't focus", "heavy"]
    high_energy_cues = ["ready", "motivated", "let's go", "energy", "excited", "focus", "sharp"]

    text = user_text.lower()
    if any(cue in text for cue in low_energy_cues):
        return "\n\nCRITICAL CONTEXT: The user is feeling LOW ENERGY/OVERWHELMED. Give only ONE very small task and suggest a 5-minute break."
    elif any(cue in text for cue in high_energy_cues):
        return "\n\nCRITICAL CONTEXT: The user has HIGH ENERGY. You can suggest a focused 25-minute sprint."
    return "\n\nCRITICAL CONTEXT: The user has balanced energy. Provide 3 micro-steps."

# --- Updated System Prompt ---
SYSTEM_PROMPT = """You are the 'Neuro-Navigator,' a supportive and low-arousal AI coach for neurodiverse individuals (ADHD/Dyslexia). 
Your goal is to reduce executive dysfunction and cognitive load.

Guidelines:
1. GREETING: Start with a calm, validating opening.
2. ANALYSIS: If an image is provided, break it down into 3 simple anchors.
3. THE SALAMI SLICER: Break tasks into 'micro-steps' (<10 mins).
4. DYSLEXIA FRIENDLY: Use short sentences and bullet points.
5. RSD AWARE: Use supportive, non-critical language."""

def process_inputs(audio_filepath, image_filepath):
    if audio_filepath is None:
        return "Waiting for your voice...", "Please tap the mic to share what's on your mind.", None, "0 XP"

    # 1. Speech-to-Text
    try:
        user_speech_text = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    except Exception as e:
        return f"Audio Error: {str(e)}", "I couldn't quite hear that.", None, "0 XP"

    # 2. Energy Analysis & Prompt Construction
    energy_context = get_energy_context(user_speech_text)
    full_query = f"{SYSTEM_PROMPT}{energy_context}\nUser Input: {user_speech_text}"

    # 3. Vision & Task Analysis
    try:
        coach_response = analyze_image_with_query(
            query=full_query,
            encoded_image=encode_image(image_filepath) if image_filepath else None,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    except Exception:
        coach_response = "I'm here to listen. Let's focus on what you told me."

    # 4. Text-to-Speech
    try:
        coach_voice_path = text_to_speech_with_elevenlabs(
            input_text=coach_response, 
            output_filepath="navigator_voice.mp3"
        ) 
    except Exception:
        coach_voice_path = None

    # 5. Gamification: Calculate "XP" earned for the session
    xp_earned = random.randint(15, 50)
    xp_display = f"✨ +{xp_earned} Focus XP Gained!"

    return user_speech_text, coach_response, coach_voice_path, xp_display

# --- UI Layout ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neuro-Navigator 1.0") as demo:
    gr.Markdown("# 🧩 Neuro-Navigator: Your Daily Focus Ally")
    
    with gr.Row():
        # Input Section
        with gr.Column(scale=1):
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Voice Mind-Dump")
            image_input = gr.Image(type="filepath", label="Task Vision")
            submit_btn = gr.Button("Help me focus ✨", variant="primary")
            
        # Output Section
        with gr.Column(scale=1):
            with gr.Row():
                xp_counter = gr.Label(value="0 Focus XP", label="Session Rewards")
            stt_output = gr.Textbox(label="What I heard you say:", interactive=False)
            response_output = gr.Markdown() 
            voice_output = gr.Audio(label="Listen to your Coach", autoplay=True)

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[stt_output, response_output, voice_output, xp_counter]
    )

if __name__ == "__main__":
=======
import os
import random
from dotenv import load_dotenv
import gradio as gr

# Load environment variables
load_dotenv()

# Import your custom modules
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# --- Energy Detection Logic ---
def get_energy_context(user_text):
    low_energy_cues = ["tired", "exhausted", "burnout", "overwhelmed", "stressed", "too much", "can't focus", "heavy"]
    high_energy_cues = ["ready", "motivated", "let's go", "energy", "excited", "focus", "sharp"]

    text = user_text.lower()
    if any(cue in text for cue in low_energy_cues):
        return "\n\nCRITICAL CONTEXT: The user is feeling LOW ENERGY/OVERWHELMED. Give only ONE very small task and suggest a 5-minute break."
    elif any(cue in text for cue in high_energy_cues):
        return "\n\nCRITICAL CONTEXT: The user has HIGH ENERGY. You can suggest a focused 25-minute sprint."
    return "\n\nCRITICAL CONTEXT: The user has balanced energy. Provide 3 micro-steps."

# --- Updated System Prompt ---
SYSTEM_PROMPT = """You are the 'Neuro-Navigator,' a supportive and low-arousal AI coach for neurodiverse individuals (ADHD/Dyslexia). 
Your goal is to reduce executive dysfunction and cognitive load.

Guidelines:
1. GREETING: Start with a calm, validating opening.
2. ANALYSIS: If an image is provided, break it down into 3 simple anchors.
3. THE SALAMI SLICER: Break tasks into 'micro-steps' (<10 mins).
4. DYSLEXIA FRIENDLY: Use short sentences and bullet points.
5. RSD AWARE: Use supportive, non-critical language."""

def process_inputs(audio_filepath, image_filepath):
    if audio_filepath is None:
        return "Waiting for your voice...", "Please tap the mic to share what's on your mind.", None, "0 XP"

    # 1. Speech-to-Text
    try:
        user_speech_text = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    except Exception as e:
        return f"Audio Error: {str(e)}", "I couldn't quite hear that.", None, "0 XP"

    # 2. Energy Analysis & Prompt Construction
    energy_context = get_energy_context(user_speech_text)
    full_query = f"{SYSTEM_PROMPT}{energy_context}\nUser Input: {user_speech_text}"

    # 3. Vision & Task Analysis
    try:
        coach_response = analyze_image_with_query(
            query=full_query,
            encoded_image=encode_image(image_filepath) if image_filepath else None,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    except Exception:
        coach_response = "I'm here to listen. Let's focus on what you told me."

    # 4. Text-to-Speech
    try:
        coach_voice_path = text_to_speech_with_elevenlabs(
            input_text=coach_response, 
            output_filepath="navigator_voice.mp3"
        ) 
    except Exception:
        coach_voice_path = None

    # 5. Gamification: Calculate "XP" earned for the session
    xp_earned = random.randint(15, 50)
    xp_display = f"✨ +{xp_earned} Focus XP Gained!"

    return user_speech_text, coach_response, coach_voice_path, xp_display

# --- UI Layout ---
with gr.Blocks(theme=gr.themes.Soft(), title="Neuro-Navigator 1.0") as demo:
    gr.Markdown("# 🧩 Neuro-Navigator: Your Daily Focus Ally")
    
    with gr.Row():
        # Input Section
        with gr.Column(scale=1):
            audio_input = gr.Audio(sources=["microphone"], type="filepath", label="Voice Mind-Dump")
            image_input = gr.Image(type="filepath", label="Task Vision")
            submit_btn = gr.Button("Help me focus ✨", variant="primary")
            
        # Output Section
        with gr.Column(scale=1):
            with gr.Row():
                xp_counter = gr.Label(value="0 Focus XP", label="Session Rewards")
            stt_output = gr.Textbox(label="What I heard you say:", interactive=False)
            response_output = gr.Markdown() 
            voice_output = gr.Audio(label="Listen to your Coach", autoplay=True)

    submit_btn.click(
        fn=process_inputs,
        inputs=[audio_input, image_input],
        outputs=[stt_output, response_output, voice_output, xp_counter]
    )

if __name__ == "__main__":
>>>>>>> 08ac7bb00b13deb61511ba05c01c9f3aa34280bf
    demo.launch(debug=True)