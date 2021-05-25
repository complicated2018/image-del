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
import re

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

os.chdir(r'D:\project\yozo-epweb-del')
print(os.getcwd())
os.makedirs(back_not_used_dir, 755, exist_ok=True)

for path in ignore_path:
    if (ignore_path.index(path) + 1) == len(ignore_path):
        ignore_path_str += '-path "' + path + '"'
    else:
        ignore_path_str += '-path "' + path + '" -o '

def do_find_command(search_dir, file_type):
    print('search_dir:%s' % search_dir)
    print('file_type:%s' % file_type)
    global ignore_path_str
    dict = {}
    if len(search_dir) == 0 or len(file_type) == 0:
        return dict
    search_dir = search_dir.replace('\n', '')
    command = "find '{}' \( {ignore} \) -prune -o -name '*.{other}'".format(search_dir, other=file_type, ignore=ignore_path_str)
    print('command:%s' % command)
    s = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    results = s.communicate()[0].split()
    index = 1
    for name in results:
        name = name.decode('utf-8')
        if not name.endswith(file_type):
            continue
        if name == '.png' or name == '.jpg' or name == '.jpeg' or name == '.gif' or name == '.svg' or name == '2.svg':
            continue
        dict[file_type + str(index)] = name
        index = index + 1
    return dict


def do_grep(path, key_word):
    key_word = key_word.replace('./', '')
    command = "grep -Rliw --include=\*.{html,css,scss,js} '%s' '%s'" % (key_word, path)
    if str(subprocess.getoutput(command)).find('No such') > -1:
        return True
    else:
        return False


def goal_file(path):
    files = []
    for dirName, subdirList, fileList in os.walk(path):
        for fname in fileList:
            if fname.find('-bundle') > 0 or fname.find('min.') > 0 or fname.find('dll.') > 0:
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
    print('\r\n ========%s is deleted========' % path)


def move_not_used_image(path):
    tmp = path.replace('./', '')
    print("tmp: %s" % tmp)
    try:
        out_dir = back_not_used_dir + '/' + tmp[: tmp.rindex('/')]
    except ValueError:
        out_dir = back_not_used_dir
    print("out_dir: %s" % out_dir)
    os.makedirs(out_dir, 755, exist_ok=True)
    shutil.move(path, out_dir)
    print('\r\n ========%s is moved========' % path)


def start_find_task():
    print("\nstart finding task...\nbelows are not used images:\n")
    global project_dir
    if len(sys.argv) > 1:
        project_dir = sys.argv[1]
    if project_dir == " ":
        print("error! project_dir can not be nil")
    print("\nproject_dir:")
    print(project_dir)
    start = time.time()
    i = 0
    results = {}
    for type_keyword in support_types():
        results = dict(results, **do_find_command(project_dir, type_keyword))
    # goal_files = {}
    # for type_path in is_available_file_path():
    #     goal_files = dict(goal_files, **do_find_command(project_dir, type_path))
    print("\nresults:")
    print(results)
    # print("\ngoal_files:")
    # print(goal_files.values())
    for result in results.values():
        if do_grep('./*', result):
            i = i + 1
            move_not_used_image(result)
    c = time.time() - start
    print('\nsearch finish,find %s results,total count %0.2f s' % (i, c))

start_find_task()
