Nebula Save - AI News Presenter
Demo: https://youtu.be/41IFPs7jMqk
Nebula Save is an AI-powered web application that generates a virtual news presenter capable of reading text-based news articles in a human-like voice, synchronized with facial animations. The application leverages AWS Polly for text-to-speech capabilities and Flask for backend operations.

Features
Text-to-Speech Integration: Utilizes AWS Polly to convert text into lifelike speech.
Dynamic Facial Animations: Synchronizes spoken words with facial expressions.
AWS Elastic Beanstalk Deployment: Supports deployment on AWS for scalability and easy management.

<img width="160" alt="{2105A945-931B-4DD0-810E-7F93F48FC5E1}" src="https://github.com/user-attachments/assets/6ff4b842-1a44-4002-95b7-74c99f1d538f">



static/: Contains all static files including images, audio, and video files.
templates/: Contains HTML files for the web interface.
app.py: The main Python Flask application file.
requirements.txt: Lists all Python libraries that the project depends on.
.env: Stores configuration variables and sensitive information, not tracked in version control.


To see the results, just scroll the website, it might take some time, the time depends on the amount of text submitted

Installation
Clone the repository to your local machine:

bash
Copy code
git clone https://yourrepositorylink.com/nebula-save.git
cd nebula-save
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Configuration
Setting Up AWS Polly
Navigate to the AWS Management Console.
Create or use existing AWS credentials (Access Key ID and Secret Access Key).
Attach a policy to your IAM user that allows access to Amazon Polly.
Set environment variables in .env for AWS access:
plaintext
Copy code
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
FFMPEG_PATH=/path/to/ffmpeg
Local Configuration
Set the environment variables by sourcing the .env file or exporting them directly in your terminal.

Running Locally
To run the application locally, execute:

bash
Copy code
flask run
Access the application via http://localhost:5000 in your web browser.

Deployment on AWS Elastic Beanstalk
Initialize Elastic Beanstalk CLI, configure your application, and create an environment:

bash
Copy code
eb init -p python-3.7 Nebula-save -r ap-south-1
eb create nebula-env
eb deploy
To open your deployed application:

bash
Copy code
eb open
Usage
Interact with the AI News Presenter through the web interface. Enter the text into the provided textbox, and submit it to see and hear the virtual avatar present the news based on the text provided.

Troubleshooting
Ensure the following if you face issues:

AWS credentials are correctly configured.
Policies for Amazon Polly are correctly set.
The .env file is not missing and correctly formatted.
Contributing
Contributions are welcome. Please fork the repository, make your changes, and submit a pull request.







