# Cantonese-to-Standard-Chinese Normalization

This project builds a small prototype for normalizing social-media-style written Cantonese into Standard Written Chinese. The focus is on orthographic and lexical variation in online Cantonese, including informal spellings, English code-mixing, nonstandard character choices, Cantonese slang, and sentence-final particles.

## Project Goal

Informal written Cantonese on social media is often difficult for automatic translation systems because the writing is not standardized. The same expression may appear in different forms, such as 有D, 有d, 個d, 你地, 佢地, 左, 既, like, post, or chok.

This project asks: how well do different automatic methods standardize social-media-style written Cantonese into Standard Written Chinese?

The goal is not to build a full Cantonese machine translation system. Instead, this is a small prototype and evaluation benchmark for one specific bottleneck: online Cantonese orthographic and lexical variation.

## Data

The dataset contains 50 manually curated short examples of social-media-style written Cantonese.

Each example includes a Cantonese input sentence, a short context description, a manually written Standard Written Chinese reference, a primary variation type, and notes explaining the relevant Cantonese forms.

The four broad variation types are:

| Type | Description | Examples |
|---|---|---|
| informal_orthography | Non-standard or inconsistent online spellings | 有D, 你地, 佢地, 左, 既, 野 |
| code_mixing | English words or online slang inside Cantonese | like, post, update, carry, chok |
| colloquial_or_slang | Cantonese colloquial or Hong Kong-style expressions | 拍拖, 打機, 幫趁, 搭枱, 收晒皮 |
| particles_and_context | Sentence-final particles or context-dependent tone | 架啦, 架喎, wo, 嘅 |

Each example is assigned one primary variation type, although many examples contain overlapping features. The type label is used for error analysis rather than as a strict linguistic classification.

For more details, see [`docs/data_collection_notes.md`](docs/data_collection_notes.md).

## Data Collection Notes

Because this project is small-scale and educational, I did not scrape or redistribute full user-generated social media posts. Instead, I reviewed commonly observable patterns of informal written Cantonese in online spaces and Cantonese learning resources, then manually constructed short example sentences that reflect these recurring patterns.

The released dataset therefore consists of author-created examples rather than direct copies of user posts. This avoids privacy and copyright issues while still grounding the benchmark in common online Cantonese usage.

For each sentence, I manually wrote a Standard Written Chinese reference. Since multiple valid Standard Chinese normalizations may be possible, these references are used as evaluation anchors rather than unique ground truth.

## Methods

I compare six methods:

1. Direct replacement baseline  
   A simple dictionary-based replacement system.

2. Google Translate  
   Outputs collected manually from the Google Translate web interface. Outputs were copied without semantic correction. Only formatting issues such as line breaks were cleaned before evaluation.

3. GPT direct translation  
   A generic Cantonese-to-Standard-Chinese translation prompt.

4. GPT basic standardization  
   A prompt that explicitly asks for social-media Cantonese standardization.

5. GPT variation-aware standardization  
   A prompt that gives examples of common online Cantonese variation, such as informal spellings, code-mixing, nonstandard characters, slang, and particles.

6. GPT context-aware standardization  
   A prompt that uses the short context field to resolve ambiguous or context-dependent expressions.

## Code Structure

- data/cantonese_examples.csv contains the manually curated dataset.
- src/dictionary_baseline.py runs the direct replacement baseline.
- src/run_llm.py runs GPT-based methods using prompt templates.
- src/evaluate.py evaluates system outputs against the manual references.
- prompts/ contains the GPT prompt templates.
- results/ contains system outputs and evaluation scores.
- docs/data_collection_notes.md explains the dataset construction process.

The evaluation script converts both predictions and references to Simplified Chinese before scoring. This avoids penalizing outputs only because of Traditional/Simplified script differences.

## Evaluation

The following automatic metrics are reported:

- Exact match: whether the output exactly matches the reference after normalization.
- Character-level F1: overlap between prediction and reference at the character level.
- Edit similarity: similarity based on sequence matching.

These metrics are useful but limited. Multiple Standard Written Chinese outputs can be acceptable, so qualitative error analysis is also necessary.

## Results

| Method | Exact Match | Char-F1 | Edit Similarity |
|---|---:|---:|---:|
| Google Translate | 0.00 | 0.6465 | 0.6249 |
| Direct replacement | 0.02 | 0.7195 | 0.7087 |
| GPT direct translation | 0.04 | 0.7351 | 0.7034 |
| GPT basic standardization | 0.04 | 0.7275 | 0.6976 |
| GPT variation-aware standardization | 0.02 | 0.7372 | 0.7076 |
| GPT context-aware standardization | 0.02 | 0.7179 | 0.6860 |

GPT-based methods generally outperform Google Translate on this dataset. The variation-aware standardization prompt achieves the highest Char-F1, although the difference among GPT prompts is small.

Direct replacement receives a relatively high character-level score because it preserves many surface characters from the input. However, qualitative inspection shows that its outputs are often unnatural or only partially standardized.

Because multiple valid Standard Chinese normalizations are possible, small differences in automatic scores should be interpreted cautiously.

## Qualitative Error Analysis

### Google Translate often leaves Cantonese unnormalized

Input: 兩位好識食，俾個like你哋

Reference: 你们两位真会找好吃的东西，给你们点个赞

Google Translate: 兩位好識食，畀個like你地

Google Translate mostly preserved the Cantonese and code-mixed expression instead of producing Standard Written Chinese. It changed some characters but did not normalize 識食, like, or 你哋.

### Google Translate may fail on informal particles

Input: 香港民意黎架wo

Reference: 这是香港民意啊

Google Translate: hong kong public opinion

This output loses the Cantonese sentence-final tone and does not produce a Chinese standardized sentence.

### Direct replacement captures local words but not sentence meaning

Input: 有D人好簡單好理所當然咁就拍到拖

Reference: 有些人很轻松、很理所当然地就谈上恋爱了

Direct replacement: 有些人好簡單好理所當然这么就拍到拖

The baseline maps some local forms, such as 有D and 咁, but leaves much of the Cantonese structure and vocabulary unchanged. The output is not fluent Standard Written Chinese.

### Slang remains difficult

Input: 大陸經濟股市收晒皮

Reference: 大陆经济和股市都彻底不行了

GPT direct translation: 大陆经济股市大幅下跌。

GPT variation-aware standardization: 大陆经济股市已经崩溃。

The Cantonese slang expression 收晒皮 means that something has completely failed or collapsed. GPT direct translation weakens the meaning, while the variation-aware prompt gives a closer but still not identical paraphrase.

### Pragmatic tone is often weakened

Input: 又話香港復甦好好景嘅

Reference: 不是说香港复苏得很好、很景气吗？

GPT direct translation: 又说香港复苏的景象很好。

GPT variation-aware standardization: 又说香港复苏的前景很好。

The GPT outputs preserve the general topic but lose the questioning or skeptical tone of 又話...嘅.

## Discussion

The results suggest that social-media-style Cantonese normalization is not only a word replacement problem. Orthographic variation, English code-mixing, Cantonese slang, and pragmatic particles all affect the quality of Standard Written Chinese outputs.

The variation-aware GPT prompt gives the best character-level score, but the improvement over other GPT prompts is small. This suggests that GPT already handles many common Cantonese forms, but still struggles with slang, particles, and context-dependent meanings.

The context-aware prompt did not improve automatic scores. One possible reason is that the context descriptions are short and sometimes lead the model to produce freer paraphrases, which may be reasonable but less similar to the reference string.

## Limitations

This is a small prototype-level benchmark with 50 manually curated examples. It is not an unbiased sample of all written Cantonese on social media. The examples were selected to cover recurring variation patterns and known normalization difficulties.

The automatic metrics are also limited. Exact match is very strict, while character-level metrics can reward surface overlap even when the output is unnatural. For this reason, qualitative error analysis is necessary.

## How to Run

Install dependencies:

```bash
pip install pandas opencc-python-reimplemented openai
```

For GPT-based methods, set an OpenAI API key before running `src/run_llm.py`:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Run the direct replacement baseline:

```bash
python src/dictionary_baseline.py
python src/evaluate.py
```

Run a GPT-based method:

```bash
python src/run_llm.py \
  --prompt prompts/direct_translate.txt \
  --method gpt_direct_translation \
  --output results/gpt_direct_translation_outputs.csv
```

Other GPT prompt files can be run by replacing `prompts/direct_translate.txt` with the corresponding file in `prompts/`.

For example:

```bash
python src/run_llm.py \
  --prompt prompts/variation_aware_standardization.txt \
  --method gpt_variation_aware_standardization \
  --output results/gpt_variation_aware_standardization_outputs.csv
```

Evaluate a method:

```bash
python src/evaluate.py \
  --predictions results/gpt_direct_translation_outputs.csv \
  --output results/gpt_direct_translation_scores.csv
```

Evaluate Google Translate outputs:

```bash
python src/evaluate.py \
  --predictions results/google_translate_outputs.csv \
  --output results/google_translate_scores.csv
```

## Main Takeaway

This project does not claim to solve Cantonese normalization completely. Instead, it provides a small reproducible prototype and evaluation showing that informal written Cantonese standardization requires more than word-for-word replacement, and that current automatic systems still struggle with slang, code-mixing, particles, and context-dependent meaning.
