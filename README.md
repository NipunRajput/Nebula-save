Nebula Save - AI News Presenter

Demo: [YouTube Demo Link](https://youtu.be/41IFPs7jMqk)

Nebula Save is an AI-powered web application designed to generate a virtual news presenter that reads text-based news articles with human-like voice synthesis, synchronized with dynamic facial animations. The application uses AWS Polly for text-to-speech functionality and Flask for backend operations.
Features

    Text-to-Speech Integration: Leverages AWS Polly to convert text into lifelike speech.
    Dynamic Facial Animations: Synchronizes spoken words with corresponding facial expressions.
   

Encryption and Decryption

This project securely handles sensitive AWS credentials using AES encryption. The encryption key is used to decrypt the encrypted AWS keys at runtime, ensuring that the credentials remain secure throughout the process.

Project Structure

    static/: Contains all static files including images, audio, and video.
    templates/: Holds HTML files for the web interface.
    app.py: The main Python file for the Flask application.
    requirements.txt: Lists all the required Python libraries for the project.
    .env: Stores configuration variables and sensitive information (not tracked in version control).

Installation Guide
1. Clone the Repository

bash

git clone https://yourrepositorylink.com/nebula-save.git
cd nebula-save

2. Install Dependencies

bash

pip install -r requirements.txt

Configuration
1. Setting Up AWS Polly

    Navigate to the AWS Management Console.
    Create or use existing AWS credentials (Access Key ID and Secret Access Key).
    Attach the necessary policy to your IAM user for Amazon Polly access.
    Add the AWS credentials to your .env file as follows:

plaintext

AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
FFMPEG_PATH=/path/to/ffmpeg

2. Local Configuration

Ensure environment variables are set by sourcing the .env file or exporting them directly in your terminal.
Running Locally

To run the application on your local machine, use:

bash

flask run or python app.py

Access the application by navigating to http://localhost:5000 in your web browser.

Usage

    Enter text into the textbox on the web interface.
    Submit the text to hear the AI-generated virtual presenter read the news while displaying synchronized facial animations.

Note: Rendering may take some time depending on the length of the text.
Troubleshooting

Ensure the following if you encounter issues:

    AWS credentials are correctly configured.
    Amazon Polly policies are properly set.
    The .env file exists and is correctly formatted.


