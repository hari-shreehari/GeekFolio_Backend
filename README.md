# PyServer

# Resume Extraction API

This API server allows you to upload resumes in various formats (PDF, DOCX, ODT, PNG) and returns structured data extracted from these documents. It uses Uvicorn and FastAPI to serve the API, and requires OCR and other processing tools.

## Requirements

This project requires a few system packages for text extraction and OCR processing. Run the following command to install them:


### Dependencies:

      - tesseract
      - poppler-utils
      - swig
      - libpulse

```bash
sudo apt install tesseract-ocr poppler-utils swig libpulse-dev
```

### Setup

This project uses Conda to manage dependencies. Make sure you have Miniconda or Anaconda installed. Then, set up the environment with the following steps:

### Clone the repository:

```bash
git clone https://github.com/Geekfolio/PyServer
cd PyServer
```

### Create and activate the environment from the environment.yaml file:

```bash
conda env create -f environment.yaml
conda activate vult
```

### Running the API Server

To start the server in development mode, use the following command:
```bash
uvicorn main:app --reload
```

This will start the server at http://127.0.0.1:8000.

### Usage

You can send POST requests to upload a resume file to the endpoint /upload. The server will process the file and return structured data in JSON format.
Example Request

```bash
curl -X POST "http://127.0.0.1:8000/extract" -F "file=@path_to_resume"
```
Replace path_to_resume with the path to your resume file.



# Deploy FastAPI on Render

Use this repo as a template to deploy a Python [FastAPI](https://fastapi.tiangolo.com) service on Render.

See https://render.com/docs/deploy-fastapi or follow the steps below:

## Manual Steps

1. You may use this repository directly or [create your own repository from this template](https://github.com/render-examples/fastapi/generate) if you'd like to customize the code.
2. Create a new Web Service on Render.
3. Specify the URL to your new repository or this repository.
4. Render will automatically detect that you are deploying a Python service and use `pip` to download the dependencies.
5. Specify the following as the Start Command.

    ```shell
    uvicorn main:app --host 0.0.0.0 --port $PORT
    ```

6. Click Create Web Service.

Or simply click:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/render-examples/fastapi)

## Thanks

Thanks to [Harish](https://harishgarg.com) for the [inspiration to create a FastAPI quickstart for Render](https://twitter.com/harishkgarg/status/1435084018677010434) and for some sample code!
