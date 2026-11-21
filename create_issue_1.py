"""
Soft Landing Newsletter - Issue #1 Creator
Run this once to create and schedule Issue #1 in Beehiiv
"""

import requests
import json
from datetime import datetime
import pytz

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY = "la1eMcAuIITXvCFJdlmm5TZxrTsKhe8ISSesagibmPgk3cevGIlXS99EIqS1WEwM"
PUB_ID  = "pub_eed7b591-81be-4062-a37e-ba022cd9ab2b"
BASE    = "https://api.beehiiv.com/v2"
# ────────────────────────────────────────────────────────────────────────────

# Monday Nov 23 2026 at 08:00 IST → UTC
ist = pytz.timezone("Asia/Kolkata")
send_time_ist = ist.localize(datetime(2026, 11, 23, 8, 0, 0))
send_time_utc = send_time_ist.astimezone(pytz.utc)
send_at_unix  = int(send_time_utc.timestamp())

SUBJECT  = "You Don't Have to Fix Everything Today"
SUBTITLE = "A gentle reminder for the days when everything feels like too much."

# Full HTML content for Issue #1
CONTENT_HTML = """
<p>Hi there,</p>

<p>Some days, the to-do list feels like a wall.</p>

<p>Not just long — but solid. Unmovable. And somewhere in the middle of staring at it, you start to believe that if you can't get through all of it, you've already failed.</p>

<p>You haven't.</p>

<hr>

<h2>Starting where you are</h2>

<p>There's a quiet pressure that builds when life gets heavy — the pressure to <em>fix it</em>. All of it. Now.</p>

<p>Fix the sleep. Fix the job situation. Fix the relationship. Fix the habits. Fix the apartment. Fix yourself.</p>

<p>And somewhere in the middle of all that fixing, you forget to just... be. To exist without being a project.</p>

<p>Here's something worth sitting with:</p>

<blockquote><strong>You are not behind. There is no schedule you're failing to keep up with. There is only today, and what's actually possible in it.</strong></blockquote>

<hr>

<h2>One thing, not everything</h2>

<p>When you're overwhelmed, the instinct is to do more — to push harder, to make up for lost time.</p>

<p>But overwhelm doesn't respond to force. It responds to focus.</p>

<p>Instead of asking <em>"How do I fix everything?"</em> — ask this:</p>

<p><strong>What is one small thing I can do today that future-me will be grateful for?</strong></p>

<p>Not ten things. Not the whole list. One.</p>

<p>Maybe it's drinking a glass of water before you open your phone.<br>
Maybe it's sending one email you've been avoiding.<br>
Maybe it's going for a 10-minute walk after lunch.<br>
Maybe it's just getting dressed.</p>

<p>One thing. That's enough.</p>

<hr>

<h2>This week's soft landing</h2>

<p>Try this tonight before you sleep:</p>

<p>Write down three things that happened today — not achievements, not tasks completed. Just three things that <em>happened</em>. A conversation. Something you noticed. A moment that felt okay.</p>

<p>That's it. No evaluation. No grading yourself.</p>

<p>Just noticing that the day existed, and you were in it.</p>

<hr>

<p>Until Thursday,<br>
<em>Soft Landing</em></p>

<p><small>You're receiving this because you signed up for Soft Landing — a twice-weekly letter about navigating hard days with a little more gentleness. If this isn't for you, no hard feelings. Unsubscribe anytime below.</small></p>
"""

def create_and_schedule_post():
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "title": SUBJECT,
        "subject_line": SUBJECT,
        "preview_text": SUBTITLE,
        "body_content": CONTENT_HTML,
        "body_content_type": "html",
        "status": "confirmed",
        "scheduled_at": send_time_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    print(f"Creating post: '{SUBJECT}'")
    print(f"Scheduled for: {send_time_ist.strftime('%A, %B %d %Y at %I:%M %p IST')}")
    print("Sending to Beehiiv API...")

    resp = requests.post(
        f"{BASE}/publications/{PUB_ID}/posts",
        headers=headers,
        json=payload
    )

    if resp.status_code in (200, 201):
        data = resp.json()
        post_id = data.get("data", {}).get("id", "unknown")
        print(f"\n✅ SUCCESS! Post created.")
        print(f"   Post ID: {post_id}")
        print(f"   Scheduled: Monday Nov 23, 2026 at 8:00 AM IST")
        print(f"\nCheck your Beehiiv dashboard → Newsletter → Posts")
    else:
        print(f"\n❌ Error {resp.status_code}")
        print(resp.text)

if __name__ == "__main__":
    create_and_schedule_post()
