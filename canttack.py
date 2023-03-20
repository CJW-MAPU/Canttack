import argparse
import os
import textwrap
from argparse import RawDescriptionHelpFormatter

from builder.AttackBuilder import AttackBuilder
from module.parser import dataset_group_parser, inject_group_parser
from module.utils import create_can_normal_dataset, create_can_fd_normal_dataset
from exception import ExceptionController
from common.Type import AttackType, DataType


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
    is_can, is_can_fd, is_ae = args.can, args.can_fd, args.ae
    is_dos, is_fuzzing, is_replay, is_spoofing = args.dos, args.fuzzing, args.replay, args.spoofing
    count, target, packet, name = args.count, args.target, args.packet, args.name

    data_type = None

    if is_can:
        data_type = DataType.CAN.value
    elif is_can_fd:
        data_type = DataType.FD.value
    elif is_ae:
        data_type = DataType.AE.value
    else:
        ExceptionController.CallNotSupportDataTypeException()

    builder = AttackBuilder(target, name, data_type = data_type)

    if is_dos:
        builder.set_attack_type(AttackType.DOS.value)
    elif is_fuzzing:
        builder.set_attack_type(AttackType.FUZZING.value)
    elif is_replay:
        builder.set_attack_type(AttackType.REPLAY.value)
    elif is_spoofing:
        builder.set_attack_type(AttackType.SPOOFING.value)
    else:
        ExceptionController.CallNotSupportAttackTypeException()

    for i in range(0, count):
        builder.inject_attack(filepath = packet)

    builder.build()


def parser_setting():
    parser = argparse.ArgumentParser(description = textwrap.dedent('''\
        canttack is a tool for creating {CAN|CAN FD} normal dataset and injecting attack into dataset.\n
        Attack types implemented only in the CAN dataset : [ DoS, Fuzzing ]
        Attack types implemented only in the CAN-FD dataset : [ DoS, Spoofing ] \n
        DoS : The injected attack has an interval of 0.00025 seconds and about 4,000 pieces of data are injected.
        Fuzzing : The injected attack has an interval of 0.0001 seconds and about 1,000 pieces of data are injected.
        Replay : ... 
        Spoofing : The injected attack has an interval of 0.0001 seconds and about 1,000 pieces of data are injected.
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
