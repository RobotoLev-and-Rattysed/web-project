import os
import os.path as path

lang_lines = {}
files_cnt = 0

for current_dir, dirs, files in os.walk(path.abspath(path.join(__file__, "../.."))):
    if any([name in current_dir for name in ['.\.git', '.\.idea']]):
        continue

    for file in files:
        lang = file.split('.')[-1]
        if lang in {'py', 'html', 'css'}:
            files_cnt += 1

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
print(f'Всего файлов кода: {files_cnt}')
print('=======')
