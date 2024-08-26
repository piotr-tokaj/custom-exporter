import subprocess
from prometheus_client import Gauge
from dateutil import parser

ANSIBLE_LOG_FILE = "/usr/src/app/ansible.log"

ansible_ok_tasks = Gauge('ansible_ok_tasks', '', ['target_hostname', 'run_timestamp'])
ansible_changed_tasks = Gauge('ansible_changed_tasks', '', ['target_hostname', 'run_timestamp'])
ansible_unreachable_tasks = Gauge('ansible_unreachable_tasks', '', ['target_hostname', 'run_timestamp'])
ansible_failed_tasks = Gauge('ansible_failed_tasks', '', ['target_hostname', 'run_timestamp'])
ansible_skipped_tasks = Gauge('ansible_skipped_tasks', '', ['target_hostname', 'run_timestamp'])
ansible_rescued_tasks = Gauge('ansible_rescued_tasks', '', ['target_hostname', 'run_timestamp'])
ansible_ignored_tasks = Gauge('ansible_ignored_tasks', '', ['target_hostname', 'run_timestamp'])

def read_latest_log_lines():
    proc = subprocess.Popen(['tail', '-n', "1000", ANSIBLE_LOG_FILE], stdout=subprocess.PIPE, encoding='utf8', text=True)
    return reversed(proc.stdout.readlines())


def collect_ansible_run_results():
    logs = read_latest_log_lines()
    run_finish_time = 0
    result_log_lines = []

    ansible_ok_tasks.clear()
    ansible_changed_tasks.clear()
    ansible_unreachable_tasks.clear()
    ansible_failed_tasks.clear()
    ansible_skipped_tasks.clear()
    ansible_rescued_tasks.clear()
    ansible_ignored_tasks.clear()

    for log_line in logs:
        if 'PLAY RECAP' in log_line:
            run_finish_time = get_timestamp_from_log(log_line)
            break

        if "changed=" in log_line and "unreachable=" in log_line:
            result_log_lines.append(log_line)

    if not result_log_lines:
        print("Something went wrong during Ansible metric collection! No results found in the logs")

    for log_line in result_log_lines:
        parse_log_line(log_line, run_finish_time)


def parse_log_line(log_line, run_timestamp):
    try:
        parts = log_line.split('|')
        hostname = parts[1].split()[0]

        task_status_part = parts[1].split(': ')[1].strip()
        task_status_items = task_status_part.split()

        ok = int(task_status_items[0].split('=')[1])
        changed = int(task_status_items[1].split('=')[1])
        unreachable = int(task_status_items[2].split('=')[1])
        failed = int(task_status_items[3].split('=')[1])
        skipped = int(task_status_items[4].split('=')[1])
        rescued = int(task_status_items[5].split('=')[1])
        ignored = int(task_status_items[6].split('=')[1])

        ansible_ok_tasks.labels(
            target_hostname=hostname,
            run_timestamp=run_timestamp
        ).set(ok)

        ansible_changed_tasks.labels(
            target_hostname=hostname,
            run_timestamp=run_timestamp
        ).set(changed)

        ansible_unreachable_tasks.labels(
            target_hostname=hostname,
            run_timestamp=run_timestamp
        ).set(unreachable)

        ansible_failed_tasks.labels(
            target_hostname=hostname,
            run_timestamp=run_timestamp
        ).set(failed)

        ansible_skipped_tasks.labels(
            target_hostname=hostname,
            run_timestamp=run_timestamp
        ).set(skipped)

        ansible_rescued_tasks.labels(
            target_hostname=hostname,
            run_timestamp=run_timestamp
        ).set(rescued)

        ansible_ignored_tasks.labels(
            target_hostname=hostname,
            run_timestamp=run_timestamp
        ).set(ignored)

        return ansible_ok_tasks, ansible_changed_tasks, ansible_unreachable_tasks, ansible_failed_tasks, ansible_skipped_tasks, ansible_rescued_tasks, ansible_ignored_tasks
    except (IndexError, ValueError):
        print(f"Something went very wrong when parsing log line: {log_line}")
        return None


def get_timestamp_from_log(log_line):
    try:
        parts = log_line.split()
        date = parts[0]
        time = parts[1]

        return parser.parse(f"{date}T{time}").timestamp()
    except (IndexError, ValueError):
        print(f"Something went very wrong when parsing date from: {log_line}")
        return None


### Example log entries that this was tested on:
#
# print(get_timestamp_from_log("2024-08-16 09:31:53,605 p=110746 u=ansible n=ansible | kasm-database-dev          : ok=25   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0"))
# print(get_timestamp_from_log("2024-08-16 10:35:45,575 p=131019 u=ansible n=ansible | PLAY RECAP *********************************************************************"))
# parse_log_line("2024-08-16 09:31:53,605 p=110746 u=ansible n=ansible | kasm-database-dev          : ok=25   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0")
# parse_log_line("2024-08-16 09:31:53,605 p=110746 u=ansible n=ansible | kasm-webapp-dev-v7xq       : ok=23   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0")
# parse_log_line("2024-08-16 09:31:53,606 p=110746 u=ansible n=ansible | realm1-agent-tjf3          : ok=19   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0")
# parse_log_line("2024-08-16 09:31:53,605 p=110746 u=ansible n=ansible | ansible-dev                : ok=19   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   ")