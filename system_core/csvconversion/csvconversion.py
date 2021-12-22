import sys
import pandas
import csv


def get_headers(fullpath):
    headers = []
    duplicates = []
    with open(fullpath, encoding='utf-8-sig', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            headers = row
            break
    
    for header in headers:
        if headers.count(header) > 1:
            duplicates.append(header)
    
    duplicates_set = set(duplicates)

    return headers, duplicates_set


def get_content(fullpath):
    content = []
    with open(fullpath, encoding='utf-8-sig', newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            content.append(row)
        content.pop(0)

    return content


def csv_list_to_dicts(headers, content):
    rows = []
    for i in range(len(content)):
        row = {}
        for j in range(len(headers)):
            row[headers[j]] = content[i][j]
        rows.append(row)
    
    return rows
