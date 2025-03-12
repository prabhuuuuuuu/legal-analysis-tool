from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = Flask(__name__)
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
LLAMA_API_URL = "https://api.llama-api.com/v1/chat/completions"  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_incident():
    incident_data = request.json
    
    if not incident_data.get('description'):
        return jsonify({
            "error": "Incident description is required"
        }), 400
    
    prompt = f"""
    Analyze the following incident from a legal perspective in India:
    
    Type: {incident_data.get('type', 'Not specified')}
    Date: {incident_data.get('date', 'Not specified')}
    Location: {incident_data.get('location', 'Not specified')}
    
    Description:
    {incident_data.get('description')}
    
    Additional Information:
    {incident_data.get('additionalInfo', 'None provided')}
    
    Please provide:
    1. Applicable constitutional laws and legal frameworks
    2. Relevant IPC sections that apply to this case
    3. Recommended steps the person should take
    4. Any additional legal guidance or considerations
    """
    
    try:
        response = requests.post(
            LLAMA_API_URL,
            headers={
                "Authorization": f"Bearer {LLAMA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-7b-chat", 
                "messages": [
                    {"role": "system", "content": "You are a legal assistant specializing in Indian law."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
        )
        
        api_response = response.json()
        
        if 'choices' in api_response and len(api_response['choices']) > 0:
            llama_response = api_response['choices'][0]['message']['content']
            
            sections = llama_response.split('\n\n')
            
            result = {
                "applicableLaws": "",
                "ipcSections": "",
                "recommendedSteps": "",
                "additionalGuidance": ""
            }
           
            for section in sections:
                if "constitutional" in section.lower() or "applicable laws" in section.lower():
                    result["applicableLaws"] = section
                elif "ipc section" in section.lower():
                    result["ipcSections"] = section
                elif "steps" in section.lower() or "should take" in section.lower():
                    result["recommendedSteps"] = section
                elif "additional" in section.lower() or "guidance" in section.lower():
                    result["additionalGuidance"] = section
            
            return jsonify(result)
        else:
            return jsonify({
                "applicableLaws": "Unable to determine applicable laws from the description provided.",
                "ipcSections": "Further consultation with a legal professional is recommended to identify relevant IPC sections.",
                "recommendedSteps": "1. Document all evidence related to the incident.\n2. Consult with a legal professional for specific guidance.",
                "additionalGuidance": "This is a preliminary analysis only. Please consult with a qualified legal professional for definitive legal advice."
            })
            
    except Exception as e:
        print(f"Error calling Llama API: {e}")
        return jsonify({
            "error": "Unable to process your request at this time. Please try again later."
        }), 500


if __name__ == '__main__':
    app.run(debug=True)