import os, re, sys
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.environ["MODEL"]
API_BASE = os.environ["API_BASE"]
API_KEY = os.environ["LM_API_KEY"]

client = OpenAI(base_url=API_BASE, api_key=API_KEY)


def page_text(html):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def browse_and_summarize(html):
    """The agent: given a page, it summarizes it. No filtering on the fetched input."""
    return client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a web-browsing assistant. Summarize the page the user fetched."},
            {"role": "user", "content": f"Here is the fetched page content:\n\n{page_text(html)}"},
        ],
    ).choices[0].message.content


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "docs/malicious_page.html"
    html = open(path, encoding="utf-8").read()

    reply = browse_and_summarize(html)
    print("--- AGENT REPLY ---\n", reply)
