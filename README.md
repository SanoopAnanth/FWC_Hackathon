**👩‍🍳🍴IndiChef - Automated Recipe Generator👩‍🍳🍴**
IndiChef is a web application designed to assist users in generating Indian cuisine recipes automatically. This tool leverages the power of AI, specifically Google's generative AI models, to provide users with recipe suggestions based on their input prompts.

### Get your API key or gemini from [Gemini AI Studio](https://ai.google.dev/gemini-api/docs/api-key), and paste your key in [Environmet file](.env)

## How to run ##
Step 1: Clone the repo.
```
git clone https://github.com/SanoopAnanth/FWC_Hackathon.git
```

Step 2: Create virtual environment using conda. And don't forget to activate the environment.
```
conda create -p venv python==3.10 -y

conda activate <path_where_venv>
```
Step 3: Install all the requirements files.
```
pip install -r requirements.txt
```
Step 4: Run the application.
```
streamlit run app.py
```
### After the above 4 steps, the streamlit application will be opened locally in a browser. ###



**Key Features**
***📝Recipe Generation:***
Input details such as dish name, ingredients, and instructions in a structured format.
Utilize Google's generative AI models to generate detailed recipes based on the provided input.

***🔄Flexible Input:***
Input various details about the dish, including ingredients and instructions, in a user-friendly interface.
Simply fill out text input fields with the relevant information. 

***🛠️Customization:***
Customize the recipe generation process by providing specific details about the dish.
Tailor recipe suggestions based on individual preferences and requirements.

***🖼️ Visual Feedback***
Upload an image of the dish to provide additional context and inspiration for recipe generation.

***🔗Streamlit Integration***
Built using Streamlit, a popular Python library for building interactive web applications.
Provides an intuitive and easy-to-use interface for users to interact with the recipe generator.

**About**
IndiChef - Automated Recipe Generator simplifies the process of generating Indian cuisine recipes by leveraging AI technology. It provides quick and convenient access to a wide range of recipe suggestions tailored to users' preferences. Whether you're looking for traditional favorites or innovative new dishes, IndiChef is designed to cater to your culinary needs.

**Output**
***Voice Translator 🎤***
IndiChef also includes a voice input feature powered by Google Speech Recognition. Simply click the "Start Recording" button and speak your input prompt. The application will transcribe your speech into text, allowing you to generate recipes with ease.
***Input Details:***
Enter the dish name, ingredients, and instructions in the provided text input fields.
***Generate Recipe 📜***
Click the "Generate Recipe" button to receive personalized recipe suggestions instantly.


Thank you