# AI-Powered Legal Analysis Platform - Legal Analysis Tool

An NLP-driven application leveraging large language models to analyze legal incidents and provide actionable insights within Indian jurisprudence.

## Features

- Simple web interface for incident reporting
- AI-powered legal analysis using Llama API
- Identification of applicable laws and IPC sections
- Recommended steps and additional guidance
- Responsive design for desktop and mobile use

## Technologies

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Llama-7b LLM API
- **Architecture**: RESTful API

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/legal-analysis-platform.git
   cd legal-analysis-platform
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API key:
   ```
   LLAMA_API_KEY=your_api_key_here
   ```

4. Run the application:
   ```
   python app.py
   ```

## Deployment

This application is ready for deployment on Vercel:

1. Ensure `requirements.txt` contains all dependencies
2. Create `vercel.json` in the project root:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "/app.py"
       }
     ]
   }
   ```
3. Connect your repository to Vercel and deploy

## Limitations

- This tool provides preliminary legal analysis only
- Not a substitute for professional legal advice
- Analysis quality depends on input detail and API capabilities

## License

MIT
