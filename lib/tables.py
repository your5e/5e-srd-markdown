import re
from tabulate import tabulate


def split_row(line):
    # don't split on escaped pipes '\|'
    parts = re.split(r'(?<!\\)\|', line)
    return parts


def realign_table(lines, index):
    if not lines[index].startswith('|'):    # not a table
        return None
    if index > 1 and lines[index-1] != '':  # not start of table
        return None
    if not all(                             # doesn't look like a table
        re.match(r'^:?-+:?$', cell.strip())
            for cell in split_row(lines[index+1])[1:-1]
    ):
        return None

    headers = [
        re.sub(r' +', ' ', cell.strip())
            for cell in split_row(lines[index])[1:-1]
    ]
    table_end = index

    while True:
        # find the end of the table
        while table_end < len(lines) - 1 and lines[table_end + 1].startswith('|'):
            table_end += 1

        # look for the same table to continue after a page break
        if table_end+3 < len(lines) and lines[table_end+3].startswith('|'):
            cells = [cell for cell in split_row(lines[table_end+3])[1:-1]]
            if len(cells) != len(headers):
                break
            if all('--' in cell for cell in cells):
                break
            table_end += 3
        else:
            break

    rows = []
    for line in lines[index+2:table_end+1]:
        cells = [
            re.sub(r' +', ' ', cell.strip())
                for cell in split_row(line)[1:-1]
        ]
        # ensure number of cells matches headers
        cells = (cells + [''] * len(headers))[:len(headers)]
        if any(cell for cell in cells):
            rows.append(cells)

    # remove columns where every cell is empty
    remove = []
    for column in range(len(headers)):
        if not headers[column] and all(not row[column] for row in rows):
            remove.append(column)
    for column in reversed(remove):
        del headers[column]
        for row in rows:
            del row[column]

    if not headers and not rows:
        end = table_end + 1
        if end < len(lines) and lines[end] == '':
            end += 1
        del lines[index:end]
        return -(end - index)

    aligned = tabulate(rows, headers=headers, tablefmt='github').split('\n')
    for i, new_line in enumerate(aligned):
        lines[index + i] = new_line

    difference = len(aligned) - (table_end - index + 1)
    if difference < 0:
        del lines[index + len(aligned):index + len(aligned) - difference]
    return difference
