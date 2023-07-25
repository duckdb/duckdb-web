import json
from pathlib import Path
from argparse import ArgumentParser
from subprocess import check_output, CalledProcessError, PIPE

parser = ArgumentParser()
parser.add_argument('--source', required=True)
parser.add_argument('--binary', required=True)
args = parser.parse_args()


def get_result(example: str) -> str:
    if example == 'current_date()':
        return '2023-07-23'
    elif example == 'get_current_time()':
        return '14:04:22.524'
    elif example == 'get_current_timestamp()':
        return '2023-07-23 14:04:22.538+00'

    try:
        out = check_output(
            [
                args.binary,
                '-json',
                '-c',
                'SELECT setseed(0.42); ',
                '-c',
                'LOAD icu;',
                '-c',
                f'SELECT {example.strip(";")} AS result'
            ],
            stderr=PIPE
        )
        rows = json.loads(out.splitlines()[-1])
        return rows[0]['result']
    except CalledProcessError as e:
        print(example.strip(), e.stderr.decode())
        return None


def main():
    functions = []
    source = Path(args.source)
    assert source.exists()
    for file in source.glob('src/core_functions/**/*.json'):
        category = file.parent.stem
        with file.open() as fh:
            functions += [
                {
                    **function,
                    'parameters': (
                        function['parameters'].split(',')
                        if function.get('parameters')
                        else
                        []
                    ),
                    'category': category,
                    'result': get_result(function['example']) if function.get('example') else None
                }
                for function in json.load(fh)
            ]

    functions = sorted(functions, key=lambda fn: fn['name'])

    with open('docs/functions.json', 'w') as fh:
        json.dump(
            functions,
            fh,
            indent=2
        )

if __name__ == '__main__':
    main()
