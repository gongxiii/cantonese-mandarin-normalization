## Data Collection Notes

This project focuses on social-media-style informal written Cantonese, especially orthographic and lexical variation that appears in online writing.

Because the project is small-scale and educational, I did not scrape or redistribute full user-generated social media posts. Instead, I reviewed commonly observable patterns of informal written Cantonese in online spaces and Cantonese learning resources, then manually constructed short example sentences that reflect these recurring patterns.

The released dataset therefore consists of author-created examples rather than direct copies of user posts. This decision was made to avoid privacy and copyright issues while still grounding the benchmark in common online Cantonese usage.

The dataset focuses on four broad types of variation:

1. **Informal orthography**  
   Non-standard or inconsistent online spellings, such as `有D`, `有d`, `個d`, `你地`, `佢地`, `人地`, `左` for `咗`, `既` for `嘅`, `野` for `嘢`, and `出黎` for `出嚟`.

2. **Code-mixing**  
   English words or online slang embedded in Cantonese sentences, such as `like`, `post`, `update`, `carry`, `chok`, `DAY 0`, and `PLAN`.

3. **Colloquial or slang expressions**  
   Cantonese colloquial vocabulary and Hong Kong-style expressions that do not map cleanly through word-for-word replacement, such as `拍拖`, `打機`, `幫趁`, `搭枱`, `收晒皮`, `正印`, and `走得甩`.

4. **Particles and context-dependent expressions**  
   Cantonese sentence-final particles, tone markers, and pragmatic expressions such as `架啦`, `架喎`, `wo`, and expressions whose meaning depends on discourse context.

Each example is assigned one primary variation type, although many examples contain overlapping features. The type label is used for error analysis rather than as a strict linguistic classification.

For each sentence, I manually wrote a Standard Written Chinese reference. Since multiple Standard Chinese normalizations may be valid, these references are used as evaluation anchors rather than unique ground truth.
