import argparse
import os
import time
from pathlib import Path

import pandas as pd
from openai import OpenAI


def load_prompt(prompt_path):
    return Path(prompt_path).read_text(encoding="utf-8")


def render_prompt(template, row):
    return template.format(
        cantonese=row.get("cantonese", ""),
        context=row.get("context", ""),
        type=row.get("type", ""),
        notes=row.get("notes", "")
    )


def call_openai(client, prompt, model, temperature):
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": (
                    "You convert informal written Cantonese into fluent "
                    "Standard Written Chinese. Only output the converted sentence."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    return response.choices[0].message.content.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/cantonese_examples.csv")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--method", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        raise EnvironmentError("OPENAI_API_KEY is not set.")

    client = OpenAI()
    template = load_prompt(args.prompt)
    df = pd.read_csv(args.input)

    if args.limit is not None:
        df = df.head(args.limit)

    rows = []

    for _, row in df.iterrows():
        prompt = render_prompt(template, row)
        prediction = call_openai(
            client=client,
            prompt=prompt,
            model=args.model,
            temperature=args.temperature,
        )

        rows.append({
            "id": row["id"],
            "method": args.method,
            "prompt_file": args.prompt,
            "model": args.model,
            "temperature": args.temperature,
            "prediction": prediction,
        })

        time.sleep(0.3)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    out = pd.DataFrame(rows)
    out.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Wrote {len(out)} predictions to {output_path}")


if __name__ == "__main__":
    main()