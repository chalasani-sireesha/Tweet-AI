# ✍️ BrandTweet AI – AI-Powered Brand Voice and Tweet Generator

## Project Overview

BrandTweet AI is a Python-based application that helps users generate social media tweets according to a brand's personality, industry, and campaign objectives.

The application analyzes the provided brand details and generates a brand voice summary along with 10 creative tweets.

## Features

- Accepts brand name and industry/category.
- Supports different campaign objectives.
- Generates a 4-point brand voice summary.
- Generates 10 creative social media tweets.
- Displays tweet character counts.
- Provides a copy option for individual tweets.
- Allows users to download tweets as a TXT file.
- Includes demo mode without an API key.
- Supports AI-powered generation using Groq API.

## Technologies Used

- Python
- Streamlit
- Groq API
- Llama 3.3 70B Versatile
- Regular Expressions

## Project Structure

```text
brandtweet-ai/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Open the project folder

```bash
cd brandtweet-ai
```

### Step 3: Create a virtual environment

```bash
python -m venv .venv
```

### Step 4: Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Run the application

```bash
streamlit run app.py
```

## Groq API Configuration

The application supports demo mode without an API key.

To enable AI-powered tweet generation:

1. Create an API key from https://console.groq.com/.
2. Set the API key as an environment variable.

Windows PowerShell:

```powershell
$env:GROQ_API_KEY="your_api_key"
```

3. Restart the Streamlit application.
4. Uncheck the demo mode option.

**Note:** Never upload your API key to GitHub.

## Sample Brands for Testing

| Brand | Industry | Campaign Objective |
|---|---|---|
| Nike | Sportswear | Engagement |
| Amul | Food | Brand Awareness |

## Application Output

The application generates:

1. Brand voice summary.
2. Ten campaign tweets.
3. Tweet character counts.
4. Copyable tweet boxes.
5. Downloadable TXT file.

## Future Enhancements

- Support more social media platforms.
- Add brand-specific hashtag suggestions.
- Improve brand voice analysis.
- Add tweet scheduling functionality.

## Author

Developed as a Python and AI-based social media content generation project.