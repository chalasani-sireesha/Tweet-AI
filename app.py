
import os
import re
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="BrandTweet AI",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ BrandTweet AI")
st.subheader("Your AI-powered brand voice and tweet generator")

st.write(
    "Enter your brand details and generate 10 creative "
    "tweets that match your brand personality."
)

# Read API key securely
api_key = None

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")


def generate_demo(brand, industry, objective, products):
    """Sample output for testing without an API key."""

    if brand.lower() == "nike":
        tone = [
            "Bold, motivational and confident.",
            "Audience: athletes and fitness enthusiasts.",
            "Themes: progress, training and personal achievement.",
            "Style: energetic language and clear calls to action."
        ]

        tweets = [
            "Your next personal best starts with one step. Make it count.",
            "Morning run or evening workout? Tell us your routine!",
            "Show up, put in the work, and celebrate every small win.",
            "Your alarm said snooze. Your goals said move. Who won?",
            "Progress is progress, even when nobody else sees it.",
            "Every athlete starts somewhere. What's your first memory of sport?",
            "Find the gear that moves with you through every mile.",
            "One more rep. One more lap. One more reason to be proud.",
            "Your journey, your pace, your goals. Keep moving forward.",
            "What's one fitness goal you're working toward this week?"
        ]

    elif brand.lower() == "amul":
        tone = [
            "Playful, witty and friendly.",
            "Audience: food lovers and Indian families.",
            "Themes: food, everyday moments and light humor.",
            "Style: conversational Indian English and playful wordplay."
        ]

        tweets = [
            "A little butter on your toast. A little happiness in your day!",
            "Breakfast is calling. What's on your plate today?",
            "When life gives you bread, make it butter-ful!",
            "Dosa, paratha or toast? Let the breakfast debate begin!",
            "Good food and good company make everyday moments special.",
            "Your evening snack deserves a little extra love.",
            "From morning toast to family recipes, food brings us together.",
            "Tag the friend who always asks for one more bite!",
            "Some conversations are better over a plate of favorite snacks.",
            "What's your all-time favorite comfort food? Tell us below!"
        ]

    else:
        tone = [
            "Friendly and conversational.",
            "Audience: customers interested in the brand's industry.",
            "Themes: product benefits, customer engagement and awareness.",
            "Style: clear, approachable language with varied content."
        ]

        tweets = [
            f"Meet {brand}: discover something new in {industry or 'our world'}.",
            f"What do you look for most in {products or 'a great product'}?",
            f"Small details can make a big difference. Explore {brand} today.",
            f"Let's talk about what matters to you. What should {brand} improve?",
            f"Discover how {products or brand} can fit into your everyday life.",
            f"Your opinion matters! Tell us what you want to see from {brand}.",
            f"Curious about {brand}? Start by exploring what makes us different.",
            f"One question for our community: what do you value most in our industry?",
            f"Stay curious, keep learning, and discover more with {brand}.",
            f"Join the conversation! What would you like to know about {brand}?"
        ]

    return tone, tweets


def generate_with_ai(brand, industry, objective, products):
    client = Groq(api_key=api_key)

    prompt = f"""
You are an expert social media copywriter.

BRAND DETAILS
Brand: {brand or 'Not provided'}
Industry: {industry or 'Not provided'}
Campaign objective: {objective}
Products and services: {products or 'Not provided'}

TASK 1: Analyze the brand voice.
Write exactly 4 concise bullet points covering:
- Tone and personality
- Target audience
- Content themes
- Writing style

TASK 2: Generate exactly 10 different tweets.
Include a balanced mix of:
- Conversational and engagement-focused
- Promotional
- Witty or playful
- Informative or value-driven

RULES
1. Keep every tweet within 280 characters.
2. Match the inferred brand voice and campaign objective.
3. Avoid repeating the same idea.
4. Use emojis and hashtags only when appropriate.
5. Never invent discounts, prices, statistics or product claims.
6. Do not claim you analyzed live social media posts.
7. Use this format exactly:

VOICE:
- First point
- Second point
- Third point
- Fourth point

TWEETS:
1. [Style] Tweet text
2. [Style] Tweet text
Continue until number 10.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You create original, brand-appropriate social "
                    "media content. Follow the requested output format."
                )
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_completion_tokens=2500
    )

    return response.choices[0].message.content


def parse_output(output):
    voice_section = re.search(
        r"VOICE:\s*(.*?)\s*TWEETS:",
        output,
        re.IGNORECASE | re.DOTALL
    )

    tweets_section = re.search(
        r"TWEETS:\s*(.*)",
        output,
        re.IGNORECASE | re.DOTALL
    )

    if not voice_section or not tweets_section:
        raise ValueError(
            "The AI did not return the expected format. Try again."
        )

    voice = []

    for line in voice_section.group(1).splitlines():
        line = line.strip()
        line = re.sub(r"^[-•]\s*", "", line)

        if line:
            voice.append(line)

    tweet_matches = re.findall(
        r"^\s*(\d{1,2})[.)]\s*(?:\[([^\]]+)\]\s*)?(.*)",
        tweets_section.group(1),
        re.MULTILINE
    )

    tweets = []

    for number, style, content in tweet_matches:
        content = content.strip()

        if content:
            tweets.append({
                "number": int(number),
                "style": style.strip() if style else "General",
                "text": content
            })

    tweets.sort(key=lambda tweet: tweet["number"])

    return voice, tweets


with st.form("brand_form"):
    st.subheader("Tell us about your brand")

    brand = st.text_input(
        "Brand name (optional)",
        placeholder="e.g. Nike, Amul or your own brand"
    )

    industry = st.text_input(
        "Industry / category (optional)",
        placeholder="e.g. Sportswear, food, technology"
    )

    objective = st.selectbox(
        "Campaign objective",
        [
            "Engagement",
            "Promotion",
            "Brand awareness",
            "Product launch"
        ]
    )

    products = st.text_area(
        "Products or services (optional)",
        placeholder="Describe the products, benefits and target customers"
    )

    demo_mode = st.checkbox(
        "Use demo mode (no API key required)",
        value=not bool(api_key)
    )

    submitted = st.form_submit_button(
        "Generate 10 Tweets",
        use_container_width=True
    )


if submitted:
    if not brand.strip():
        st.warning(
            "Please enter a brand name to generate relevant tweets."
        )

    else:
        with st.spinner("Analyzing brand voice and generating tweets..."):
            try:
                if demo_mode:
                    voice, tweet_texts = generate_demo(
                        brand.strip(),
                        industry.strip(),
                        objective,
                        products.strip()
                    )

                    tweets = []

                    for index, text in enumerate(tweet_texts):
                        tweets.append({
                            "number": index + 1,
                            "style": "Demo",
                            "text": text
                        })

                else:
                    if not api_key:
                        st.error(
                            "API key not found. Add GROQ_API_KEY "
                            "to your environment or Streamlit secrets."
                        )
                        st.stop()

                    output = generate_with_ai(
                        brand.strip(),
                        industry.strip(),
                        objective,
                        products.strip()
                    )

                    voice, tweets = parse_output(output)

                if len(tweets) != 10:
                    st.error(
                        f"Expected 10 tweets but received "
                        f"{len(tweets)}. Please generate again."
                    )
                    st.stop()

                if any(len(tweet["text"]) > 280 for tweet in tweets):
                    st.error(
                        "At least one tweet exceeds 280 characters. "
                        "Please generate again."
                    )
                    st.stop()

                if not voice:
                    st.error("The brand voice summary is empty.")
                    st.stop()

                st.session_state["brand_voice"] = voice
                st.session_state["tweets"] = tweets
                st.session_state["brand"] = brand.strip()

            except Exception as error:
                st.error(f"Could not generate tweets: {error}")


if "tweets" in st.session_state:
    st.divider()

    st.header(
        f"Brand Voice: {st.session_state['brand']}"
    )

    for point in st.session_state["brand_voice"]:
        st.markdown(f"- {point}")

    st.header("Your 10 Tweets")

    all_tweets = []

    for tweet in st.session_state["tweets"]:
        st.markdown(
            f"**{tweet['number']}. {tweet['style']}**"
        )

        # Updated: show each tweet with a Copy button
        st.code(tweet["text"], language=None)

        st.caption(
            f"Characters: {len(tweet['text'])}/280"
        )

        all_tweets.append(
            f"{tweet['number']}. {tweet['text']}"
        )

    st.text_area(
        "All tweets — select and copy",
        value="\n\n".join(all_tweets),
        height=350
    )

    st.download_button(
        "Download tweets as TXT",
        data=(
            "Brand: " + st.session_state["brand"] + "\n\n"
            + "BRAND VOICE\n"
            + "\n".join(st.session_state["brand_voice"])
            + "\n\nTWEETS\n"
            + "\n\n".join(all_tweets)
        ),
        file_name="brand_tweets.txt",
        mime="text/plain"
    )
