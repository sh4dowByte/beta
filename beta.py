import argparse
import sys
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from app.scan import scan
from app.script import load_script
from app.utils.helper import display_banner, print_result, tabbed_result
from app.utils.network import ipman, process_ip_list
from rich.console import Console
from rich.tree import Tree

# Global variables
progress_lock = threading.Lock()
progress_counter = 0
progress_global = None
total_hosts = 0
total_hosts_up = 0
total_hosts_close = 0
output = []

# Initialize rich console
console = Console()

# Initialize stop event
stop_event = threading.Event()

def run(ip, options):
    """
    Executes the scan on a single IP address and puts the result into the queue.
    
    Args:
        ip (str): The IP address to scan.
        options (dict): Scan options including timeout, limit_text, banner, port, and max_workers.
    """
    global progress_counter, total_hosts_up, total_hosts_close

    if stop_event.is_set():
        return
    
    result = scan(options, {'ip': ip})

    progress_counter += 1
    description = f"Scanning {progress_counter}/{total_hosts}"
    progress_global.update(task_global, advance=1, description=description)


    if result:
        total_hosts_up += 1
        return result
    
    total_hosts_close += 1

def perform_concurrent_scans(ips, options):
    """
    Performs scanning concurrently using multiple threads.
    
    Args:
        ips (list): List of IP addresses to scan.
        options (dict): Scan options including timeout, limit_text, banner, port, and max_workers.
    """
    global total_hosts, progress_global, task_global
    total_hosts = len(ips)

    # Initialize Rich console
    console = Console()
    host_up = 0
    try:
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(run, ip.strip() if ip is not None else '', options) for ip in ips]

            with Progress(
                SpinnerColumn(spinner_name="dots", style="bold green"),
                TextColumn("[progress.description]{task.description}"),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task_global = progress.add_task("Scanning Start", total=total_hosts)
                progress_global = progress

                for future in as_completed(futures):
                    if stop_event.is_set():
                        break
                    result = future.result()
                    if result:
                        console.print(result)
                        console.print('\n')
                        host_up += 1
                       
                # progress.remove_task(task_global)

        console.print(f"  [cyan][UP][/cyan] Host Up      : {total_hosts_up}")
        console.print(f"  [red][CL][/red] Host Close   : {total_hosts_close}")
    except KeyboardInterrupt:
        console.print("[red]Scanning interrupted by user. Exiting...[/red]")
        sys.exit(1)

def main():
    """
    Main function to parse arguments, prepare IP list, and start concurrent scanning.
    """
    global total_hosts

    display_banner()

    parser = argparse.ArgumentParser(
        description="Beta - A tool for port scanning and information gathering."
    )

    parser.add_argument(
        "targets", nargs='*',
        help="IP addresses, domain names, file paths containing IP addresses, or CIDR network ranges."
    )
    parser.add_argument(
        "-p", "--port", type=str, default='ALL',
        help="Port to scan. Default is 'ALL'."
    )
    parser.add_argument(
        "--list", type=str,
        help="File containing a list of IP addresses to check."
    )
    parser.add_argument(
        "--timeout", type=int, default=2,
        help="Timeout for the scan in seconds. Default is 2 seconds."
    )
  
    parser.add_argument(
        "--max_workers", type=int, default=10,
        help="Maximum number of concurrent workers. Default is 10."
    )
    parser.add_argument(
        "--script", type=str, default='',
        help="Script Engine"
    )
    
    parser.add_argument(
        "-A", action="store_true",
        help="Use All Script Engine"
    )
    parser.add_argument(
        "-l", "--limit-text", action="store_false",
        help="Show all text output for the scan results, no limited text."
    )
    parser.add_argument(
        "-b", "--banner", action="store_true",
        help="Show banner information in scan results."
    )

    args = parser.parse_args()

    if not args.targets and not args.list:
        print("No arguments provided.")
        parser.print_help()
        sys.exit(1)

    targets = args.targets
    script = args.script

    ips = []
    if args.list:
        ips.extend(process_ip_list(args.list))
    else:
        ips.extend(ipman(targets))

    if not ips:
        ips.append(None)
    
    try:
        script, metadata = load_script(script, {}, all = args.A)
        perform_concurrent_scans(ips, {
            'timeout': args.timeout,
            'limit_text': args.limit_text,
            'banner': args.banner,
            'port': args.port,
            'max_workers': args.max_workers,
            'script': script,
        })
    except KeyboardInterrupt:
        console.print("[red]Process interrupted by user. Exiting...[/red]")
        stop_event.set()  # Signal all threads to stop
        sys.exit(1)

if __name__ == "__main__":
    main()
