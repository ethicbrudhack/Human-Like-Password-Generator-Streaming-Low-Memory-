#!/usr/bin/env python3
# coding: utf-8
"""
generate_human_like_stream.py – wersja pamięciooszczędna (streamująca)
- nie trzyma wszystkich haseł w RAM
- zapisuje każdą partię od razu do pliku
- czyści pamięć co 10k słów
"""

from pathlib import Path
import argparse
import gc

# === KONFIGURACJA ===
PREFIXES = ["", "my", "the", "real", "official", "super", "vip", "best"]
SUFFIXES = ["", "1", "12", "123", "1234", "01", "007", "69", "777"]
SEPARATORS = ["", "_", ".", "-"]
COMMON_KEYWORDS = ["", "user", "admin", "pass", "password", "welcome", "letmein", "qwerty", "1q2w3e", "abc123"]
MONTHS_SHORT = ["", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
YEARS = [str(y) for y in range(1970, 2026)]

LEET_MAP = {
    'a': ['4', '@'],
    'o': ['0'],
    'i': ['1', '!'],
    'e': ['3'],
    's': ['5', '$'],
    't': ['7']
}

def simple_leet(word, max_variants=5):
    variants = {word}
    length = len(word)
    positions = []
    if length >= 1:
        positions.append(0)
    if length >= 3:
        positions.append(length//2)
    if length >= 2:
        positions.append(length-1)
    for pos in positions:
        c = word[pos].lower()
        if c in LEET_MAP:
            for r in LEET_MAP[c]:
                cand = word[:pos] + r + word[pos+1:]
                variants.add(cand)
        if len(variants) >= max_variants:
            break
    return list(variants)[:max_variants]

def capitalization_forms(base):
    b = base.strip()
    forms = []
    low = b.lower()
    cap = b.capitalize()
    up = b.upper()
    for f in (low, cap, up):
        if f and f not in forms:
            forms.append(f)
    return forms

def join_with_prefix(prefix, core):
    if not prefix:
        return [core]
    outs = [prefix + core]
    for sep in ("_", ".", "-"):
        outs.append(f"{prefix}{sep}{core}")
    return outs

def generate_digit_combinations(core):
    for i in range(10):
        n = str(i)
        yield core + n
        for sep in SEPARATORS[1:]:
            yield f"{core}{sep}{n}"
    for i in range(100):
        n = f"{i:02d}"
        yield core + n
        for sep in SEPARATORS[1:]:
            yield f"{core}{sep}{n}"
    for i in range(1000):
        n = f"{i:03d}"
        yield core + n
        for sep in SEPARATORS[1:]:
            yield f"{core}{sep}{n}"

def generate_for_base(base, max_per_word=50000, enable_leet=True):
    base = base.strip()
    if not base:
        return
    seen = set()
    forms = capitalization_forms(base)
    cores = []
    for f in forms:
        cores.append(f)
        if enable_leet and len(cores) < 8:
            for l in simple_leet(f, max_variants=3):
                if l not in cores:
                    cores.append(l)

    count = 0
    for core in cores:
        for variant in generate_digit_combinations(core):
            if variant not in seen:
                yield variant
                seen.add(variant)
                count += 1
                if count >= max_per_word:
                    return

        for suf in SUFFIXES:
            if not suf:
                continue
            for sep in SEPARATORS:
                variant = f"{core}{sep}{suf}".strip()
                if variant not in seen:
                    yield variant
                    seen.add(variant)
                    count += 1
                    if count >= max_per_word:
                        return

        for pre in PREFIXES:
            if not pre:
                continue
            for variant in join_with_prefix(pre, core):
                if variant not in seen:
                    yield variant
                    seen.add(variant)
                    count += 1
                    if count >= max_per_word:
                        return

        for kw in COMMON_KEYWORDS:
            if not kw:
                continue
            for sep in SEPARATORS:
                for variant in [
                    f"{core}{sep}{kw}",
                    f"{kw}{sep}{core}"
                ]:
                    if variant not in seen:
                        yield variant
                        seen.add(variant)
                        count += 1
                        if count >= max_per_word:
                            return

        for m in MONTHS_SHORT:
            if not m:
                continue
            for variant in [core + m, m + core]:
                if variant not in seen:
                    yield variant
                    seen.add(variant)
                    count += 1
                    if count >= max_per_word:
                        return

        for y in YEARS:
            for variant in [core + y, y + core]:
                if variant not in seen:
                    yield variant
                    seen.add(variant)
                    count += 1
                    if count >= max_per_word:
                        return

def stream_process(input_path, output_path, max_per_word=50000, enable_leet=True, flush_every=10000):
    input_file = Path(input_path)
    output_file = Path(output_path)

    with input_file.open('r', encoding='utf-8', errors='ignore') as fin, \
         output_file.open('w', encoding='utf-8') as fout:

        buffer_count = 0
        total_count = 0
        for idx, line in enumerate(fin, 1):
            base = line.strip()
            if not base:
                continue
            fout.write(f"# base: {base}\n")
            for variant in generate_for_base(base, max_per_word, enable_leet):
                fout.write(variant + "\n")
                buffer_count += 1
                total_count += 1

            fout.write("\n")

            if idx % flush_every == 0:
                fout.flush()
                gc.collect()
                print(f"✅ Przetworzono {idx} słów ({total_count:,} linii zapisanych)...")

        fout.flush()
        print(f"\nZakończono: {total_count:,} linii zapisano do {output_path}")

def main():
    ap = argparse.ArgumentParser(description="Generate huge password list (streaming mode, low RAM)")
    ap.add_argument('-i','--input', required=True, help='plik wejściowy ze słowami (po jednym na linię)')
    ap.add_argument('-o','--output', required=True, help='plik wyjściowy')
    ap.add_argument('--max-per-word', type=int, default=50000, help='limit wariantów na słowo')
    ap.add_argument('--no-leet', action='store_true', help='wyłącz leet substitutions')
    ap.add_argument('--flush-every', type=int, default=10000, help='czyszczenie pamięci co X słów')
    args = ap.parse_args()

    stream_process(args.input, args.output, max_per_word=args.max_per_word, enable_leet=not args.no_leet, flush_every=args.flush_every)

if __name__ == "__main__":
    main()
