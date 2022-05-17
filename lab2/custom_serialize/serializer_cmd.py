import argparse
from custom_serialize import serializer_service
parser_args = argparse.ArgumentParser()
parser_args.add_argument('file_path', type=str)
parser_args.add_argument('format', type=str)
parser_args.add_argument('-o', '--old_format', type=str, default=None)
parser_args.add_argument('-t', '--to_file', type=str, default=None)

args = parser_args.parse_args()

if args.old_format is None:
    point = args.file_path.rfind('.')
    if point == -1:
        raise ValueError('Unknown format file')
    else:
        args.old_format = args.file_path[point + 1:]

if args.to_file is None:
    args.to_file = args.file_path

obj = serializer_service.load(args.file_path, args.old_format)
serializer_service.dump(obj, args.format, args.file_path)
