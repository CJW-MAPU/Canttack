import argparse
import os
import textwrap
from argparse import RawDescriptionHelpFormatter

from module.AttackBuilder import AttackBuilder
from module.parser import dataset_group_parser, inject_group_parser
from module.utils import create_can_normal_dataset, create_can_fd_normal_dataset

from exception import ExceptionController


def dataset(args):
    is_can, is_can_fd = args.can, args.can_fd
    dest, target = args.name, args.target
    f = None

    try:
        f = open(f'{target}.txt')
    except FileNotFoundError:
        exit(f'{target}.txt file is Not Found! please check file in current directory {os.getcwd()}')

    if is_can:
        create_can_normal_dataset(f, dest)
    elif is_can_fd:
        create_can_fd_normal_dataset(f, dest)


def inject(args):
    is_can, is_can_fd = args.can, args.can_fd
    is_dos, is_fuzzing, is_replay, is_spoofing = args.dos, args.fuzzing, args.replay, args.spoofing
    count, target = args.count, args.target

    builder = AttackBuilder(target)

    if is_dos and is_can:
        builder.set_attack_type('dos')
    elif is_fuzzing and is_can:
        builder.set_attack_type('fuzzing')
    elif is_replay and is_can_fd:
        builder.set_attack_type('replay')
    elif is_spoofing and is_can_fd:
        builder.set_attack_type('spoofing')
    else:
        ExceptionController.CallTypeMatchException()

    for i in range(0, count):
        builder.inject_attack()

    builder.build()


def parser_setting():
    parser = argparse.ArgumentParser(description = textwrap.dedent('''\
        canttack is a tool for creating {CAN|CAN FD} normal dataset and injecting attack into dataset.\n
        Attack types implemented only in the CAN dataset : [ DoS, Fuzzing ]
        Attack types implemented only in the CAN-FD dataset : [ Replay, Spoofing ] \n
        DoS : The injected attack has a interval of 0.00025 and about 4000 pieces of data are injected.
        Fuzzing : The injected attack has an interval equal to the average of the timestamps of the entire packet, and is injected for about 1 second. 
        Replay : ... 
        Spoofing : ... 
        '''), prog = 'canttack', formatter_class = RawDescriptionHelpFormatter)

    parser.add_argument('-V', '--version', action = 'version', version = 'canttack 2.1.1',
                        help = 'show this program version')
    parser.set_defaults(func = None)

    subparsers = parser.add_subparsers(metavar = 'command')
    dataset_parser = subparsers.add_parser('dataset',
                                           help = 'Create a normal dataset')
    dataset_parser.set_defaults(func = dataset)
    inject_parser = subparsers.add_parser('inject',
                                          help = 'Inject an attack into the dataset')
    inject_parser.set_defaults(func = inject)

    dataset_group_parser(dataset_parser)
    inject_group_parser(inject_parser)

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
