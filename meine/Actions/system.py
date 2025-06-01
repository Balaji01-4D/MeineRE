import asyncio
import datetime as dt
import os
import platform
import shutil as sl
from pathlib import Path
from time import ctime

import psutil
from rich.console import Group
from rich.panel import Panel
from rich.progress import BarColumn, Progress
from rich.table import Table
from rich.text import Text

from ..exceptions import InfoNotify
from .other import SizeHelper
from .app_theme import get_theme_colors


class System:

    os_type = platform.system()

    def ShutDown(self):

        if self.os_type == "Windows":
            os.system(r"shutdown \s \t 60")
            raise InfoNotify("shutting down in 1 Minute")
        elif self.os_type == "Linux" or self.os_type == "Darwin":
            os.system("shutdown -h +1")
            raise InfoNotify("shutting down in 1 Minute")
        else:
            raise InfoNotify("Unsupported OS")

    def Reboot(self):

        if self.os_type == "Windows":
            os.system(r"shutdown \r \t 60")
            raise InfoNotify("restarting in 1 Minute")
        elif self.os_type == "Linux" or self.os_type == "Darwin":
            os.system("shutdown -r +1")
            raise InfoNotify("restarting in 1 Minute")
        else:
            raise InfoNotify("Unsupported OS")

    async def Time(self) -> Panel:
        date = dt.datetime.now().date()
        time = dt.datetime.now().time()
        return f"""[{get_theme_colors()['accent']}]DATE : {date}\nTIME : {time}"""

    async def DiskSpace(self, Destination: Path = Path("/")) -> Panel:
        try:
            theme = get_theme_colors()
            primary = theme['primary']
            accent = theme['accent']
            foreground = theme['foreground']

            disk_usage_task = asyncio.to_thread(sl.disk_usage, Destination)
            swap_memory_task = asyncio.to_thread(psutil.swap_memory)
            disk_usage, swap_memory = await asyncio.gather(
                disk_usage_task, swap_memory_task
            )

            total, used, free = disk_usage.total, disk_usage.used, disk_usage.free

            available_percentage = (free / total) * 100
            used_percentage = (used / total) * 100

            progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(bar_width=30, complete_style=accent),
                "{task.percentage:>3.0f}%",
                transient=True,
            )
            available_task = progress.add_task(
                "[{theme['foreground']}]AVAILABLE %", total=100, completed=available_percentage
            )
            used_task = progress.add_task(
                "[{theme['foreground']}]USED %", total=100, completed=used_percentage
            )

            storage_table = Table(show_lines=True, border_style=primary)
            storage_table.add_column("", justify="center", header_style=accent)
            storage_table.add_column("STORAGE", justify="center", header_style=accent)
            storage_table.add_column("SWAP MEMORY", justify="center", header_style=accent)
            storage_table.add_row(
                "TOTAL", SizeHelper(total), SizeHelper(swap_memory.total), style=foreground
            )
            storage_table.add_row(
                "USED", SizeHelper(used), SizeHelper(swap_memory.used), style=foreground
            )
            storage_table.add_row(
                "FREE", SizeHelper(free), SizeHelper(swap_memory.free), style=foreground
            )

            panel_collections = Group(
                Panel(f"[{foreground}]STORAGE", border_style=primary),
                Panel(storage_table, border_style=primary),
                Panel(progress, border_style=primary),
            )

            return panel_collections

        except Exception as e:
            raise InfoNotify("Error in getting disk space")

    async def GetCurrentDir(self) -> Panel:
        path: Path = str(Path(".").resolve())
        return Panel(f"CURRENT DIRECTORY: {path}", expand=False)

    async def Info(self, Name: Path) -> Table | str:
        theme = get_theme_colors()
        if not Name.exists():
            return f"[{theme['error']}]{Name.name} Not Found"

        try:
            stats, fullpath = await asyncio.gather(
                asyncio.to_thread(Name.stat), asyncio.to_thread(Name.resolve)
            )

            size = SizeHelper(stats.st_size)
            file_type = "File" if Name.is_file() else "Directory"
            foreground = theme['foreground']
            info = Table(show_header=False, show_lines=True, border_style=theme['primary'])
            info.add_row("Name", Name.name, style= foreground)
            info.add_row("Path", str(fullpath), style= foreground)
            info.add_row("Size", size, style= foreground)
            info.add_row("Type", file_type, style= foreground)
            info.add_row("Created", ctime(stats.st_ctime), style= foreground)
            info.add_row("Last Modified", ctime(stats.st_mtime), style= foreground)
            info.add_row("Last Accessed", ctime(stats.st_atime), style= foreground)

            return info

        except Exception as e:
            raise InfoNotify(f"Failed to retrieve info: {e}")

    async def IP(self) -> Table:

        import socket
        theme = get_theme_colors()
        try:
            hostname_task = asyncio.to_thread(socket.gethostname)
            hostname = await hostname_task

            ip_address_task = asyncio.to_thread(socket.gethostbyname, hostname)
            ip_address = await ip_address_task

            net_info = Table(show_header=False ,show_lines=True,border_style=theme['primary'])
            net_info.add_row(f"Hostname", hostname,style=theme['foreground'])
            net_info.add_row(f"IP Address", ip_address,style=theme['foreground'])

            return net_info

        except Exception as e:
            raise InfoNotify('Error in Fetching IP')

    async def HomeDir(self) -> Panel:
        theme = get_theme_colors()
        return f"[{theme['foreground']}]Home Directory :  [{theme['accent']}]{Path.home()}"

    async def RAMInfo(self) -> Panel:

        theme = get_theme_colors()
        primary = theme['primary']
        memory = await asyncio.to_thread(psutil.virtual_memory)
        total, available, used = memory.total, memory.available, memory.used
        data = {"AVAILABLE": available / total * 100, "USED": used / total * 100}

        rampanel = Progress(
            "[progress.description]{task.description}",
            BarColumn(bar_width=30, complete_style=theme['accent']),
            "{task.percentage:>3.0f}%",
        )

        rampanel.add_task(
            f"[{theme['foreground']}]AVAILABLE % ", total=100, completed=data["AVAILABLE"]
        )
        rampanel.add_task(f"[{theme['foreground']}]USED      % ", total=100, completed=data["USED"])

        ram_info_text = (
            f"[{theme['foreground']}]Total Memory      : [{theme['accent']}]{SizeHelper(total)}\n"
            f"[{theme['foreground']}]Memory Available  : [{theme['accent']}]{SizeHelper(available)}\n"
            f"[{theme['foreground']}]Memory Used       : [{theme['accent']}]{SizeHelper(used)}"
        )

        panel_group = Group(
            Panel(f"[{theme['accent']}]RAM", width=20, border_style=primary),
            Panel(rampanel, width=70, border_style=primary),
            Panel(ram_info_text, width=70, border_style=primary),
        )

        return panel_group

    # final
    async def SYSTEM(self) -> Panel:
        theme = get_theme_colors()
        system_info = [
            ("SYSTEM", platform.system()),
            ("NODE NAME", platform.node()),
            ("RELEASE", platform.release()),
            ("VERSION", platform.version()),
            ("MACHINE", platform.machine()),
            ("PROCESSOR", platform.processor()),
            ("CPU COUNT", str(psutil.cpu_count(logical=True))),
            ("CPU USAGE(%)", str(await asyncio.to_thread(psutil.cpu_percent, 1))),
        ]

        systemtable = Table(
            show_header=False,
            show_lines=True,
            title="SYSTEM INFO",
            border_style=theme['primary'],
        )
        systemtable.add_column("")

        for label, value in system_info:
            systemtable.add_row(label, value, style=theme['foreground'])

        rampanel = await self.RAMInfo()
        gp = Group(systemtable, rampanel)

        return gp

    async def Battery(self) -> Panel | str:
        """Get detailed battery information with improved error handling."""
        theme = get_theme_colors()

        try:
            battery = await asyncio.to_thread(psutil.sensors_battery)

            if not battery:
                return f"[{theme['error']}]No battery detected on this system"

            # Calculate battery percentage and time remaining
            percent = round(battery.percent)
            time_left = battery.secsleft if battery.secsleft != -1 else None

            # Create progress bar
            progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(
                    bar_width=30,
                    complete_style=theme['success'] if percent > 20 else theme['error'],
                ),
                "{task.percentage:>3.0f}%",
            )

            progress.add_task(
                f"[{theme['foreground']}]Battery Level",
                total=100,
                completed=percent
            )

            # Create status information
            status_items = [
                f"[{theme['foreground']}]Status: [{theme['accent']}]{'Charging' if battery.power_plugged else 'On Battery'}",
                f"[{theme['foreground']}]Plugged In: [{theme['accent']}]{'Yes' if battery.power_plugged else 'No'}"
            ]

            if time_left and not battery.power_plugged:
                hours = time_left // 3600
                minutes = (time_left % 3600) // 60
                status_items.append(
                    f"[{theme['foreground']}]Time Remaining: [{theme['accent']}]{hours:02d}:{minutes:02d}"
                )

            status_panel = Panel(
                "\n".join(status_items),
                border_style=theme['primary'],
                title=f"[{theme['accent']}]Battery Information"
            )

            return Group(progress, status_panel)

        except Exception as e:
            return f"[{theme['error']}]Error getting battery information: {str(e)}"

    async def NetWork(self) -> Table:
        """Get detailed network information with improved error handling."""
        theme = get_theme_colors()
        import socket

        try:
            # Get network interfaces and stats concurrently
            net_if_addrs, net_if_stats = await asyncio.gather(
                asyncio.to_thread(psutil.net_if_addrs),
                asyncio.to_thread(psutil.net_if_stats)
            )

            net = Table(
                title=f"[{theme['accent']}]Network Information",
                border_style=theme['primary'],
                show_lines=True
            )

            # Add columns for detailed network information
            net.add_column("Interface", header_style=theme['accent'])
            net.add_column("Address", header_style=theme['accent'])
            net.add_column("Type", header_style=theme['accent'])
            net.add_column("Status", header_style=theme['accent'])
            net.add_column("Speed", header_style=theme['accent'])

            for interface, addresses in net_if_addrs.items():
                # Get interface statistics
                stats = net_if_stats.get(interface)
                is_up = stats.isup if stats else False
                speed = f"{stats.speed} Mb/s" if stats and stats.speed > 0 else "N/A"

                # Group addresses by family
                for addr in addresses:
                    # Determine address type
                    if addr.family == socket.AF_INET:
                        addr_type = "IPv4"
                    elif addr.family == socket.AF_INET6:
                        addr_type = "IPv6"
                    elif addr.family == psutil.AF_LINK:
                        addr_type = "MAC"
                    else:
                        addr_type = "Unknown"

                    # Add row with status indicators
                    status = f"[{theme['success']}]Up" if is_up else f"[{theme['error']}]Down"

                    net.add_row(
                        interface,
                        addr.address,
                        addr_type,
                        status,
                        speed,
                        style=theme['foreground']
                    )

            return net

        except Exception as e:
            raise InfoNotify(f"Error getting network information: {str(e)}")

    async def ENV(self, page: int = 1, items_per_page: int = 20, filter_text: str = "") -> Table:
        theme = get_theme_colors()

        # Get environment variables asynchronously
        env_items = await asyncio.to_thread(lambda: list(os.environ.items()))

        # Apply filter if specified
        if filter_text:
            env_items = [
                (k, v) for k, v in env_items
                if filter_text.lower() in k.lower() or filter_text.lower() in v.lower()
            ]

        # Calculate pagination
        total_items = len(env_items)
        total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
        page = min(max(1, page), total_pages)

        start_idx = (page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_items)

        env = Table(
            show_lines=True,
            title=f"[{theme['accent']}]ENV (Page {page}/{total_pages})",
            border_style=theme['primary']
        )
        env.add_column("key", no_wrap=True, header_style=theme['accent'])
        env.add_column("value", no_wrap=True, header_style=theme['accent'])

        # Add the current page's items
        for key, value in env_items[start_idx:end_idx]:
            env.add_row(key, value, style=theme['foreground'])

        return env

    async def CPU(self) -> Panel:
        theme = get_theme_colors()
        Usage = await asyncio.to_thread(psutil.cpu_percent, interval=1)
        progress = Progress(
            "[progress.description]{task.description}",
            BarColumn(bar_width=30, complete_style=theme['accent']),
            "{task.percentage:>3.0f}%",
        )
        Task = progress.add_task(
            f"[{theme['foreground']}]  CPU PERCENT % ", total=100, completed=Usage
        )
        progress.update(Task, completed=Usage)

        cpu_count = await asyncio.to_thread(psutil.cpu_count, logical=True)
        cpu_freq = psutil.cpu_freq()
        Freqpanel = Panel(
            f"[{theme['foreground']}]CPU Count:[{theme['accent']}] {cpu_count}\n"
            f"[{theme['foreground']}]CPU FREQ RANGE:[{theme['accent']}] {cpu_freq.min} < {cpu_freq.current} < {cpu_freq.max}",
            expand=False,
            border_style=theme['primary']
        )

        gp = Group(progress, Freqpanel)
        return gp

    async def USER(self) -> Panel:
        theme = get_theme_colors()
        import getpass

        return f"[{theme['foreground']}]Current User:[{theme['accent']}] {getpass.getuser()}"


    async def DiskInfo(self) -> Table:
        """Get disk information with improved async handling and error checking."""
        theme = get_theme_colors()

        tableofdisk = Table(
            show_lines=True,
            border_style=theme['primary'],
            title=f"[{theme['accent']}]Disk Information"
        )
        headers = ["Device", "Mount Point", "File System", "Total Size", "Used", "Free", "Usage"]

        for header in headers:
            tableofdisk.add_column(header, header_style=theme['accent'])

        try:
            # Get partitions asynchronously
            partitions = await asyncio.to_thread(psutil.disk_partitions, all=True)

            # Gather disk usage information in parallel
            async def get_partition_info(partition):
                try:
                    usage = await asyncio.to_thread(psutil.disk_usage, partition.mountpoint)
                    return {
                        'partition': partition,
                        'usage': usage
                    }
                except (PermissionError, FileNotFoundError):
                    return None

            # Process all partitions concurrently
            partition_infos = await asyncio.gather(
                *[get_partition_info(p) for p in partitions]
            )

            # Add rows for valid partitions
            for info in partition_infos:
                if info is not None:
                    partition = info['partition']
                    usage = info['usage']

            tableofdisk.add_row(
                partition.device,
                        partition.mountpoint,
                        partition.fstype or "N/A",
                        f"{usage.total / (1024 ** 3):.1f} GB",
                        f"{usage.used / (1024 ** 3):.1f} GB",
                        f"{usage.free / (1024 ** 3):.1f} GB",
                f"{usage.percent}%",
                        style=theme['foreground']
            )

            return tableofdisk

        except Exception as e:
            raise InfoNotify(f"Error getting disk information: {str(e)}")

    async def Processes(self, limit: int = 50):
        """Get system processes with pagination and optimized CPU usage calculation."""
        theme = get_theme_colors()

        tableofprocess = Table(
            show_lines=True,
            border_style=theme['primary']
        )

        headers = ["PID", "Name", "Status", "Memory (MB)", "CPU Usage (%)"]
        alt_style = theme['accent']

        for header in headers:
            tableofprocess.add_column(header, style=alt_style)

        try:
            initial_cpu_times = {}
            processes = []

            # FIXED: Changed to regular function for threading
            def get_process_info():
                for proc in psutil.process_iter(['pid', 'name', 'status', 'memory_info', 'cpu_times']):
                    try:
                        info = proc.info
                        initial_cpu_times[info['pid']] = info['cpu_times']
                        processes.append(proc)
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                    if len(processes) >= limit:
                        break

            await asyncio.to_thread(get_process_info)

            # Measure elapsed time
            interval = 0.1
            await asyncio.sleep(interval)

            for proc in processes[:limit]:
                try:
                    pid = proc.pid
                    info = proc.as_dict(['name', 'status', 'memory_info', 'cpu_times'])

                    initial_times = initial_cpu_times.get(pid)
                    current_times = info['cpu_times']

                    if initial_times and current_times:
                        # Correct CPU usage calculation
                        initial_total = initial_times.user + initial_times.system
                        current_total = current_times.user + current_times.system
                        cpu_usage = ((current_total - initial_total) / interval) * 100
                    else:
                        cpu_usage = 0.0

                    memory = info['memory_info'].rss / (1024 * 1024)  # MB

                    tableofprocess.add_row(
                    str(pid),
                        info['name'],
                        str(info['status']),
                        f"{memory:.1f}",
                        f"{cpu_usage:.1f}",
                        style=theme['foreground']
                    )
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            return tableofprocess

        except Exception as e:
            raise InfoNotify(f"Error getting process information: {str(e)}")

    async def ProcessKill(self, pid: int) -> str:
        """Kill a process by its PID with proper async handling."""
        try:
            # Create Process object and kill it asynchronously
            process = await asyncio.to_thread(psutil.Process, int(pid))
            await asyncio.to_thread(process.kill)
            return f"[{get_theme_colors()['success']}]Process with PID {pid} has been terminated."
        except ValueError:
            return f"[{get_theme_colors()['error']}]Invalid PID format: {pid}"
        except psutil.NoSuchProcess:
            return f"[{get_theme_colors()['error']}]No process with PID {pid} exists."
        except psutil.AccessDenied:
            return f"[{get_theme_colors()['error']}]Permission denied to terminate process {pid}."
        except Exception as e:
            return f"[{get_theme_colors()['error']}]Error terminating process {pid}: {str(e)}"
