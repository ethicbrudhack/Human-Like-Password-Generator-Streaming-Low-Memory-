🔤 Human-Like Password Generator (Streaming, Low Memory)

This Python script generates massive wordlists / password combinations based on given input words — efficiently and without loading everything into RAM.
It streams all generated variants directly to an output file, flushing memory regularly to stay fast and memory-safe.

⚙️ Features

✅ Streaming mode – doesn’t keep all results in memory
✅ Automatic file flushing every few thousand words
✅ Leet substitutions (a → 4/@, e → 3, i → 1, etc.)
✅ Capitalization and digit variants
✅ Prefix / suffix / month / year / common word expansions
✅ Customizable limits and flush frequency

📦 Required modules

You only need built-in modules and one external library (argparse, pathlib, and gc are included in Python).

Install dependencies with:

pip install gc-python-utils  # optional, if you want extended garbage collection (not required)


But for this script to work normally, you only need standard Python (no extra pip installs required).
If you want to be safe and match the environment used to test it:

pip install pathlib argparse


(Both are included by default in Python 3.7+.)

🐍 Run instructions

Make sure the file is executable:

chmod +x generate_human_like_stream.py


Then run it like this:

python3 generate_human_like_stream.py -i input.txt -o output.txt

💡 Example
Input (input.txt):
john
admin
welcome

Command:
python3 generate_human_like_stream.py -i input.txt -o passwords.txt --max-per-word 10000

Output (passwords.txt):
# base: john
john1
john_1
john.1
john-1
myjohn
realjohn
john123
John123
J0hn
j0hn2024
john-pass
...

🧩 Command-line options
Option	Description	Default
-i, --input	Input file with one base word per line	(required)
-o, --output	Output file where passwords will be written	(required)
--max-per-word	Max number of variants per base word	50000
--no-leet	Disable leet-style substitutions	False
--flush-every	How often to flush memory (every X words)	10000
🧠 How it works

For every word in your input file:

Generates multiple capitalization variants (john, John, JOHN).

Adds prefixes and suffixes (myjohn, john_123, real-john).

Inserts common words (john_pass, admin_john, welcome-john).

Adds months and years (john2024, marjohn, john_dec).

Optionally applies leet substitutions like a→4, o→0, etc.

Writes everything directly to the output file line by line.

Flushes memory and performs garbage collection every few thousand iterations.

🧰 Notes

Works great for generating realistic human-style password lists.

You can stop and resume any time (it writes progressively).

It’s designed to process millions of variants without using much RAM.

✅ Example of full command
python3 generate_human_like_stream.py \
  -i words.txt \
  -o all_passwords.txt \
  --max-per-word 30000 \
  --flush-every 5000

  BTC donation address:
bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
