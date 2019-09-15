from pprint import pprint
import psutil


def total_usage():
    # returns total system network usage as a namedtuple
    return psutil.net_io_counters()


def per_nic_usage():
    # pernic=True, return information for every network interface as dictionary
    # key = network interface card name,     value = namedtuple
    return psutil.net_io_counters(pernic=True)


def my_nic_usage(nic):
    # returns network usage for the specified nic
    all_nics = per_nic_usage()
    return all_nics.get(nic, 'NIC not found!')


def nics_stats():
    # information about each NIC installed on the system as a dictionary.
    # key = NIC name,     value = named tuple
    return psutil.net_if_stats()


def nics_running():
    # returns a list of NIC names that are running(up).
    nics_dict = nics_stats()

    # exclude the 'Local Host' from the running NICs.
    # list comprehension
    running_nic = [nic for nic, stats in nics_dict.items()
                   if stats.isup and ('loopback' not in nic.lower())]

    return running_nic


def print_stats():
    print()
    print(f'Running Network Interface Cards (NICs)     '
          f'Bytes Received    '
          f'Bytes Sent    ')

    total_bytes = 0
    for my_nic in nics_running():
        usage = my_nic_usage(my_nic)               # NIC status as named tuple
        received = usage.bytes_recv                # bytes received in int
        sent = usage.bytes_sent                    # bytes sent in int
        total_bytes += (received + sent)
        print(f'{my_nic.ljust(43)}'
              f'{str(received).ljust(18)}'
              f'{str(sent).ljust(14)}')

    print(f'\nTotal Bytes: {total_bytes / (1024 ** 2):.2f} MB')


if __name__ == '__main__':
    print_stats()