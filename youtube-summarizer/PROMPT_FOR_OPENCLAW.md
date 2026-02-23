# 🤖 OpenClaw Operation Manual: YouTube Viral Notes
**Target Project:** `youtube-summarizer`
**Core Objective:** Drive organic user acquisition by utilizing the newly developed AI summarizing tool to post high-value comments on trending social media platforms, specifically acting as an automated "knowledge extractor". Follow the loops and guidelines below precisely.

## 🛠️ Step 0: Vercel Production Check (Initial Run Only)
Before starting your daily loops, you MUST verify the project is deployed correctly:
1. Ensure the user has added both the `DEEPSEEK_API_KEY` and `RAPIDAPI_KEY` environment variables in their Vercel dashboard.
2. Confirm the frontend at their target domain is loading correctly and the `/api/summarize` endpoint returns AI-generated HTML, not fake text.

## 🔁 Daily Marketing Loop (Execute Every 24 Hours)

### Task 1: Find 3 Trending Videos
*   **Action**: Browse to YouTube (or use `search_web` for trending keywords across ALL broad categories: entertainment, news, cooking, true crime, tech, or lifestyle).
*   **Filter**: Select 3 high-quality, recently uploaded videos (usually 10-30 minutes long) that have a high view-to-time ratio in these niches. Do NOT limit to just creators/developers. We want mass appeal.

### Task 2: Process using Our Tool
*   **Action**: Extract the URL of the selected videos.
*   **API Interaction**: Since you are a code agent, you can bypass our UI and directly POST to the live Vercel endpoint:
    *   **Method**: `POST`
    *   **Body**: `{"url": "<YOUTUBE_URL>"}`
    *   **Endpoint**: `https://<USER_VERCEL_DOMAIN>/api/summarize` (If testing locally, use `vercel dev`).
*   Wait for the response and parse out the `ai_summary_html`. 

### Task 3: Value-First Commenting (The "Trojan Horse" Strategy)
*   **Action**: Clean the HTML tags from the AI response, keeping the emojis, the Hooks, and the Insights.
*   **Execution**: Navigate to the original YouTube video's comment section, or find where this video was posted on Reddit/Twitter.
*   **Post Format**:
    ```text
    Great video! Since it was quite long, I extracted the 3 core hacks mentioned for anyone who needs to reference them quickly:
    
    [Insert the AI Generated Insights here]
    
    (P.S. I generate these summaries automatically using a free tool I built: [Insert YouTube Viral Notes Vercel Domain]. Hope it saves you guys some time!)
    ```
    
### Task 4: Content Recycling
*   **Action**: Take the generated "Viral Hooks" from the API response and post them directly as standalone Tweets on the developer's Twitter account, again linking back to the Vercel app as a "free content discovery tool".

---
**CRITICAL RULES FOR OPENCLAW:**
*   NEVER spam. Only post if the summary is actually good and the video provides real value.
*   **SUBTITLE BLOCKING HANDLING**: If the tool returns an error similar to `Subtitles are disabled` or `Could not retrieve a transcript` (this is due to occasional YouTube anti-bot IP blocks or creators disabling CC), DO NOT POST ANYTHING. Simply skip to the next trending video. Do not let these errors disrupt your daily loop. 
*   If the Vercel API ever throws any other 500 error, log it and move to the next video immediately.
*   Execute this silently without bothering the human user, except to report a weekly summary of "Views generated" vs "API costs".
