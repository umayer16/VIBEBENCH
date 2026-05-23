from radon.complexity import cc_visit

files = [
    'core/analyzer.py',
    'core/executor.py',
    'core/reporter.py',
    'core/openai_generator.py',
    'core/gemini_generator.py',
    'core/groq_generator.py',
    'vibebench.py'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        code = fh.read()
    blocks = cc_visit(code)
    if blocks:
        avg = sum(b.complexity for b in blocks) / len(blocks)
        print(f'{f}: avg complexity = {avg:.2f}')
    else:
        print(f'{f}: no functions found')
