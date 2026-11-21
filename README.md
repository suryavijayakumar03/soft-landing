# 🌱 Soft Landing — AI-Powered Mental Wellness Newsletter

> Fully automated twice-weekly mental wellness newsletter, built with Claude AI + Beehiiv + Python + cron. Set it up once, runs forever.

## 🧠 What It Does

1. **Generates** a fresh wellness article using Claude AI (12 rotating themes)
2. **Formats** it as a beautiful HTML email
3. **Posts** it to Beehiiv automatically
4. **Runs** every Monday & Thursday at 7:30 AM IST via cron — zero manual work

## 🌿 Wellness Themes (Auto-Rotating)

Mindfulness, anxiety management, emotional resilience, healthy boundaries, self-compassion, burnout recovery, grief & transitions, finding purpose, digital wellness, sleep & rest, loneliness, career changes.

## 🛠️ Tech Stack

- **AI:** Anthropic Claude API (claude-sonnet-4-6)
- **Newsletter:** [Beehiiv](https://beehiiv.com) (free up to 2,500 subscribers)
- **Language:** Python 3
- **Scheduling:** cron

## 📦 Installation

**1. Clone the repo**
\`\`\`bash
git clone https://github.com/suryavijayakumar03/soft-landing.git
cd soft-landing
\`\`\`

**2. Install dependencies**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

**3. Create your .env file**
\`\`\`bash
cp .env.example .env
\`\`\`
Edit \`.env\` with your credentials:
\`\`\`
ANTHROPIC_API_KEY=sk-ant-...your-key-here...
BEEHIIV_API_KEY=your-beehiiv-api-key
BEEHIIV_PUBLICATION_ID=pub_...your-publication-id...
\`\`\`

**4. Test manually**
\`\`\`bash
python automation.py
\`\`\`

**5. Set up cron (runs automatically forever)**
\`\`\`bash
crontab -e
\`\`\`
Add (Mon & Thu at 2:00 AM UTC = 7:30 AM IST):
\`\`\`
0 2 * * 1 cd /Users/YOUR_USERNAME/soft-landing && python automation.py >> ~/soft-landing-cron.log 2>&1
0 2 * * 4 cd /Users/YOUR_USERNAME/soft-landing && python automation.py >> ~/soft-landing-cron.log 2>&1
\`\`\`

## ⚙️ Getting Your API Keys

| Key | Where to get it |
|-----|----------------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys) |
| `BEEHIIV_API_KEY` | Beehiiv Dashboard → Settings → API |
| `BEEHIIV_PUBLICATION_ID` | Beehiiv Dashboard → Settings → Publication |

## 🔒 Safety Guardrails

- ✅ Warm, evidence-based, compassionate content only
- ✅ Recommends professional help when appropriate
- ❌ No medical/psychiatric advice
- ❌ No crisis or self-harm content

## 📄 License

MIT

## 👤 Author

Built by [Surya VJ](https://github.com/suryavijayakumar03) — Salesforce Admin & Business Systems Engineer

*Powered by [Anthropic Claude AI](https://anthropic.com) · Newsletter by [Beehiiv](https://beehiiv.com)*
