# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# -*- coding: utf-8 -*-
import io
import os
import sys
import subprocess
import shutil
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

exclude_AssetImage1 = 'images'
exclude_AssetImage2 = 'img'
project_dir = "."
back_not_used_dir = "./no_used"
auto_delete = 0
auto_move = 1
ignore_path = [
    './.git',
    './.idea',
    './node_modules',
    './configs_web',
    './applet',
    './android',
    './activity',
    './b',
    './background',
    './dist',
    './dist_bak',
    './email-tmpl',
    './local-strings',
    './office',
    './outerJs',
    './p',
    './p1',
    './public',
    './separate',
    './share',
    './javascript/plugins',
    './javascript/tasks',
    './javascript/wx',
    './javascript/vendor',
    './no_used',
]
ignore_path_str = ''

f = open('output1.txt', 'w')
os.chdir(r'D:\project\yozo-epweb-del')
print(os.getcwd(), file=f)
os.makedirs(back_not_used_dir, 755, exist_ok=True)

for path in ignore_path:
    if (ignore_path.index(path) + 1) == len(ignore_path):
        ignore_path_str += '-path "' + path + '"'
    else:
        ignore_path_str += '-path "' + path + '" -o '

def do_find_command(search_dir, file_type):
    print('\n search_dir:%s' % search_dir, file=f)
    print('\n file_type:%s' % file_type, file=f)
    global ignore_path_str
    dict = {}
    if len(search_dir) == 0 or len(file_type) == 0:
        return dict
    search_dir = search_dir.replace('\n', '')
    command = "find '{}' \( {ignore} \) -prune -o -name '*.{other}'".format(search_dir, other=file_type, ignore=ignore_path_str)
    print('\n do_find_command:%s' % command, file=f)
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    results = s.communicate()[0].split()
    index = 1
    for name in results:
        name = name.decode('utf-8')
        if not name.endswith(file_type):
            continue
        if name == '.png' or \
           name == '.jpg' or \
           name == '.jpeg' or \
           name == '.gif' or \
           name == '.svg' or \
           name == '2.svg':
            continue
        dict[file_type + str(index)] = name
        index = index + 1
    return dict


def do_grep(path, key_word):
    key_word = key_word[key_word.rindex('/') + 1:]
    print("\n key_word: %s" % key_word, file=f)
    command = "grep -Rliw --include=\*.{html,scss,js} --exclude=\*{-bundle.js,-mini.js,js.map} '%s' '%s'" % (key_word, path)
    print("\n do_grep: %s" % command, file=f)
    if subprocess.getoutput(command):
        return False
    else:
        return True


def goal_file(path):
    files = []
    for dirName, subdirList, fileList in os.walk(path):
        for fname in fileList:
            if fname.find('-bundle') > -1 or fname.find('min.') > -1 or fname.find('dll.') > -1:
                continue
            files.append(path)
    return files


def is_available_file_path():
    types = []
    types.append('css')
    types.append('scss')
    types.append('js')
    types.append('html')
    return types


def support_types():
    types = []
    types.append('png')
    types.append('jpg')
    types.append('jpeg')
    types.append('gif')
    types.append('svg')
    return types


def delete_not_used_image(path):
    os.remove(path)
    print('\n ========%s is deleted========' % path, file=f)


def move_not_used_image(path):
    tmp = path.replace('./', '')
    print("\n tmp: %s" % tmp, file=f)
    try:
        out_dir = back_not_used_dir + '/' + tmp[: tmp.rindex('/')]
    except ValueError:
        out_dir = back_not_used_dir
    print("\n out_dir: %s" % out_dir, file=f)
    os.makedirs(out_dir, 755, exist_ok=True)
    shutil.move(path, out_dir)
    print('\n ========%s is moved========' % path, file=f)


def start_find_task():
    print("\n start finding task...\nbelows are not used images:\n", file=f)
    global project_dir
    if len(sys.argv) > 1:
        project_dir = sys.argv[1]
    if project_dir == " ":
        print("\n error! project_dir can not be nil", file=f)
    start = time.time()
    i = 0
    results = {}
    for type_keyword in support_types():
        results = dict(results, **do_find_command(project_dir, type_keyword))
    print("\n results: %s" % results.values(), file=f)
    for result in results.values():
        if do_grep('.', result):
            i = i + 1
            move_not_used_image(result)
    c = time.time() - start
    print('\n search finish,find %s results,total count %0.2f s' % (i, c), file=f)

start_find_task()

f.close()
