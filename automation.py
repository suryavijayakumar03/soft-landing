"""
Soft Landing Newsletter - Full Automation Script
Generates content with Claude API and posts to Beehiiv automatically.
Run manually or schedule with cron.

Schedule: Every Monday and Thursday at 8:00 AM IST
"""

import anthropic
import requests
import json
import os
import pytz
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ── CONFIG ──────────────────────────────────────────────────────────────────
BEEHIIV_API_KEY   = os.environ["BEEHIIV_API_KEY"]
PUB_ID            = os.environ["BEEHIIV_PUBLICATION_ID"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
BEEHIIV_BASE      = "https://api.beehiiv.com/v2"
# ────────────────────────────────────────────────────────────────────────────

THEMES = [
    "Starting where you are — moving forward without needing to feel ready",
    "Permission to pause — rest as a productive act, not a failure",
    "Action without motivation — doing small things when you don't feel like it",
    "Coming back after disappearing — returning to routines without shame",
    "Comparison and self-worth — measuring your life against yourself, not others",
    "The power of one good decision — how small choices compound over time",
    "Dealing with uncertainty — sitting with not-knowing without panic",
    "Saying no without guilt — protecting your energy as an act of self-respect",
    "What consistency actually looks like — small, boring, and powerful",
    "Being a beginner — starting something new without needing to be good at it",
    "Emotional fatigue — when you're tired of being strong",
    "Celebrating tiny wins — why small progress deserves real acknowledgment",
]

SYSTEM_PROMPT = """You are the voice of Soft Landing — a mental wellness newsletter.

Your tone is:
- Warm, like a thoughtful friend who has been through hard things
- Minimal — no fluff, no filler, every sentence earns its place
- Honest — you don't pretend everything is fine, but you hold space for hope
- Never preachy, never clinical, never toxic-positive

Your writing style:
- Short paragraphs (2-3 sentences max)
- Use em dashes, not exclamation points
- Occasional bold for key phrases, never for decoration
- One blockquote per issue — a simple, honest sentence
- End with a small actionable reflection (not a task — a practice)

The reader is someone having a hard time. They're smart, tired, and don't need more advice — they need perspective and permission."""


def get_theme_for_today():
    week_num = datetime.now().isocalendar()[1]
    return THEMES[week_num % len(THEMES)]


def generate_newsletter_content(theme: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = f"""Write a complete Soft Landing newsletter issue on this theme:

THEME: {theme}

FORMAT:
- Subject line (compelling, 6-9 words, no clickbait)
- Preview text (1 sentence, 15-20 words)
- Full newsletter body in HTML format

The newsletter body should include:
1. A short opening (2-3 paragraphs) — name the feeling without being dramatic
2. A section heading + 3-4 paragraphs of gentle perspective
3. One blockquote (a single honest sentence)
4. "This week's soft landing" — one small practice to try
5. A simple sign-off: "Until [Monday/Thursday]," then "Soft Landing"

Return your response as JSON with these exact keys:
{{
  "subject_line": "...",
  "preview_text": "...",
  "content_html": "..."
}}

Use proper HTML tags: <p>, <h2>, <blockquote>, <strong>, <em>, <hr>, <br>"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = message.content[0].text
    start = raw.find("{")
    end = raw.rfind("}") + 1
    return json.loads(raw[start:end])


def get_next_send_time():
    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)
    weekday = now.weekday()
    days_to_monday = (7 - weekday) % 7 or 7
    days_to_thursday = (3 - weekday) % 7 or 7
    days_ahead = min(days_to_monday, days_to_thursday)
    next_send = now + timedelta(days=days_ahead)
    next_send = next_send.replace(hour=8, minute=0, second=0, microsecond=0)
    send_time_utc = next_send.astimezone(pytz.utc)
    return send_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"), next_send


def post_to_beehiiv(subject: str, preview: str, html: str, send_at: str) -> bool:
    headers = {
        "Authorization": f"Bearer {BEEHIIV_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "title": subject,
        "subject_line": subject,
        "preview_text": preview,
        "body_content": html,
        "body_content_type": "html",
        "status": "confirmed",
        "scheduled_at": send_at,
    }
    resp = requests.post(
        f"{BEEHIIV_BASE}/publications/{PUB_ID}/posts",
        headers=headers,
        json=payload
    )
    return resp.status_code in (200, 201), resp.json()


def run():
    print("=" * 50)
    print("Soft Landing Newsletter Automation")
    print("=" * 50)

    theme = get_theme_for_today()
    print(f"\n📌 Theme: {theme}")

    print("\n✍️  Generating content with Claude...")
    content = generate_newsletter_content(theme)
    print(f"   Subject: {content['subject_line']}")

    send_at_iso, send_time_ist = get_next_send_time()
    print(f"\n📅 Scheduling for: {send_time_ist.strftime('%A, %B %d %Y at %I:%M %p IST')}")

    print("\n🚀 Posting to Beehiiv...")
    success, response = post_to_beehiiv(
        content["subject_line"],
        content["preview_text"],
        content["content_html"],
        send_at_iso
    )

    if success:
        post_id = response.get("data", {}).get("id", "unknown")
        print(f"\n✅ SUCCESS!")
        print(f"   Post ID: {post_id}")
        print(f"   Scheduled: {send_time_ist.strftime('%A, %B %d %Y at %I:%M %p IST')}")
    else:
        print(f"\n❌ Failed to post")
        print(json.dumps(response, indent=2))


if __name__ == "__main__":
    run()
