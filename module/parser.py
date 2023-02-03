def dataset_group_parser(dataset_parser):
    dataset_group = dataset_parser.add_argument_group('Target Dataset Specification')
    dataset_group2 = dataset_parser.add_argument_group('Destination Dataset Specification')

    dataset_group.add_argument('-T', '--target', required = True, type = str,
                               help = 'Text file name extracted from {CAN | CAN FD}')
    dataset_group2.add_argument('-n', '--name', required = True, type = str,
                                help = 'Dataset created by processing target file')

    dataset_mutual_group = dataset_group.add_mutually_exclusive_group(required = True)

    dataset_mutual_group.add_argument('--can', action = 'store_true',
                                      help = 'Choose this if target is CAN text file')
    dataset_mutual_group.add_argument('--can-fd', action = 'store_true',
                                      help = 'Choose this if target is CAN FD text file')
    dataset_mutual_group.add_argument('--ae', action = 'store_true',
                                      help = 'Choose this if target is Automotive Ethernet data file')


def inject_group_parser(inject_parser):
    attack_spec_group = inject_parser.add_argument_group('Attack Specification')
    attack_spec_group.add_argument('-T', '--target', required = True, type = str,
                                   help = 'The name of the dataset you want to inject the attack into')

    attack_spec_group.add_argument('-c', '--count', type = int, default = 10,
                                   help = 'Number of attacks you want to inject into the dataset')

    attack_spec_group.add_argument('-p', '--packet', type = str, default = 'DefaultPacket.json',
                                   help = '')

    attack_spec_group.add_argument('-n', '--name', required = True, type = str,
                                   help = '')

    dataset_type_group = inject_parser.add_argument_group('Dataset Type')

    dataset_mutual_group = dataset_type_group.add_mutually_exclusive_group(required = True)
    dataset_mutual_group.add_argument('--can', action = 'store_true',
                                      help = 'Choose this if want inject any attack into CAN dataset')
    dataset_mutual_group.add_argument('--can-fd', action = 'store_true',
                                      help = 'Choose this if want inject any attack into CAN-FD dataset')
    dataset_mutual_group.add_argument('--ae', action = 'store_true',
                                      help = 'Choose this if want inject any attack into Automotive Ethernet dataset')

    attack_type_group = inject_parser.add_argument_group('Attack Type')

    inject_mutual_group = attack_type_group.add_mutually_exclusive_group(required = True)
    inject_mutual_group.add_argument('--dos', action = 'store_true',
                                     help = 'Choose this if want inject DoS attack into dataset')
    inject_mutual_group.add_argument('--fuzzing', action = 'store_true',
                                     help = 'Choose this if want inject Fuzzing attack into dataset')
    inject_mutual_group.add_argument('--replay', action = 'store_true',
                                     help = 'Choose this if want inject Replay attack into dataset')
    inject_mutual_group.add_argument('--spoofing', action = 'store_true',
                                     help = 'Choose this if want inject Spoofing attack into dataset')
