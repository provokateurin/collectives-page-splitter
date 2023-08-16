#!/usr/bin/env python

import sys
import subprocess
import os
import re
import urllib.parse
import shutil

if len(sys.argv) < 2 or len(sys.argv) > 3:
    raise Exception("Need markdown page and optional attachments folder")

markdown_source_file = os.path.abspath(sys.argv[1])
if len(sys.argv) >= 3:
    attachments_source_dir = os.path.abspath(sys.argv[2])
else:
    attachments_source_dir = None

source_dir = os.path.dirname(markdown_source_file)
assert attachments_source_dir is None or os.path.dirname(attachments_source_dir) == source_dir, \
    "Attachments source needs to be in the same folder as the Markdown source"

subprocess.run([
    "csplit",
    "--elide-empty-files",
    "--silent",
    markdown_source_file,
    "/^# /",
    "{*}",
], cwd=source_dir)

file_pattern = re.compile("^xx[0-9]{2}$")
heading_pattern = re.compile("^#+ ")
if attachments_source_dir is not None:
    attachments_pattern = re.compile("\\(" + os.path.basename(attachments_source_dir) + "/([^)]+)\\)")
else:
    attachments_pattern = None


def drop_heading_level(heading: str):
    if heading_pattern.match(heading):
        return heading[1:]
    return heading


for file in os.listdir(source_dir):
    if not file_pattern.match(file):
        continue

    split_source_file = os.path.join(source_dir, file)

    with open(split_source_file) as f:
        lines = [line for line in f]

    # First line is the heading
    title = lines[0][2:-1]

    # Remove the heading
    lines = lines[2:]

    # Drop all heading levels so that they all make sense
    lines = list(map(drop_heading_level, lines))

    target_dir = os.path.join(source_dir, title)
    os.mkdir(target_dir)

    markdown_target_file = os.path.join(target_dir, "Readme.md")
    with open(markdown_target_file, "w") as f:
        f.writelines(lines)

    if attachments_source_dir is not None:
        attachments_target_dir = os.path.join(target_dir, os.path.basename(attachments_source_dir))
        os.mkdir(attachments_target_dir)

        for line in lines:
            match = re.search(attachments_pattern, line)
            if match:
                name = urllib.parse.unquote(match.group(1))
                shutil.copy2(os.path.join(attachments_source_dir, name), os.path.join(attachments_target_dir, name))

    os.unlink(split_source_file)

with open(markdown_source_file, "w") as f:
    f.write("")
shutil.rmtree(attachments_source_dir)
