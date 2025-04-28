
# Russian Text Enhancer

This application processes transcribed Russian text through GPT-4o to improve readability while preserving content. It fixes punctuation, improves structure, and renders text in an easy-to-read format.

## Features

- Process Russian text with OpenAI's GPT-4o model
- Split long texts into manageable chunks by sentence count or character count
- Format output as clean plain text
- Support for both direct text input and file uploads
- Download processed results as text files

## Getting Started

### Prerequisites

- An OpenAI API key (with access to GPT-4o model)

### Setup

1. Add your OpenAI API key to the Secrets tab in Replit:
   - Click on "Tools" in the sidebar
   - Select "Secrets"
   - Add a new secret with the key `OPENAI_KEY` and your API key as the value

2. Run the application:
   - Click the "Run" button at the top of the Replit window

### Using the Application

1. **Input Your Text**:
   - Choose between "Paste Text" or "Upload File"
   - For text input, paste your Russian text in the provided text area
   - For file upload, select a `.txt` file containing Russian text

2. **Configure Processing Options**:
   - Choose a chunking method:
     - **By Sentence Count**: Splits text into chunks with specified number of sentences
     - **By Character Count**: Splits text by character count

   - Adjust the chunk size using the slider:
     - For sentence count: 20-150 sentences per chunk (default: 50)
     - For character count: 1000-10000 characters per chunk (default: 4000)

3. **Process the Text**:
   - Click "Process Text" to send your text to GPT-4o
   - A progress bar will show the processing status

4. **View and Save Results**:
   - The processed text appears in the "Processed Text" section
   - Use the "Download processed text as TXT" button to save the result

## How It Works

The application:
1. Splits your text into manageable chunks
2. Sends each chunk to OpenAI's GPT-4o with instructions to:
   - Preserve all content
   - Fix punctuation and structure
   - Organize text into logical blocks with headings
   - Format lists and examples clearly
   - Maintain the author's style and tone

## Troubleshooting

- **API Key Issues**: Ensure your OpenAI API key is correctly added to Secrets
- **Processing Errors**: For very long texts, try using smaller chunk sizes
- **Rate Limits**: If you encounter rate limits, wait a few minutes before trying again

## Limitations

- The application requires an OpenAI API key with access to GPT-4o
- Processing very large texts may take time and incur API usage costs

## Note

This application processes text through OpenAI's GPT-4o. While it aims to preserve content, the AI may occasionally make small adjustments to improve readability. Always review the processed text.
