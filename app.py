from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=os.environ["API_KEY"])
model1 = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(image_data, input_prompt):
    response = model.generate_content([image_data[0], input_prompt])
    return response.text

def generate_recipes(input_text):
    prompt = f"""Generate a detailed recipe and 3 popular YouTube cooking video links for: {input_text}

    Follow this exact structure:
    1. RECIPE SECTION:
    - Provide complete ingredients list
    - Step by step cooking instructions
    - Tips and tricks
    - Serving suggestions
    
    2. VIDEOS SECTION:
    Find 3 most popular YouTube cooking videos from verified cooking channels (like Food Network, Ranveer Brar, Sanjeev Kapoor, etc.) with minimum 100K views.
    For each video provide:
    VIDEO_ID: [extract only the ID from YouTube URL]
    TITLE: [exact video title]

    Important: Only include currently working videos from major cooking channels.
    Maximum response length: 4096 tokens
    """
    
    response = model1.generate_content(prompt, generation_config={
        'temperature': 0.7,
        'top_p': 1,
        'top_k': 40,
        'max_output_tokens': 4096,
    })
    return response.text

def create_download_button(recipe_text, dish_name):
    clean_name = "".join(x for x in dish_name if x.isalnum() or x.isspace())
    filename = f"{clean_name}_recipe.txt"
    
    st.download_button(
        label="📥 Download Recipe",
        data=recipe_text,
        file_name=filename,
        mime="text/plain",
        key=f"download_recipe_{dish_name}",  # Unique key for each button
        help="Click to download the recipe as a text file"
    )

def display_recipe_section(recipe_text):
    st.markdown("""
        <style>
        .recipe-container {
            background: rgba(0, 0, 0, 0.8);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .recipe-title {
            color: #00ff9d;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
        }
        .recipe-section {
            margin: 15px 0;
            padding: 15px;
            border-left: 3px solid #00ff9d;
        }
        .recipe-text {
            font-size: 16px;
            line-height: 1.6;
            white-space: pre-line;
        }
        .highlight {
            color: #00ff9d;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    formatted_recipe = f"""
    <div class="recipe-container">
        <div class="recipe-title">🍳 Generated Recipe</div>
        <div class="recipe-section">
            <div class="recipe-text">{recipe_text}</div>
        </div>
    </div>
    """
    st.markdown(formatted_recipe, unsafe_allow_html=True)

def display_video_section(videos_data):
    st.markdown("""
        <style>
        .video-section {
            padding: 20px;
            background: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    st.subheader("📺 Cooking Videos")
    
    for video in videos_data:
        with st.container():
            st.markdown(f"#### {video['title']}")
            try:
                video_url = f"https://www.youtube.com/watch?v={video['id']}"
                st.video(video_url)
                st.markdown("---")
            except Exception as e:
                st.error(f"Unable to load video: {video['title']}")

def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening... Click the button again to stop.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        st.write("Recognizing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand your speech.")
        return ""
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No image uploaded")

st.set_page_config(page_title="IndiChef - Automated Recipe Generator")

st.markdown("""
    <style>
    .stApp {
        background-image: url('https://as2.ftcdn.net/v2/jpg/05/02/08/49/1000_F_502084966_llTHsfsFBt6tZCXbm0WM4LPpPDJflxcc.jpg');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: Arial, sans-serif;
    }
    
    .main {
        width: 84%;
        margin-left: auto;
        margin-right: auto;
        padding: 6rem 1rem 10rem;
        max-width: 46rem;
    }
    
    h1 {
        color: white;
        text-align: center;
        font-size: 36px;
        margin-bottom: 20px;
    }
    
    h2 {
        color: #696969;
        text-align: center;
        font-size: 24px;
        margin-bottom: 10px;
    }
    
    .stButton>button {
        background-color: #008080;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 18px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    .stAlert {
        color: red;
        text-align: center;
        font-size: 18px;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>IndiChef - Automated Recipe Generator</h1>", unsafe_allow_html=True)

if st.button("Start Recording"):
    input_text = get_voice_input()
    st.write("You said:", input_text)
    if input_text:
        response = generate_recipes(input_text)
        sections = response.split("VIDEOS SECTION")
        display_recipe_section(sections[0])
        create_download_button(sections[0], input_text)
        
        if len(sections) > 1:
            video_data = []
            video_lines = sections[1].strip().split("\n")
            
            for line in video_lines:
                if "VIDEO_ID:" in line:
                    id_part = line.split("VIDEO_ID:")[1].strip()
                    title_part = next((l for l in video_lines if "TITLE:" in l and video_lines.index(l) > video_lines.index(line)), None)
                    if title_part:
                        video_data.append({
                            'id': id_part,
                            'title': title_part.split("TITLE:")[1].strip()
                        })
            
            display_video_section(video_data)

dish_name = st.text_input("Name of the Dish:", key="dish_name")
input_text = st.text_input("Input Prompt:", key="input")
submit1 = st.button("Generate Recipe")

if submit1:
    if input_text:
        response = generate_recipes(input_text)
        sections = response.split("VIDEOS SECTION")
        
        display_recipe_section(sections[0])
        create_download_button(sections[0], dish_name or input_text)
        
        if len(sections) > 1:
            video_data = []
            video_lines = sections[1].strip().split("\n")
            
            for line in video_lines:
                if "VIDEO_ID:" in line:
                    id_part = line.split("VIDEO_ID:")[1].strip()
                    title_part = next((l for l in video_lines if "TITLE:" in l and video_lines.index(l) > video_lines.index(line)), None)
                    if title_part:
                        video_data.append({
                            'id': id_part,
                            'title': title_part.split("TITLE:")[1].strip()
                        })
            
            display_video_section(video_data)
    else:
        st.error("Please enter the input prompt.")

if not input_text:
    st.warning("Please provide an input prompt.")
