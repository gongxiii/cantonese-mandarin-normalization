import argparse
from pathlib import Path
import pandas as pd


REPLACEMENTS = [
    # Longer phrases first
    ("有D", "有些"),
    ("有d", "有些"),
    ("個d", "那些"),
    ("嗰啲", "那些"),
    ("你地", "你们"),
    ("佢地", "他们"),
    ("人地", "别人"),

    ("DAY 0", "第0天"),
    ("PLAN", "计划"),
    ("update", "更新"),
    ("post", "帖子"),
    ("like", "赞"),
    ("carry", "撑着"),
    ("chok口音", "刻意口音"),
    ("chok", "刷"),

    ("阿仙奴", "阿森纳"),
    ("曼聯", "曼联"),

    ("拍拖", "谈恋爱"),
    ("打機", "打游戏"),
    ("幫趁", "光顾"),
    ("搭枱", "拼桌"),
    ("收晒皮", "彻底不行了"),
    ("走得甩", "脱身"),
    ("正印", "正牌伴侣"),
    ("兩餸飯", "两餸饭"),
    ("銀包", "钱包"),
    ("家用", "生活费"),
    ("公屋", "公屋"),
    ("開演唱會", "开演唱会"),

    ("話時話", "说起来"),
    ("有得", "可以"),
    ("白食白住", "白吃白住"),
    ("大把人", "很多人"),
    ("得你一個", "只有你一个"),
    ("日日", "天天"),
    ("唔好彩", "不走运"),
    ("唔切", "来不及"),
    ("冇點", "没怎么"),
    ("冇咁易", "没那么容易"),
    ("唔會", "不会"),
    ("唔到", "不到"),
    ("唔貴", "不贵"),
    ("唔得", "不可以"),
    ("唔", "不"),
    ("冇", "没有"),
    ("無咗", "没有了"),
    ("無咩", "没什么"),

    ("係咪", "是不是"),
    ("定係", "还是"),
    ("都係", "也是"),
    ("實係", "一定是"),
    ("係", "是"),

    ("左", "了"),
    ("咗", "了"),
    ("既", "的"),
    ("嘅", "的"),
    ("野", "东西"),
    ("嘢", "东西"),
    ("比", "被"),
    ("畀", "被"),
    ("出黎", "出来"),
    ("出嚟", "出来"),
    ("宜家", "现在"),
    ("而家", "现在"),
    ("黎架wo", "啊"),
    ("架喎", "啊"),
    ("架啦", "的啦"),
    ("囉", "了"),

    ("啲", "些"),
    ("咁", "这么"),
    ("佢", "他"),
    ("睇", "看"),
    ("講", "说"),
    ("諗", "想"),
    ("攞", "拿"),
    ("拎", "拿"),
    ("返屋企", "回家"),
    ("屋企", "家里"),
    ("放工", "下班"),
    ("攰", "累"),
    ("搵", "找"),
    ("飛", "票"),
    ("食", "吃"),
]


def direct_replace(text: str) -> str:
    output = str(text)
    for src, tgt in REPLACEMENTS:
        output = output.replace(src, tgt)
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/cantonese_examples.csv")
    parser.add_argument("--output", default="results/direct_replacement_outputs.csv")
    parser.add_argument("--method", default="direct_replacement")
    args = parser.parse_args()

    df = pd.read_csv(args.input)

    rows = []
    for _, row in df.iterrows():
        rows.append({
            "id": row["id"],
            "method": args.method,
            "prediction": direct_replace(row["cantonese"])
        })

    out = pd.DataFrame(rows)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    out.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Wrote {len(out)} predictions to {output_path}")


if __name__ == "__main__":
    main()