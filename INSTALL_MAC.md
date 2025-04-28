
# Installing and Running Russian Text Enhancer on macOS

This guide will walk you through installing and running the Russian Text Enhancer application on your Mac.

## Prerequisites

- macOS 10.15 or newer
- Python 3.9 or newer
- OpenAI API key (with access to GPT-4o model)

## Installation Steps

1. **Clone or Download the Repository**

   Download the source code or clone the repository to your local machine.

2. **Open Terminal**

   Open Terminal from Applications > Utilities > Terminal.

3. **Navigate to the Project Directory**

   ```bash
   cd path/to/russian-text-enhancer
   ```

4. **Create and Configure Environment Variables**

   Create a `.env` file in the project directory:

   ```bash
   touch .env
   ```

   Open the file with a text editor and add your OpenAI API key:

   ```
   OPENAI_KEY=your_openai_api_key_here
   ```

   Replace `your_openai_api_key_here` with your actual OpenAI API key.

5. **Install Required Dependencies**

   Install the required Python packages:

   ```bash
   pip3 install -r requirements.txt
   ```

   This will install Streamlit, OpenAI, and other dependencies.

## Running the Application

1. **Start the Streamlit Application**

   ```bash
   streamlit run app.py
   ```

2. **Access the Application**

   The application will automatically open in your default web browser, or you can manually navigate to:

   ```
   http://localhost:8501
   ```

## Using the Application

1. Choose between pasting text directly or uploading a text file.
2. Configure the chunking method and size according to your needs.
3. Click "Process Text" to enhance your Russian text.
4. Download the processed text as a TXT file when complete.

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly added to the `.env` file
- **Dependencies Installation Errors**: Try updating pip before installing dependencies:
  ```bash
  pip3 install --upgrade pip
  ```
- **Port Already in Use**: If port 8501 is already in use, you can specify a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```

## Additional Resources

For more detailed information on how to use the application, refer to the main README.md file.
