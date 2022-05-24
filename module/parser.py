def dataset_group_parser(dataset_parser):
    dataset_group = dataset_parser.add_argument_group('Target Dataset Specification')
    dataset_group2 = dataset_parser.add_argument_group('Destination Dataset Specification')

    dataset_group.add_argument('-T', '--target', required = True, type = str,
                               help = 'Text file name extracted from {CAN | CAN FD}.')
    dataset_group2.add_argument('-n', '--name', required = True, type = str,
                                help = 'Dataset created by processing target file.')

    dataset_mutual_group = dataset_group.add_mutually_exclusive_group(required = True)

    dataset_mutual_group.add_argument('--can', action = 'store_true',
                                      help = 'Choose this if target is CAN text file.')
    dataset_mutual_group.add_argument('--can-fd', action = 'store_true',
                                      help = 'Choose this if target is CAN FD text file.')


def inject_group_parser(inject_parser):
    attack_spec_group = inject_parser.add_argument_group('Attack Specification')
    attack_spec_group.add_argument('-T', '--target', required = True,
                                   help = 'The name of the dataset you want to inject the attack into.')

    attack_spec_group.add_argument('-c', '--count', type = int,
                                   help = 'Number of attacks you want to inject into the dataset.')

    attack_type_group = inject_parser.add_argument_group('Attack Type')

    inject_mutual_group = attack_type_group.add_mutually_exclusive_group(required = True)
    inject_mutual_group.add_argument('--ddos', action = 'store_true',
                                     help = '')
    inject_mutual_group.add_argument('--fuzzing', action = 'store_true',
                                     help = '')
