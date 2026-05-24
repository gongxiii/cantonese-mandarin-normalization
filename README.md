# Cantonese-to-Standard-Chinese Normalization

This project builds a small prototype for normalizing social-media-style written Cantonese into Standard Written Chinese. The focus is on orthographic and lexical variation in online Cantonese, including informal spellings, English code-mixing, nonstandard character choices, Cantonese slang, and sentence-final particles.

## Project Goal

Informal written Cantonese on social media is often difficult for automatic translation systems because the writing is not standardized. The same expression may appear in different forms, such as 有D, 有d, 個d, 你地, 佢地, 左, 既, like, post, or chok.

The goal is not to build a full Cantonese machine translation system. Instead, this is a small prototype and evaluation benchmark for one specific bottleneck: online Cantonese orthographic and lexical variation.

In this project, **Standard Written Chinese** refers to Mandarin-based written Chinese phrasing rather than simply the use of Simplified Chinese characters. Outputs are represented and evaluated in Simplified Chinese for consistency, but Traditional/Simplified script differences are not treated as normalization errors.

Although the task is framed as normalization, some examples require limited lexical paraphrasing or semantic interpretation, especially for Cantonese slang, idioms, and pragmatic sentence-final particles. The project therefore focuses on sentence-level normalization of informal written Cantonese into Mandarin-based Standard Written Chinese.

## Data Collection Notes

The dataset was collected from publicly visible online Cantonese comments, mainly from YouTube comments under Cantonese street-interview videos and discussions on Hong Kong online forums.

Only short standalone sentence-level examples are released. Usernames, user IDs, profile information, timestamps, URLs, and full discussion threads are not included. The context field is an author-written topic description rather than a copy of the surrounding online discussion.

For more details, see [`docs/data_collection_notes.md`](docs/data_collection_notes.md).

## Methods

I compare an off-the-shelf machine translation system, a rule-based baseline, and several GPT-based normalization prompts.

### 1. Google Translate

Google Translate is included as an off-the-shelf MT comparison system. Its outputs were collected manually from the Google Translate web interface for the 70 Cantonese input sentences.

The outputs were copied without semantic correction. Only formatting issues such as line breaks were cleaned before evaluation.

### 2. Direct replacement baseline

The direct replacement baseline is a simple rule-based prototype implemented in `src/dictionary_baseline.py`.

It uses a manually written replacement list for common Cantonese forms, informal spellings, code-mixed items, and slang. For example, it maps forms such as `有D`, `你地`, `唔`, `冇`, `like`, `post`, `拍拖`, and `收晒皮` to approximate Standard Chinese equivalents.

The baseline applies direct string replacement without tokenization, word-boundary control, or context-sensitive disambiguation. This makes the method transparent and easy to reproduce, but it also makes it vulnerable to substring replacement errors and unnatural word order.

This baseline is intentionally simple. It tests whether word-level replacement is sufficient for this normalization task.

### 3. GPT direct translation

This method uses a generic prompt asking GPT to translate informal written Cantonese into fluent Standard Written Chinese using Simplified Chinese characters.

It represents a simple LLM translation baseline without detailed task-specific linguistic guidance.

### 4. GPT basic standardization

This method explicitly frames the task as standardizing social-media-style written Cantonese into Standard Written Chinese.

The prompt mentions that the input may contain informal spellings, mixed Traditional/Simplified characters, English code-mixing, Cantonese colloquial expressions, slang, or nonstandard character choices.

### 5. GPT variation-aware standardization

This is the main LLM-based normalization method.

The prompt gives concrete examples of common online Cantonese variation, including informal spellings such as `有D` and `你地`, nonstandard character choices such as `左` for `咗`, English code-mixing such as `like` and `post`, Cantonese slang such as `收晒皮`, and sentence-final particles such as `架喎` and `wo`.

This method tests whether explicit linguistic guidance improves normalization quality.

### 6. GPT context-aware standardization

This method uses the same normalization goal but also provides the short context field from the dataset.

It tests whether topic context helps resolve ambiguous slang, tone, code-mixing, and context-dependent expressions.

## Code Structure

- `data/cantonese_examples.csv` contains the manually curated 70-example dataset collected from publicly visible online Cantonese comments.
- `src/dictionary_baseline.py` runs the direct replacement baseline.
- `src/run_llm.py` runs GPT-based methods using prompt templates.
- `src/evaluate.py` evaluates system outputs against the manual references.
- `prompts/` contains the GPT prompt templates.
- `results/` contains system outputs, automatic evaluation scores, and manual evaluation files.
- `docs/data_collection_notes.md` explains the dataset construction process.

The evaluation script converts both predictions and references to Simplified Chinese before scoring. This avoids penalizing outputs only because of Traditional/Simplified script differences.

## Evaluation

I use both automatic metrics and a small manual evaluation.

### Automatic evaluation

The following automatic metrics are reported for all six methods:

- **Exact match**: whether the output exactly matches the reference after normalization.
- **Character-level F1**: overlap between prediction and reference at the character level.
- **Edit similarity**: similarity based on sequence matching.

Before scoring, both predictions and references are converted to Simplified Chinese. This avoids penalizing outputs only because of Traditional/Simplified script differences.

These metrics are useful but limited. Exact match is very strict, while character-level metrics can reward surface overlap even when the output is unnatural or only partially standardized. Multiple Standard Written Chinese outputs can also be acceptable for the same Cantonese input. The manual references should therefore be interpreted as evaluation anchors rather than the only possible correct Standard Written Chinese outputs.

### Manual evaluation

Because automatic metrics can overestimate systems that preserve many input characters, I also conducted a small manual evaluation on 40 representative examples.

The 40 examples were sampled by variation type from the 70-example dataset. I evaluated three methods:

- Google Translate
- Direct replacement
- GPT variation-aware standardization

Each output was assigned one of three labels:

- **acceptable**: the meaning is preserved and the output is fluent Standard Written Chinese.
- **partial**: the general meaning is preserved, but the output contains Cantonese residue, unnatural wording, missing pragmatic tone, or incomplete normalization.
- **wrong**: the output has a clear meaning error, fails to standardize the sentence, or is not usable as Standard Written Chinese.

Traditional/Simplified script differences were ignored during manual evaluation.

## Results

The table below shows the automatic evaluation results on the 70-example dataset.

| Method | Exact Match | Char-F1 | Edit Similarity |
|---|---:|---:|---:|
| Google Translate | 0.0000 | 0.6472 | 0.6370 |
| Direct replacement | 0.0286 | 0.7411 | 0.7352 |
| GPT direct translation | 0.0286 | 0.7228 | 0.7046 |
| GPT basic standardization | 0.0429 | 0.7279 | 0.7136 |
| GPT variation-aware standardization | 0.0286 | 0.7355 | 0.7238 |
| GPT context-aware standardization | 0.0286 | 0.7284 | 0.7111 |

Google Translate performs the worst among the evaluated systems on this dataset. This supports the motivation that off-the-shelf MT systems are not reliable for social-media-style written Cantonese normalization.

Among the GPT-based methods, the variation-aware standardization prompt achieves the highest Char-F1 and edit similarity. This suggests that explicitly prompting the model with common online Cantonese variation can help.

The direct replacement baseline receives the highest automatic character-level scores overall. However, this should be interpreted cautiously. Direct replacement preserves many surface characters from the Cantonese input, which can increase character overlap even when the output is unnatural or only partially standardized.

Because multiple valid Standard Written Chinese normalizations are possible, small differences in automatic scores should be interpreted cautiously. For this reason, I also include a small manual evaluation below.

## Small Manual Evaluation

Because automatic character-level metrics can reward surface overlap, I also conducted a small manual evaluation on 40 representative examples. The examples were sampled by variation type from the 70-example dataset.

I compared three methods: Google Translate, direct replacement, and GPT variation-aware standardization. Each output was assigned one of three labels:

- `acceptable`: the meaning is preserved and the output is fluent Standard Written Chinese.
- `partial`: the general meaning is preserved, but the output contains Cantonese residue, unnatural wording, missing pragmatic tone, or incomplete normalization.
- `wrong`: the output has a clear meaning error, fails to standardize the sentence, or is not usable as Standard Written Chinese.

Traditional/Simplified script differences were ignored during manual evaluation.

| Method | Acceptable | Partial | Wrong | Acceptable Rate |
|---|---:|---:|---:|---:|
| Google Translate | 8 | 11 | 21 | 0.200 |
| Direct replacement | 8 | 16 | 16 | 0.200 |
| GPT variation-aware standardization | 17 | 15 | 8 | 0.425 |

The manual evaluation gives a different perspective from the automatic metrics. Although direct replacement receives the highest automatic character-level scores, only 20% of its sampled outputs were judged acceptable. This suggests that automatic metrics overestimate word-replacement methods because they preserve many surface characters from the input.

GPT variation-aware standardization has the highest manual acceptable rate, with 42.5% acceptable outputs. This supports the idea that task-specific LLM prompting can improve normalization quality compared with Google Translate and direct replacement, although many cases remain only partially correct or wrong.

## Qualitative Error Analysis

Automatic metrics only show part of the picture. Since written Cantonese and Standard Written Chinese share many surface characters, a system may receive a reasonable character-level score while still producing an unnatural or incomplete normalization. Therefore, I inspected representative outputs from the direct replacement baseline, Google Translate, and the GPT variation-aware prompt.

### 1. General MT often leaves Cantonese and code-mixing untranslated

Input:

> 兩位好識食，俾個like你哋

Reference:

> 你们两位真会吃，给你们点个赞。

Direct replacement:

> 兩位好識吃，被個赞你们

Google Translate:

> 兩位好識食，畀個like你地

GPT variation-aware:

> 两位很会吃，给你们一个赞。

Google Translate mostly preserves the Cantonese wording and the English code-mixed item `like`, so it does not really normalize the sentence into Standard Written Chinese. The direct replacement baseline changes some individual forms, but the result is unnatural. The GPT output is more fluent, although it slightly weakens the meaning of `識食`, which means being good at finding or appreciating good food.

### 2. Sentence-final particles and pragmatic tone are difficult

Input:

> 香港民意黎架wo

Reference:

> 这是香港民意来的啊。

Direct replacement:

> 香港民意黎架啊

Google Translate:

> hong kong public opinion

GPT variation-aware:

> 香港民意来了。

Google Translate fails to produce a Standard Chinese sentence. The direct replacement baseline only partially changes the final expression and still leaves an unnatural output. The GPT output is fluent Chinese, but it changes the meaning and loses the emphatic or reminding tone expressed by `wo/喎`. This shows that sentence-final particles are not just removable noise; they can carry pragmatic meaning.

### 3. Simple replacement rules are transparent but brittle

Input:

> 佢chok 到全歐洲最靚數據

Reference:

> 他刷出了全欧洲最好看的数据。

Direct replacement:

> 他ch还可以 到全欧洲最靚数据

Google Translate:

> 他chok到全欧洲最漂亮的数据

GPT variation-aware:

> 他获得了全欧洲最漂亮的数据。

This example shows a clear failure of direct string replacement. Because `ok` appears inside `chok`, the replacement baseline incorrectly changes part of the word and produces `ch还可以`. Google Translate keeps `chok` untranslated. The GPT output is fluent and closer to the intended meaning, but it still loses some of the informal sports-discussion tone of the original.

### 4. Cantonese lexical items can be misinterpreted

Input:

> 如果賣得貴過兩餸飯都唔會幫趁

Reference:

> 如果卖得比两餸饭还贵，我也不会光顾。

Direct replacement:

> 如果賣得貴過两餸饭都不会光顾

Google Translate:

> 如果賣得貴過兩餸飯都不會幫趁

GPT variation-aware:

> 如果卖得比两份饭还贵就不会帮忙了。

The direct replacement baseline handles `幫趁` relatively well because it is covered by the dictionary. Google Translate leaves several Cantonese forms untranslated. The GPT output is fluent, but it misinterprets `幫趁`, which means to patronize a shop or buy from a business, as `帮忙` “to help.” This changes the intended meaning.It also misinterprets `兩餸飯`, a common Hong Kong local food term, as ordinary “two portions of rice.” These errors change the intended meaning of the sentence.

### 5. Idiomatic expressions may be translated too literally

Input:

> 想早啲返屋企可以搬老婆出黎

Reference:

> 想早点回家的时候，可以把老婆拿出来当借口。

Direct replacement:

> 想早些回家可以搬老婆出来

Google Translate:

> 想早点回家可以把老婆搬出来

GPT variation-aware:

> 想早点回家可以把老婆搬出来。

Here, both Google Translate and GPT translate `搬老婆出嚟` too literally as physically moving or bringing out one’s wife. In context, the intended meaning is to use one’s wife as an excuse for leaving early. This example shows that even fluent outputs can be semantically wrong when the system misses an idiomatic or context-dependent use.

### 6. Hong Kong online slang remains challenging

Input:

> 最憎就係女仔收兵

Reference:

> 最讨厌的就是女生拿别人当备胎。

Direct replacement:

> 最憎就是女生拿别人当备胎

Google Translate:

> 最憎就是女仔收兵

GPT variation-aware:

> 最讨厌的就是女生收兵。

The slang expression `收兵` refers to keeping admirers or backup romantic options. Google Translate leaves the slang mostly untranslated, and GPT also preserves `收兵` instead of normalizing it into Standard Written Chinese. Interestingly, the direct replacement baseline performs better in this case because the expression is included in the replacement dictionary. This shows that simple lexical resources can help with known slang, but they are limited to expressions that are already covered.

### Summary

Overall, the qualitative analysis suggests that GPT-based prompting improves fluency compared with Google Translate and the direct replacement baseline in many cases. However, it still struggles with pragmatic particles, idiomatic expressions, local slang, and context-dependent meanings. The direct replacement baseline is useful for some known lexical items, but it is brittle and can fail badly when replacements are applied mechanically. These examples support the main finding that informal written Cantonese normalization is not only a word- or character-replacement problem.

## Discussion

The results show that social-media-style Cantonese normalization is not only a word replacement problem. The main difficulties come from informal orthography, English code-mixing, Cantonese slang, and pragmatic particles.

In practice, the boundary between normalization and translation is not always sharp: some inputs can be standardized through orthographic replacement, while others require interpreting slang, idioms, local cultural references, or pragmatic particles.

The automatic metrics and manual evaluation show different aspects of system behavior. Direct replacement receives the highest automatic character-level scores, but the manual evaluation shows that its outputs are often not acceptable as fluent Standard Written Chinese. This is because direct replacement preserves many input characters while failing to handle syntax, tone, context, and naturalness.

Google Translate performs the worst among the evaluated systems on this small dataset. This supports the motivation that at least one widely used off-the-shelf MT system is unreliable for fully normalizing social-media-style written Cantonese in this benchmark.

Among the GPT-based methods, the variation-aware standardization prompt achieves the highest Char-F1 and edit similarity, although the differences between GPT prompts are small. This suggests that explicitly prompting the model with common online Cantonese variation may help, but the automatic-score differences should not be overinterpreted.

However, the GPT variation-aware method does not solve the task completely. It still struggles with Cantonese slang, sarcastic tone, sentence-final particles, and cases where several Standard Chinese paraphrases are possible. This is why the manual acceptable rate is higher than the other systems but still below 50%.

Overall, the prototype shows that task-specific LLM prompting is a useful intervention for this bottleneck, but it should be evaluated with both automatic and manual methods. Automatic character-level metrics are useful for reproducibility, but they can overestimate outputs that preserve surface characters and underestimate fluent paraphrases.

## Limitations

This is a small prototype-level benchmark with 70 manually curated examples. It is not an unbiased or representative sample of all written Cantonese on social media. The examples were selected because they illustrate common normalization difficulties, so the results should be interpreted as evidence about specific bottlenecks rather than as a general estimate of real-world system performance.

The dataset is also limited in domain. Most examples come from publicly visible YouTube comments and Hong Kong online forum discussions. Other domains, such as private messaging, news comments, subtitles, or longer forum threads, may contain different writing styles and different normalization challenges.

The Standard Written Chinese references were written by one annotator. Since multiple valid normalizations are often possible, the references should be treated as evaluation anchors rather than unique ground truth. A larger project would ideally include multiple annotators and measure inter-annotator agreement.

The automatic metrics are limited. Exact match is very strict, while character-level F1 and edit similarity can reward surface overlap even when the output remains unnatural. This is why direct replacement receives high automatic scores despite low manual acceptability. The small manual evaluation helps address this issue, but it was still performed by one evaluator on a sample of 40 examples.

The rule-based baseline depends on a manually written replacement list. It can perform well when a phrase is already covered by the dictionary, but it does not generalize well to unseen slang, new spellings, or context-dependent expressions.

Finally, the GPT-based methods were tested using prompt engineering rather than model training. The results may vary with model version, decoding settings, and prompt wording. For stronger reproducibility, future versions should record the exact GPT model name, API date or model snapshot if available, temperature, decoding parameters, and the date on which Google Translate outputs were collected. This project should therefore be understood as a reproducible prototype rather than a production-ready Cantonese normalization system.

## Acknowledgment of AI Assistance

ChatGPT was used as an assistant for coding, debugging, prompt drafting, and README organization. I reviewed, adapted, ran, and interpreted the code and results myself. The dataset selection, Standard Written Chinese references, manual evaluation labels, and final analysis were curated and checked by me.

## How to Run

Install dependencies:

```bash
pip install pandas opencc-python-reimplemented openai
```

For GPT-based methods, set an OpenAI API key before running `src/run_llm.py`:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Run the direct replacement baseline

The direct replacement baseline is implemented in `src/dictionary_baseline.py`.

```bash
python src/dictionary_baseline.py
python src/evaluate.py
```

This generates:

```text
results/direct_replacement_outputs.csv
results/direct_replacement_scores.csv
results/direct_replacement_scores_summary.csv
```

### Run GPT-based methods

Run GPT direct translation:

```bash
python src/run_llm.py \
  --prompt prompts/direct_translate.txt \
  --method gpt_direct_translation \
  --output results/gpt_direct_translation_outputs.csv
```

Run GPT basic standardization:

```bash
python src/run_llm.py \
  --prompt prompts/basic_standardization.txt \
  --method gpt_basic_standardization \
  --output results/gpt_basic_standardization_outputs.csv
```

Run GPT variation-aware standardization:

```bash
python src/run_llm.py \
  --prompt prompts/variation_aware_standardization.txt \
  --method gpt_variation_aware_standardization \
  --output results/gpt_variation_aware_standardization_outputs.csv
```

Run GPT context-aware standardization:

```bash
python src/run_llm.py \
  --prompt prompts/context_aware_standardization.txt \
  --method gpt_context_aware_standardization \
  --output results/gpt_context_aware_standardization_outputs.csv
```

### Evaluate system outputs

All system outputs are evaluated with the same script, `src/evaluate.py`.

For example, to evaluate GPT variation-aware standardization:

```bash
python src/evaluate.py \
  --predictions results/gpt_variation_aware_standardization_outputs.csv \
  --output results/gpt_variation_aware_standardization_scores.csv
```

To evaluate GPT direct translation:

```bash
python src/evaluate.py \
  --predictions results/gpt_direct_translation_outputs.csv \
  --output results/gpt_direct_translation_scores.csv
```

To evaluate GPT basic standardization:

```bash
python src/evaluate.py \
  --predictions results/gpt_basic_standardization_outputs.csv \
  --output results/gpt_basic_standardization_scores.csv
```

To evaluate GPT context-aware standardization:

```bash
python src/evaluate.py \
  --predictions results/gpt_context_aware_standardization_outputs.csv \
  --output results/gpt_context_aware_standardization_scores.csv
```

### Evaluate Google Translate outputs

Google Translate outputs were collected manually from the web interface and saved in:

```text
results/google_translate_outputs.csv
```

They can be evaluated using the same evaluation script:

```bash
python src/evaluate.py \
  --predictions results/google_translate_outputs.csv \
  --output results/google_translate_scores.csv
```

### Manual evaluation

The manually labeled evaluation sample is saved in:

```text
results/manual_evaluation_sample.csv
```

The manual evaluation summary is saved in:

```text
results/manual_evaluation_summary.csv
```

To regenerate the manual evaluation summary from the labels:

```bash
python - << 'EOF'
import pandas as pd

df = pd.read_csv("results/manual_evaluation_sample.csv")
df["label"] = df["label"].astype(str).str.strip().str.lower()

counts = pd.crosstab(df["method"], df["label"])

for col in ["acceptable", "partial", "wrong"]:
    if col not in counts.columns:
        counts[col] = 0

counts = counts[["acceptable", "partial", "wrong"]]
counts["total"] = counts.sum(axis=1)
counts["acceptable_rate"] = counts["acceptable"] / counts["total"]

counts = counts.reset_index()
counts.to_csv("results/manual_evaluation_summary.csv", index=False, encoding="utf-8-sig")

print(counts.to_string(index=False))
EOF
```

### Reproduce all automatic summaries

After all output files have been generated, all automatic score summaries can be viewed with:

```bash
cat results/*summary.csv
```

## Main Takeaway

This project shows that social-media-style written Cantonese normalization is a real bottleneck for off-the-shelf MT systems. Google Translate often fails to fully standardize informal Cantonese comments, especially when they contain code-mixing, slang, nonstandard spellings, or sentence-final particles.

A simple direct replacement baseline can obtain high automatic character-level scores, but the manual evaluation shows that this does not necessarily mean the output is fluent or acceptable. This highlights the limitation of relying only on automatic string-based metrics.

The GPT variation-aware prompt performs best in the small manual evaluation and best among GPT methods in automatic evaluation. This suggests that task-specific LLM prompting is a useful prototype intervention, although it does not fully solve the problem.

Overall, this project provides a small reproducible benchmark and prototype pipeline for evaluating Cantonese-to-Standard-Chinese normalization in social-media contexts.
