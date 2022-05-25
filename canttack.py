import os
import argparse
import textwrap

from module.parser import dataset_group_parser, inject_group_parser, info_group_parser
from module.AttackBuilder import AttackBuilder
from module.utils import create_can_normal_dataset
from argparse import RawDescriptionHelpFormatter


def dataset(args):
    is_can, is_can_fd = args.can, args.can_fd
    dest, target = args.name, args.target
    f = None

    try:
        f = open(f'{target}.txt')
    except FileNotFoundError:
        exit(f'{target}.csv file is Not Found! please check file in current directory {os.getcwd()}')

    if is_can:
        create_can_normal_dataset(f, dest)
    elif is_can_fd:
        create_can_normal_dataset(f, dest)


def inject(args):
    is_ddos, is_fuzzing = args.ddos, args.fuzzing
    count, target = args.count, args.target

    builder = AttackBuilder(target)

    if is_ddos:
        builder.set_attack_type('ddos')
    elif is_fuzzing:
        builder.set_attack_type('fuzzing')

    for i in range(0, count):
        builder.inject_attack()

    builder.build()


# def info(args):
#     print('asdfadsf')
#     print('qweqwe')


def parser_setting():
    parser = argparse.ArgumentParser(description = textwrap.dedent('''\
        canttack is a tool for creating {can|can fd} normal dataset and injecting attack into dataset.\n
        DDoS : The injected attack has a interval of 0.000001 and about 100 pieces of data are injected.
        Fuzzing :The injected attack has a interval of 0.0000001 and about 10 pieces of data are injected.
        '''), prog = 'canttack', formatter_class = RawDescriptionHelpFormatter)
    parser.add_argument('-V', '--version', action = 'version', version = 'canttack 1.0.0',
                        help = 'show this program version')
    parser.set_defaults(func = None)

    subparsers = parser.add_subparsers(metavar = 'command')
    dataset_parser = subparsers.add_parser('dataset',
                                           help = 'Create an normal dataset')
    dataset_parser.set_defaults(func = dataset)
    inject_parser = subparsers.add_parser('inject',
                                          help = 'Inject an attack into the dataset')
    inject_parser.set_defaults(func = inject)
    info_parser = subparsers.add_parser('info',
                                        help = 'View information about dataset')
    # info_parser.set_defaults(func = info)

    dataset_group_parser(dataset_parser)
    inject_group_parser(inject_parser)
    # info_group_parser(info_parser)

    args = parser.parse_args()
    if args.func is not None:
        args.func(args)
    else:
        parser.print_help()


def main():
    parser_setting()
    # @todo 1: Add CAN FD Option
    # @todo 2: Code Refactoring
    # @todo 3: Update description in help command


if __name__ == '__main__':
    main()
