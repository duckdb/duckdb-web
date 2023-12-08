import os
import sys
import re

if len(sys.argv) < 2:
    print("Expected usage: python3 scripts/generate_docs.py /path/to/duckdb/folder")
    exit(1)

base_path = sys.argv[1]

# generate C API docs
duckdb_h_path = os.path.join(
    base_path, os.path.sep.join('src/include/duckdb.h'.split('/'))
)
with open(duckdb_h_path, 'r') as f:
    text = f.read()

docs_map = {
    'Open/Connect': 'docs/dev/api/c/connect.md',
    'Query Execution': 'docs/dev/api/c/query.md',
    'Configuration': 'docs/dev/api/c/config.md',
    'Result Functions': 'docs/dev/api/c/types.md',
    'Helpers': None,
    'Date/Time/Timestamp Helpers': 'docs/dev/api/c/types.md',
    'Hugeint Helpers': 'docs/dev/api/c/types.md',
    'Decimal Helpers': 'docs/dev/api/c/types.md',
    'Value Interface': 'docs/dev/api/c/value.md',
    'Logical Type Interface': 'docs/dev/api/c/types.md',
    'Data Chunk Interface': 'docs/dev/api/c/data_chunk.md',
    'Vector Interface': 'docs/dev/api/c/data_chunk.md',
    'Validity Mask Functions': 'docs/dev/api/c/data_chunk.md',
    'Table Functions': 'docs/dev/api/c/table_functions.md',
    'Table Function Bind': 'docs/dev/api/c/table_functions.md',
    'Table Function Init': 'docs/dev/api/c/table_functions.md',
    'Table Function': 'docs/dev/api/c/table_functions.md',
    'Replacement Scans': 'docs/dev/api/c/replacement_scans.md',
    'Prepared Statements': 'docs/dev/api/c/prepared.md',
    'Appender': 'docs/dev/api/c/appender.md',
    'Arrow Interface': None,
}
all_api_functions = 'docs/dev/api/c/api.md'


def is_line_separator(l):
    return l.strip().startswith('//===---')


lines = [x.strip() for x in text.split('\n')]
docs = []
code = []
current_group = None
in_header = False
in_docs = False
in_code = False

documentation_list = []


def format_function(function_text):
    function_spaces = '  '
    function_text = function_text.replace('(', '(\n' + function_spaces)
    function_text = function_text.replace(', ', ',\n' + function_spaces)
    function_text = function_text.replace(');', '\n);')
    return function_text


def extract_function_name(function_text):
    return function_text.split('(')[0].split(' ')[-1].lstrip('*')


def extract_parameters(docs_str):
    param_start_regex = '[*] *([a-zA-Z0-9_]+)[:](.*)'

    normal_docs = ''
    parameters = []
    in_parameter = False
    param_name = None
    param_docs = None
    for line in docs_str.split('\n'):
        param_match = re.match(param_start_regex, line)
        if param_match is not None:
            # parameter match: new parameter
            # push the old parameter (if any)
            if param_name is not None:
                parameters.append([param_name, param_docs])
            in_parameter = True
            param_name = param_match.groups()[0]
            param_docs = param_match.groups()[1].strip()
        elif not in_parameter:
            normal_docs += line + '\n'
        else:
            param_docs += '\n' + line
    # push the final parameter (if any)
    if param_name is not None:
        parameters.append((param_name, param_docs))
    return (normal_docs, parameters)


keyword_list = '''
bool
char
const
double
float
idx_t
int16_t
int32_t
int64_t
int8_t
size_t
uint16_t
uint32_t
uint64_t
uint8_t
void
'''

duckdb_type_list = '''
duckdb_appender
duckdb_arrow
duckdb_arrow_array
duckdb_arrow_schema
duckdb_bind_info
duckdb_blob
duckdb_config
duckdb_connection
duckdb_data_chunk
duckdb_database
duckdb_date
duckdb_date_struct
duckdb_function_info
duckdb_hugeint
duckdb_init_info
duckdb_interval
duckdb_logical_type
duckdb_prepared_statement
duckdb_replacement_scan_info
duckdb_result
duckdb_state
duckdb_table_function
duckdb_time
duckdb_time_struct
duckdb_timestamp
duckdb_timestamp_struct
duckdb_value
duckdb_vector
'''

keywords = [x.strip() for x in keyword_list.split('\n') if len(x.strip()) > 0]
duckdb_types = [x.strip() for x in duckdb_type_list.split('\n') if len(x.strip()) > 0]


def quick_docs_start():
    return '<div class="language-c highlighter-rouge"><div class="highlight"><pre class="highlight"><code>'


def quick_docs_end():
    return '</code></pre></div></div>\n'


def process_function_part(function_part, function_name):
    if function_part == function_name:
        return f'<a href="#{function_name}"><span class="nf">{function_part}</span></a>'
    if function_part in keywords:
        return f'<span class="kt">{function_part}</span>'
    if function_part in duckdb_types:
        return f'<span class="kt">{function_part}</span>'
    return f'<span class="nv">{function_part}</span>'


def highlight_function_prototype(function_prototype, function_name):
    split_regex = re.compile('([ \t(),;*]+)')
    last_pos = 0
    result = ''
    for match in split_regex.finditer(function_prototype):
        start = match.start()
        end = match.end()
        result += process_function_part(
            function_prototype[last_pos:start], function_name
        )
        result += function_prototype[start:end]
        last_pos = end
    if last_pos < len(function_prototype):
        result += process_function_part(
            function_prototype[last_pos:start], function_name
        )
    return result


def add_function(function_prototype, documentation, group):
    if len(documentation) == 0 or len(function_prototype) == 0:
        return
    function_prototype_str = ' '.join(
        [x.replace('DUCKDB_API', '').strip() for x in function_prototype]
    )
    function_name = extract_function_name(function_prototype_str)
    docs_str = '\n'.join(documentation) + '\n'
    (docs_str, parameters) = extract_parameters(docs_str)
    docs_string = '\n'
    docs_string += f'### `{function_name}`\n\n'
    docs_string += '---\n'
    docs_string += (
        docs_str.replace('e.g. ', 'e.g., ').replace('i.e. ', 'i.e., ').strip() + '\n'
        if docs_str
        else ''
    )
    docs_string += '\n#### Syntax\n\n'
    docs_string += '---\n'
    docs_string += quick_docs_start()
    docs_string += (
        highlight_function_prototype(format_function(function_prototype_str), None)
        + '\n'
    )
    docs_string += quick_docs_end()
    if len(parameters) > 0:
        docs_string += '\n#### Parameters\n\n'
        docs_string += '---\n'
        for parameter_pair in parameters:
            docs_string += "* `" + parameter_pair[0] + '`\n\n'
            docs_string += parameter_pair[1] + '\n'
    docs_string += '<br>\n'
    documentation_list.append(
        [
            docs_string,
            group,
            highlight_function_prototype(function_prototype_str, function_name),
        ]
    )


for line in lines:
    if in_header:
        if is_line_separator(line):
            in_header = False
        elif line.startswith("//"):
            current_group = line.replace('//', '').strip()
        else:
            in_header = False
    elif is_line_separator(line):
        in_header = True
    elif line == '/*!':
        docs = []
        in_docs = True
    elif line == '*/':
        in_docs = False
    elif in_docs:
        docs.append(line)
    elif in_code:
        code.append(line)
        if ';' in line:
            in_code = False
            add_function(code, docs, current_group)
            code = []
            docs = []
    else:
        if line.startswith('DUCKDB_API'):
            code = [line]
            if ';' not in line:
                in_code = True
            else:
                add_function(code, docs, current_group)
                code = []
                docs = []

group_docs = {}
for doc_pair in documentation_list:
    doc_text = doc_pair[0]
    group = doc_pair[1]
    prototype = doc_pair[2]
    if group not in group_docs:
        group_docs[group] = []
    group_docs[group].append([doc_text, prototype])


def replace_docs_in_file(file_name, group_name, docs_string_for_this_group):
    with open(file_name, 'r') as f:
        text = f.read()
    found = False
    api_ref_split = '## API Reference'
    if api_ref_split in text:
        text = (
            text.rsplit(api_ref_split, 1)[0]
            + api_ref_split
            + '\n\n<!-- This section is generated by scripts/generate_config_docs.py -->\n\n'
            + docs_string_for_this_group
        )
        found = True
    if not found:
        print(
            "API ref split not found in file " + file_name + " for group " + group_name
        )
        exit(1)
    with open(file_name, 'w+') as f:
        f.write(text)


file_docs = {}
for group_name in docs_map.keys():
    file_name = docs_map[group_name]
    print(group_name)
    print(file_name)
    if file_name is None:
        continue
    if group_name not in group_docs:
        print("No docs found for " + group_name)
        continue
    if file_name not in file_docs:
        quick_docs = quick_docs_start()
        docs_string_for_this_group = ""
    else:
        quick_docs = file_docs[file_name][0]
        docs_string_for_this_group = file_docs[file_name][1]
        quick_docs += '\n### ' + group_name + '\n\n'
        quick_docs += quick_docs_start()
    for entry in group_docs[group_name]:
        quick_docs += entry[1] + '\n'
        docs_string_for_this_group += entry[0] + '\n'
    quick_docs += quick_docs_end()
    file_docs[file_name] = [quick_docs, docs_string_for_this_group]

for file_name in file_docs.keys():
    quick_docs = file_docs[file_name][0]
    docs_string_for_this_group = file_docs[file_name][1]

    replace_docs_in_file(file_name, group_name, quick_docs + docs_string_for_this_group)

current_group_name = None
total_quick_docs = ''
total_docs = ""
for entry in documentation_list:
    group_name = entry[1]
    if group_name is not current_group_name:
        if current_group_name is not None:
            total_quick_docs += quick_docs_end() + '\n'
        total_quick_docs += '### `' + group_name + '`\n\n'

        total_quick_docs += quick_docs_start()
        current_group_name = group_name
    total_quick_docs += entry[2] + '\n'
    total_docs += entry[0] + '\n'
total_quick_docs += quick_docs_end()

replace_docs_in_file(
    all_api_functions, 'All API Functions', total_quick_docs + total_docs
)
