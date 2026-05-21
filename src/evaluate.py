import argparse
from pathlib import Path
from difflib import SequenceMatcher

import pandas as pd

try:
    from opencc import OpenCC
    cc = OpenCC("t2s")
except Exception:
    cc = None


def normalize_text(text):
    if pd.isna(text):
        return ""

    text = str(text).strip()

    # Convert Traditional Chinese to Simplified Chinese for fair scoring.
    if cc is not None:
        text = cc.convert(text)

    # Normalize some common punctuation spacing.
    text = text.replace("，", "，")
    text = text.replace("？", "？")
    text = text.replace("。", "。")
    text = text.replace(" ", "")

    return text


def char_f1(prediction, reference):
    prediction = normalize_text(prediction)
    reference = normalize_text(reference)

    if not prediction and not reference:
        return 1.0
    if not prediction or not reference:
        return 0.0

    pred_chars = list(prediction)
    ref_chars = list(reference)

    common = 0
    ref_used = [False] * len(ref_chars)

    for char in pred_chars:
        for i, ref_char in enumerate(ref_chars):
            if not ref_used[i] and char == ref_char:
                common += 1
                ref_used[i] = True
                break

    precision = common / len(pred_chars) if pred_chars else 0
    recall = common / len(ref_chars) if ref_chars else 0

    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def edit_similarity(prediction, reference):
    prediction = normalize_text(prediction)
    reference = normalize_text(reference)
    return SequenceMatcher(None, prediction, reference).ratio()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/cantonese_examples.csv")
    parser.add_argument("--predictions", default="results/direct_replacement_outputs.csv")
    parser.add_argument("--output", default="results/direct_replacement_scores.csv")
    args = parser.parse_args()

    data = pd.read_csv(args.data)
    preds = pd.read_csv(args.predictions)

    merged = preds.merge(
        data[["id", "cantonese", "mandarin_reference", "type"]],
        on="id",
        how="left"
    )

    rows = []

    for _, row in merged.iterrows():
        prediction = row["prediction"]
        reference = row["mandarin_reference"]

        norm_prediction = normalize_text(prediction)
        norm_reference = normalize_text(reference)

        rows.append({
            "id": row["id"],
            "type": row["type"],
            "method": row["method"],
            "cantonese": row["cantonese"],
            "prediction": prediction,
            "reference": reference,
            "normalized_prediction": norm_prediction,
            "normalized_reference": norm_reference,
            "exact_match": int(norm_prediction == norm_reference),
            "char_f1": char_f1(prediction, reference),
            "edit_similarity": edit_similarity(prediction, reference),
        })

    scores = pd.DataFrame(rows)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scores.to_csv(output_path, index=False, encoding="utf-8-sig")

    summary = scores.groupby("method").agg(
        n=("id", "count"),
        exact_match=("exact_match", "mean"),
        char_f1=("char_f1", "mean"),
        edit_similarity=("edit_similarity", "mean"),
    ).reset_index()

    summary_path = output_path.with_name(output_path.stem + "_summary.csv")
    summary.to_csv(summary_path, index=False, encoding="utf-8-sig")

    print("Summary:")
    print(summary)
    print()
    print(f"Wrote item-level scores to {output_path}")
    print(f"Wrote summary to {summary_path}")


if __name__ == "__main__":
    main()