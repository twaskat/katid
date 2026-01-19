import gradio as gr
import socket
import requests
import json
import base64

def find_available_port(start_port=7861, max_attempts=100):
    """Find an available port starting from the given port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None

def encode_image_to_base64(image_path):
    """Encode image to base64 bytes"""
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
            return base64.b64encode(image_bytes)
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

def analyze_image(api_key, model, image, analysis_type):
    """Analyze image using Fireworks vision API"""
    if not api_key:
        return "❌ Please enter your Fireworks API key first!"
    
    if image is None:
        return "❌ Please upload an image first!"
    
    try:
        # Convert image to base64
        # Gradio returns image as numpy array or file path
        import numpy as np
        
        if isinstance(image, str):
            # File path
            base64_image = encode_image_to_base64(image)
        elif isinstance(image, np.ndarray):
            # numpy array from Gradio
            from PIL import Image
            import io
            pil_image = Image.fromarray(image)
            buffered = io.BytesIO()
            pil_image.save(buffered, format="JPEG")
            base64_image = base64.b64encode(buffered.getvalue())
        else:
            # Try to handle as bytes or file-like object
            base64_image = base64.b64encode(image)
        
        if not base64_image:
            return "❌ Failed to process the image. Please try another image."
        
        url = "https://api.fireworks.ai/inference/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Create analysis type specific prompts
        analysis_prompts = {
            "General Description": "Provide a comprehensive description of this image. Describe the main subjects, setting, colors, mood, and any notable details. Be detailed and descriptive.",
            "Object Detection": "Identify and list all objects visible in this image. For each object, describe its position, appearance, and any relevant details.",
            "Scene Understanding": "Analyze the scene in this image. What type of environment is this? What is happening? Describe the context, setting, and overall composition.",
            "Text Recognition (OCR)": "Extract and transcribe any text visible in this image. Include the text content and note its location if relevant.",
            "Emotion & Mood": "Analyze the emotional content and mood of this image. Describe the feelings, atmosphere, and emotional impact conveyed.",
            "Detailed Analysis": "Provide an extremely detailed analysis of this image. Include all elements: objects, people, colors, lighting, composition, mood, context, and any other relevant details."
        }
        
        system_prompt = analysis_prompts.get(analysis_type, analysis_prompts["General Description"])
        
        user_prompt = "Please analyze this image according to the instructions above."
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{system_prompt}\n\n{user_prompt}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image.decode('utf-8') if isinstance(base64_image, bytes) else base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            analysis = result['choices'][0]['message']['content']
            return f"🔍 **{analysis_type} Analysis**\n\n{analysis}"
        else:
            error_msg = response.json().get('error', 'Unknown error')
            return f"❌ API Error: {error_msg}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Custom CSS for cute dark purple theme (same as Story Forge)
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #1a0a2e 0%, #2d1b4e 50%, #1a0a2e 100%) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
}

#header-title {
    text-align: center;
    color: #e0b0ff !important;
    font-size: 2.5em !important;
    font-weight: bold;
    text-shadow: 0 0 20px rgba(224, 176, 255, 0.5);
    margin: 20px 0 !important;
}

#header-subtitle {
    text-align: center;
    color: #c77dff !important;
    font-size: 1.1em !important;
    margin-bottom: 30px !important;
}

.emoji-icon {
    font-size: 1.5em;
}

#main-container {
    max-width: 900px;
    margin: 0 auto;
    background: rgba(45, 27, 78, 0.6) !important;
    border-radius: 20px !important;
    padding: 30px !important;
    border: 2px solid #9d4edd !important;
    box-shadow: 0 0 30px rgba(157, 78, 221, 0.3) !important;
}

.input-group {
    margin: 20px 0 !important;
}

.api-key-box textarea,
.api-key-box input,
.model-box textarea,
.model-box input,
.analysis-box select,
.image-upload {
    background: rgba(26, 10, 46, 0.8) !important;
    border: 2px solid #7b2cbf !important;
    border-radius: 12px !important;
    color: #e0b0ff !important;
    font-size: 1em !important;
    padding: 12px !important;
}

.api-key-box textarea:focus,
.api-key-box input:focus,
.model-box textarea:focus,
.model-box input:focus,
.analysis-box select:focus {
    border-color: #c77dff !important;
    box-shadow: 0 0 15px rgba(199, 125, 255, 0.4) !important;
    outline: none !important;
}

label {
    color: #e0b0ff !important;
    font-weight: 600 !important;
    font-size: 1em !important;
}

.analyze-btn {
    background: linear-gradient(135deg, #7b2cbf 0%, #9d4edd 50%, #c77dff 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 1.2em !important;
    font-weight: bold !important;
    padding: 15px 30px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 5px 20px rgba(157, 78, 221, 0.4) !important;
}

.analyze-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(199, 125, 255, 0.6) !important;
}

.output-box textarea {
    background: rgba(26, 10, 46, 0.9) !important;
    border: 2px solid #9d4edd !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 1em !important;
    line-height: 1.6 !important;
    padding: 20px !important;
    min-height: 300px !important;
}

.image-preview {
    max-width: 100%;
    border-radius: 12px;
    border: 2px solid #7b2cbf;
}

.footer-text {
    text-align: center;
    color: #c77dff !important;
    font-size: 0.9em !important;
    margin-top: 20px !important;
}

.image-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}
"""

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🔍 Vision Agent 🔍", elem_id="header-title")
    gr.Markdown("### 👁️ See what AI sees in your images 👁️", elem_id="header-subtitle")
    
    with gr.Group(elem_id="main-container"):
        with gr.Group(elem_classes="input-group api-key-box"):
            api_key_input = gr.Textbox(
                label="🔑 Fireworks API Key",
                placeholder="Enter your Fireworks API key...",
                type="password",
                show_label=True
            )
        
        with gr.Group(elem_classes="input-group model-box"):
            model_input = gr.Textbox(
                label="🤖 Vision Model",
                value="accounts/fireworks/models/llava-v1.5-7b-instruct",
                placeholder="Enter vision model name (e.g., accounts/fireworks/models/llava-v1.5-7b-instruct)",
                show_label=True
            )
        
        with gr.Group(elem_classes="input-group analysis-box"):
            analysis_type = gr.Dropdown(
                label="📊 Analysis Type",
                choices=[
                    "General Description",
                    "Object Detection",
                    "Scene Understanding",
                    "Text Recognition (OCR)",
                    "Emotion & Mood",
                    "Detailed Analysis"
                ],
                value="General Description",
                interactive=True
            )
        
        with gr.Group(elem_classes="input-group image-section"):
            image_input = gr.Image(
                label="📷 Upload Image",
                type="filepath",
                show_label=True,
                elem_classes="image-upload"
            )
        
        analyze_btn = gr.Button("🔍 Analyze Image 🔍", elem_classes="analyze-btn", size="lg")
        
        with gr.Group(elem_classes="output-box"):
            analysis_output = gr.Textbox(
                label="📋 Analysis Results",
                lines=15,
                show_label=True,
                interactive=False
            )
    
    gr.Markdown("<div class='footer-text'>Made with 💜 using Vision Agent</div>", elem_id="footer")
    
    # Set up the button click event
    analyze_btn.click(
        fn=analyze_image,
        inputs=[api_key_input, model_input, image_input, analysis_type],
        outputs=analysis_output
    )

if __name__ == "__main__":
    # Find an available port
    port = find_available_port()
    if port:
        print(f"🚀 Vision Agent is starting on port {port}")
        print(f"📱 Access the app at: http://localhost:{port}")
        demo.launch(
            server_name="0.0.0.0",
            server_port=port,
            share=False,
            show_error=True,
            css=custom_css
        )
    else:
        print("❌ Could not find an available port. Please try again.")