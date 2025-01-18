from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
import json
import logging
import google.generativeai as genai
from pathlib import Path

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Access the Google API key
google_api_key = os.getenv("GOOGLE_API_KEY")

# FastAPI app initialization
app = FastAPI()

# Configure GenAI and the model
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/extract")
async def extract_text_from_resume():
    return {"message": "Upload a resume file to extract text."}


@app.post("/extract")
async def extract_text_from_resume(file: UploadFile = File(...)):
    try:
        # Save the uploaded file to the server
        file_location = f"/tmp/{file.filename}"
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Upload the file to the Generative AI model
        genai_file = genai.upload_file(file_location)
        logger.info(f"Uploaded file to GenAI: {genai_file=}")

        # Construct the prompt
        prompt = '''
        Can you analyze the attached resume file and convert it into the following structured JSON format?

        Only output valid JSON. Do not include any extra commentary or text, just the JSON data. Leave any missing fields empty as shown in the format.

        Format the content in the resume to this JSON: {{
        "personal_information": [
            {{
            "name": [""],
            "contact_information": [
                {{
                "phone_number": [""],
                "email": [""],
                "address": [""]
                }}
            ],
            "linkedin_profile": [""],
            "github_profile": [""],
            "objective_summary": [
                {{
                "career_objective": [""],
                "professional_summary": [""]
                }}
            ]
            }}
        ],
        "education": [
            {{
            "degree": [""],
            "major_field_of_study": [""],
            "university_institution_name": [""],
            "graduation_date": [""],
            "cgpa_grades": [""]
            }}
        ],
        "experience": [
            {{
            "job_title": [""],
            "company_name": [""],
            "location": {{
                "city": [""],
                "state": [""]
            }},
            "dates_of_employment": {{
                "start_date": [""],
                "end_date": [""]
            }},
            "responsibilities_achievements": [""]
            }}
        ],
        "projects": [
            {{
            "project_title": [""],
            "technologies_used": [""],
            "project_description": [""],
            "duration": {{
                "start_date": [""],
                "end_date": [""]
            }},
            "project_links": [""]
            }}
        ],
        "certifications": [
            {{
            "certification_title": [""],
            "issuing_organization": [""],
            "date_obtained": [""]
            }}
        ],
        "skills": {{
            "technical_skills": [""],
            "soft_skills": [""]
        }},
        "achievements": {{
            "awards_honors": [""],
            "scholarships": [""],
            "competitions": [""]
        }},
        "extracurricular_activities": {{
            "clubs_organizations": [""],
            "volunteer_work": [""],
            "leadership_roles": [""]
        }},
        "languages": [
            {{
            "language_proficiency": [""],
            "level_of_proficiency": [""]
            }}
        ]
        }}
        '''

        # Generate content from the model
        result = model.generate_content([genai_file, "\n\n", prompt])
        response_text = result.text
        
        # response_json = json.loads(response_text)

        # Return the parsed JSON directly
        return JSONResponse(content={"structured_json": response_text})

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
        
if __name__ == "_main_":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
