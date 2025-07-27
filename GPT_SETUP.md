# GPT Integration Setup Guide

## Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an OpenAI account
3. Click "Create new secret key"
4. Copy the generated API key (starts with "sk-...")

## Setting Up the API Key

1. Open the `.env` file in the project root
2. Replace `your-openai-api-key-here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
3. Save the file

## Important Security Notes

- Never commit your `.env` file to version control
- Keep your API key secure and private
- The `.env` file is already in `.gitignore` to prevent accidental commits

## GPT Models Available

You can change the model in `.env`:
- `gpt-3.5-turbo` (default, cost-effective)
- `gpt-4` (more advanced, higher cost)
- `gpt-4-turbo` (balance of speed and capability)

## Cost Considerations

- GPT-3.5-turbo: ~$0.001-0.002 per report
- GPT-4: ~$0.03-0.06 per report
- You'll be charged based on token usage

## Fallback Behavior

If no API key is provided or the API fails:
- The system automatically falls back to statistical analysis
- You'll still get reports, just without GPT-enhanced insights
- The report will show "Statistical" instead of "GPT-Enhanced" analysis type
