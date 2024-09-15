import json
from app.utils.helper import tabbed_result
from app.utils.network import check_connection, get_banner
from app.utils.style import Colors
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from rich.console import Console
from rich.tree import Tree

ports = []

# Initialize rich console
console = Console()

def scan(options, var):
    """Executes the port scan with the given options and returns the result."""
    ip = var['ip']

    tree = Tree(f'Server on [green]{ip}[/green]')
    result = pool(ip, options, tree)
    return result

def process_script_engines(ip, port, services, script_engines, tree):
    """Process the script engines and return the formatted script results."""
    for script_engine in script_engines:
        metadata = script_engine['metadata']
        run_script = script_engine['run']
        if set(services).issubset(metadata['portrule']):
            output = run_script(ip, port, script_engine['options'])
            
            if output:
                script = tree.add(f'[white]{script_engine['name']}[/white]', style="bright_black")
                if isinstance(output, list):
                    for ref in output:
                        script.add(ref)
                else:
                    script.add(output)


def get_open_port(ip, port, result_queue, options, tree):
    """Attempts to connect to a given port on the specified IP. If successful, logs the open port and services."""
    sock = check_connection(ip, port, options['timeout'])
    if sock:
        # Find all services associated with the open port
        services = [name for name, port_list in ports.items() if port in port_list]
        
        # Optionally retrieve the banner
        banner = get_banner(sock, options['timeout'], options
        ['limit_text']) if options['banner'] else ''
        port_open = tree.add(f'Port Open [green bold]{port}[/green bold] [[blue]{",".join(services)}[/blue]] {banner}')
        
        # Process script engines
        process_script_engines(ip, port, services, options['script'], port_open)

        result_queue.put((port, tree))

def pool(ip, options, tree):
    """Executes a port scan on the given IP with the specified options."""
    global ports
    with open('app/data/port.json', 'r') as file:
        ports = json.load(file)

    # Determine the list of ports to scan
    if 'ALL' not in options['port']:
        port_numbers = [int(x) for x in options['port'].split(',')]
    else:
        port_numbers = sorted(set(port for sublist in ports.values() for port in sublist))
    
    result_queue = Queue()
    
    # Use a ThreadPoolExecutor to scan ports concurrently
    with ThreadPoolExecutor(max_workers=options['max_workers']) as executor:
        futures = [executor.submit(get_open_port, ip, port, result_queue, options, tree) for port in port_numbers]
    
    # Ensure all threads have completed
    for future in futures:
        future.result()
    
    # Compile and return the scan results
    if not result_queue.empty():
        return tree
