# Data Collection Notes

This project focuses on social-media-style informal written Cantonese, especially orthographic and lexical variation that appears in online writing.

The dataset was collected from publicly visible online Cantonese comments, mainly from YouTube comments under Cantonese street-interview videos and discussions on Hong Kong online forums.

I selected short sentence-level examples that illustrate recurring patterns in social-media-style written Cantonese, such as informal orthography, code-mixing, Cantonese slang, and sentence-final particles. I did not include usernames, user IDs, profile information, timestamps, URLs, or full discussion threads in the released dataset.

To reduce privacy and copyright risks, the released dataset only contains short standalone sentences used for linguistic analysis and evaluation. The examples are not intended to redistribute complete user-generated posts or reconstruct the original discussion contexts. The context field is a brief author-written description of the topic, not a copy of the surrounding online discussion.

The dataset focuses on four broad types of variation:

## Informal orthography

Non-standard or inconsistent online spellings, such as `有D`, `有d`, `個d`, `你地`, `佢地`, `人地`, `左` for `咗`, `既` for `嘅`, `野` for `嘢`, and `出黎` for `出嚟`.

## Code-mixing

English words or online slang embedded in Cantonese sentences, such as `like`, `post`, `update`, `carry`, `chok`, `DAY 0`, `PLAN`, `Fun`, and `ok`.

## Colloquial or slang expressions

Cantonese colloquial vocabulary and Hong Kong-style expressions that do not map cleanly through word-for-word replacement, such as `拍拖`, `打機`, `幫趁`, `搭枱`, `收晒皮`, `正印`, `走得甩`, and `收兵`.

## Particles and context-dependent expressions

Cantonese sentence-final particles, tone markers, and pragmatic expressions such as `架啦`, `架喎`, `喎`, `囉`, `wo`, and `㗎啦`, as well as expressions whose meaning depends on discourse context.

Each example is assigned one primary variation type, although many examples contain overlapping features. The type label is used for error analysis rather than as a strict linguistic classification.

For each sentence, I manually wrote a Standard Written Chinese reference. Since multiple Standard Chinese normalizations may be valid, these references are used as evaluation anchors rather than unique ground truth.
