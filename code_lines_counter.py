import os

lang_lines = {}

for current_dir, dirs, files in os.walk('.'):
    if any([name in current_dir for name in ['.\.git', '.\.idea']]):
        continue

    for file in files:
        if file == 'code_lines_counter.py':
            continue

        lang = file.split('.')[-1]
        if lang in {'py', 'html', 'css'}:
            with open(current_dir + '/' + file, 'r', encoding='utf8') as f:
                lines_now = len(f.readlines())

            if lang not in lang_lines:
                lang_lines[lang] = 0
            lang_lines[lang] += lines_now

print('=======')
print(f'Количество строк кода в проекте: {sum(lang_lines.values())}')
print('=======')
for lang, lines in sorted(list(lang_lines.items()), key=lambda x: (-x[1], x[0])):
    print(f'{lang}: {lines} строк')
print('=======')
