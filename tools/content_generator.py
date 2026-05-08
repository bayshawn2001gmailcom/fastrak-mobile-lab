"""
Generate SEO-optimized content for fastrakmobilelab.com using Gemini API.
Usage:
  python tools/content_generator.py --keyword "mobile phlebotomy atlanta" \
      --supporting "in-home blood draw,mobile lab services" \
      --type service --output .tmp/content.html
"""
import os, sys, argparse
from dotenv import load_dotenv

load_dotenv()
load_dotenv(os.path.join(os.path.expanduser("~"), ".env"), override=False)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    sys.exit("Error: GEMINI_API_KEY must be set in ~/.env")

try:
    import google.generativeai as genai
except ImportError:
    sys.exit("Error: run 'pip install google-generativeai' first")

genai.configure(api_key=GEMINI_API_KEY)

BUSINESS_CONTEXT = """
Business: Fastrak Mobile Lab
Services: Mobile phlebotomy, in-home blood draw, specimen collection, mobile lab services
Target customers: Patients who can't travel to a lab, elderly, homebound, busy professionals
Differentiators: Licensed phlebotomists, fast turnaround, comes to you, serves the Atlanta metro area and surrounding Georgia communities
CTA: "Book your mobile blood draw today" — link to contact/booking page
Tone: Professional, trustworthy, reassuring. Not overly clinical. Speak to the patient's convenience and peace of mind.
"""

TEMPLATES = {
    "service": """Write an SEO-optimized service page for a mobile phlebotomy company.
Requirements:
- H1 must contain the primary keyword exactly
- First paragraph (100 words) must naturally include the primary keyword
- Include 3 H2 subheadings using supporting keywords where natural
- Include local trust signals (licensed professionals, serving [location implied by keyword], fast results)
- End with a clear CTA paragraph
- Word count: 650–900 words
- Output clean HTML (h1, h2, p, ul tags only — no divs, no inline styles)
- No keyword stuffing — write for humans first
""",
    "blog": """Write an SEO-optimized blog post for a mobile phlebotomy company.
Requirements:
- H1 must contain the primary keyword naturally
- Intro paragraph hooks the reader and includes primary keyword
- Include 3–4 H2 subheadings; use supporting keywords naturally in at least 2
- Include a practical FAQ section (3 questions) as an H2 at the end
- Local context where relevant
- CTA at the end directing readers to book
- Word count: 900–1200 words
- Output clean HTML (h1, h2, h3, p, ul, ol tags only)
""",
    "location": """Write an SEO-optimized location page for a mobile phlebotomy company.
Requirements:
- H1: "[Service] in [City/Area]" format using the primary keyword
- Mention the specific city/area multiple times naturally
- Include local trust signals and specifics (nearby landmarks/neighborhoods where relevant)
- 2 H2s covering: what to expect, who benefits from mobile phlebotomy
- CTA to book
- Word count: 500–700 words
- Output clean HTML
""",
    "faq": """Write an SEO-optimized FAQ page for a mobile phlebotomy company.
Requirements:
- H1 must contain primary keyword
- Include 8–10 FAQ items as H2 (question) + p (answer) pairs
- Questions should reflect real patient concerns: cost, insurance, what to prepare, turnaround time, who qualifies
- Answers: 2–4 sentences each, reassuring and clear
- Output clean HTML
"""
}


def generate_content(keyword, supporting, content_type, min_words=None):
    template = TEMPLATES.get(content_type, TEMPLATES["service"])
    supporting_str = ", ".join(supporting) if supporting else "none"

    prompt = f"""
{BUSINESS_CONTEXT}

Primary keyword: {keyword}
Supporting keywords: {supporting_str}

{template}
{"Minimum word count: " + str(min_words) if min_words else ""}

Generate the content now. Output only the HTML content — no markdown, no code fences, no explanation.
"""

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", required=True, help="Primary SEO keyword")
    parser.add_argument("--supporting", default="", help="Comma-separated supporting keywords")
    parser.add_argument("--type", default="service", choices=["service", "blog", "location", "faq"])
    parser.add_argument("--output", help="Output file path (default: print to stdout)")
    parser.add_argument("--min-words", type=int, help="Minimum word count override")
    args = parser.parse_args()

    supporting = [s.strip() for s in args.supporting.split(",") if s.strip()]
    content = generate_content(args.keyword, supporting, args.type, args.min_words)

    word_count = len(content.split())
    print(f"Generated {word_count} words", file=sys.stderr)

    if args.output:
        os.makedirs(os.path.dirname(args.output), exist_ok=True) if os.path.dirname(args.output) else None
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved to {args.output}", file=sys.stderr)
    else:
        print(content)


if __name__ == "__main__":
    main()
