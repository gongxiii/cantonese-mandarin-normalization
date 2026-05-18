# Data Collection Notes

This project focuses on social-media-style informal written Cantonese.

Because the project is small-scale and educational, I did not scrape or redistribute full user-generated social media posts. Instead, I reviewed commonly observable patterns of informal written Cantonese in online spaces and Cantonese learning resources, then manually constructed short example sentences that reflect these recurring patterns.

The released dataset therefore consists of author-created examples rather than direct copies of user posts. This decision was made to avoid privacy and copyright issues while still grounding the benchmark in common online Cantonese usage.

The dataset focuses on five recurring phenomena:

1. Negation markers: 唔, 冇, 唔係, 唔使
2. Aspect markers: 咗, 緊, 過
3. Sentence-final particles: 啦, 喎, 咩, 啫, 掛
4. Colloquial vocabulary: 食, 睇, 攰, 靚, 返工, 癲
5. Pragmatic expressions: 唔該, 冇所謂, 得閒, 飲茶

For each sentence, I manually wrote a Standard Written Chinese reference. Since multiple Standard Chinese normalizations may be valid, these references are used as evaluation anchors rather than unique ground truth.
