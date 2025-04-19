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

from ..exceptions import InfoNotify
from .other import SizeHelper   


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
        return Panel(f"[#2196F3]DATE : {date}\nTIME : {time}", expand=False)

    async def DiskSpace(self, Destination: Path = Path("/")) -> Panel:
        try:
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
                BarColumn(bar_width=30, complete_style="#2196F3", style="#F2F2F2"),
                "{task.percentage:>3.0f}%",
                transient=True,
            )
            available_task = progress.add_task(
                "[#2196F3]AVAILABLE %", total=100, completed=available_percentage
            )
            used_task = progress.add_task(
                "[#2196F3]USED %", total=100, completed=used_percentage
            )

            storage_table = Table(show_lines=True, style="#A6A6C3")
            storage_table.add_column("", justify="center")
            storage_table.add_column("[#2196F3]STORAGE", justify="center")
            storage_table.add_column("[#2196F3]SWAP MEMORY", justify="center")
            storage_table.add_row(
                "[#2196F3]TOTAL", SizeHelper(total), SizeHelper(swap_memory.total)
            )
            storage_table.add_row(
                "[#2196F3]USED", SizeHelper(used), SizeHelper(swap_memory.used)
            )
            storage_table.add_row(
                "[#2196F3]FREE", SizeHelper(free), SizeHelper(swap_memory.free)
            )

            panel_collections = Group(
                Panel("[#2196F3]STORAGE", style="#A6A6C3"),
                Panel(storage_table, style="#FFFFFF"),
                Panel(progress, style="#A6A6C3"),
            )

            return Panel(panel_collections, style="#1E1E2C", expand=False)

        except Exception as e:
            return Panel(f"[red]Error: {e}", style="#1E1E2C", expand=False)

    async def GetCurrentDir(self) -> Panel:
        path: Path = str(Path(".").resolve())
        return Panel(f"[#F2F2F2]CURRENT DIRECTORY: {path}", expand=False)

    async def Info(self, Name: Path) -> Table | str:
        if not Name.exists():
            return f"[red]{Name.name} Not Found"

        try:
            stats, fullpath = await asyncio.gather(
                asyncio.to_thread(Name.stat), asyncio.to_thread(Name.resolve)
            )

            size = SizeHelper(stats.st_size)
            file_type = "File" if Name.is_file() else "Directory"

            info = Table(show_header=False, show_lines=True, style="#2196F0")
            info.add_row("[#F2F2F2]Name", Name.name)
            info.add_row("[#F2F2F2]Path", str(fullpath))
            info.add_row("[#F2F2F2]Size", size)
            info.add_row("[#F2F2F2]Type", file_type)
            info.add_row("[#F2F2F2]Created", ctime(stats.st_ctime))
            info.add_row("[#F2F2F2]Last Modified", ctime(stats.st_mtime))
            info.add_row("[#F2F2F2]Last Accessed", ctime(stats.st_atime))

            return info

        except Exception as e:
            return f"[#E06C75] Failed to retrieve info: {e}"

    async def IP(self) -> Table:
        import socket

        try:
            # Asynchronously fetch hostname and IP address
            hostname_task = asyncio.to_thread(socket.gethostname)
            hostname = await hostname_task

            ip_address_task = asyncio.to_thread(socket.gethostbyname, hostname)
            ip_address = await ip_address_task

            # Create the table for display
            net_info = Table(show_header=False, style="color(105)", show_lines=True)
            net_info.add_row("[#F2F2F2]Hostname", hostname)
            net_info.add_row("[#F2F2F2]IP Address", ip_address)

            return net_info

        except Exception as e:
            # Handle potential exceptions (e.g., DNS issues)
            error_table = Table(show_header=False, style="color(105)", show_lines=True)
            error_table.add_row("[red]Error", str(e))
            return error_table

    async def HomeDir(self) -> Panel:
        return Panel(
            f"Home Directory :  {Path.home()}", expand=False, style="color(105)"
        )

    async def RAMInfo(self) -> Panel:
        memory = await asyncio.to_thread(psutil.virtual_memory)
        total, available, used = memory.total, memory.available, memory.used
        data = {"AVAILABLE": available / total * 100, "USED": used / total * 100}

        rampanel = Progress(
            "[progress.description]{task.description}",
            BarColumn(bar_width=30, complete_style="#61AFEF"),
            "{task.percentage:>3.0f}%",
        )

        rampanel.add_task(
            "[#C5C8C6]AVAILABLE % ", total=100, completed=data["AVAILABLE"]
        )
        rampanel.add_task("[#C5C8C6]USED      % ", total=100, completed=data["USED"])

        ram_info_text = (
            f"[#C5C8C6]Total Memory      : [#61AFEF]{SizeHelper(total)}\n"
            f"[#C5C8C6]Memory Available  : [#61AFEF]{SizeHelper(available)}\n"
            f"[#C5C8C6]Memory Used       : [#61AFEF]{SizeHelper(used)}"
        )

        panel_group = Group(
            Panel("[#61AFEF]RAM", width=20, border_style="#ABB2BF"),
            Panel(rampanel, width=70, border_style="#ABB2BF"),
            Panel(ram_info_text, width=70, border_style="#ABB2BF"),
        )

        return Panel(panel_group, expand=False, border_style="#ABB2BF")

    # final
    async def SYSTEM(self) -> Panel:
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
            title="[#61AFEF]SYSTEM INFO",
            border_style="#ABB2BF",
        )
        systemtable.add_column("", style="#61AFEF")

        for label, value in system_info:
            systemtable.add_row(label, value)

        rampanel = await self.RAMInfo()
        gp = Group(systemtable, rampanel)

        return Panel(gp, border_style="#ABB2BF", expand=False)

    async def Battery(self) -> Panel:
        battery = await asyncio.to_thread(psutil.sensors_battery)

        if battery:
            BtPercent = round(battery.percent)
            progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(bar_width=30, complete_style="#61AFEF"),
                "{task.percentage:>3.0f}%",
            )
            bt = progress.add_task(
                f"[bold cyan]  BATTERY % ", total=100, completed=BtPercent
            )
            progress.update(bt, completed=BtPercent)

            status_message = (
                f"[#61AFEF]{'Charging' if battery.power_plugged else 'Not Charging'}"
            )
            status = Panel(
                f"[#C5C8C6]Battery Status: {status_message}",
                expand=False,
                border_style="#ABB2BF",
            )
            gp = Group(progress, status)
            return Panel(gp, expand=False, border_style="#ABB2BF")

        return Panel(
            f"[bold green]No battery information available.",
            expand=False,
            border_style="#ABB2BF",
        )

    async def NetWork(self) -> Panel:
        net_info = await asyncio.to_thread(psutil.net_if_addrs)

        net = Table(title="[#61AFEF]Network Information")
        net.add_column("[#C5C8C6]Interface", no_wrap=True, style="#61AFEF")
        net.add_column("[#C5C8C6]Address", no_wrap=True, style=None)
        net.add_column("[#C5C8C6]Family", no_wrap=True, justify="left", style="#61AFEF")

        for interface, addresses in net_info.items():
            for address in addresses:
                net.add_row(interface, address.address, address.family.name)

        return Panel(net, expand=False)

    async def ENV(self) -> Panel:
        env_vars = await asyncio.to_thread(os.environ.items)

        env = Table(show_lines=True, title="[#61AFEF]ENV", border_style="#ABB2BF")
        env.add_column("[#C5C8C6]key", no_wrap=True, style="#61AFEF")
        env.add_column("[#C5C8C6]value", no_wrap=True)

        for key, value in env_vars:
            env.add_row(key, value)

        return Panel(env, expand=False, border_style="#ABB2BF")

    async def CPU(self) -> Panel:
        Usage = await asyncio.to_thread(psutil.cpu_percent, interval=1)
        progress = Progress(
            "[progress.description]{task.description}",
            BarColumn(bar_width=30, complete_style="#61AFEF"),
            "{task.percentage:>3.0f}%",
        )
        Task = progress.add_task(
            f"[#C5C8C6]  CPU PERCENT % ", total=100, completed=Usage
        )
        progress.update(Task, completed=Usage)

        cpu_count = await asyncio.to_thread(psutil.cpu_count, logical=True)
        cpu_freq = psutil.cpu_freq()
        Freqpanel = Panel(
            f"[#C5C8C6]CPU Count[/#C5C8C6]:[#61AFEF] {cpu_count}\n"
            f"[#C5C8C6]CPU FREQ RANGE:[/#C5C8C6][#61AFEF] {cpu_freq.min} < {cpu_freq.current} < {cpu_freq.max}",
            expand=False,
            border_style="#ABB2BF",
        )

        gp = Group(progress, Freqpanel)
        return Panel(gp, expand=False, border_style="#ABB2BF")

    async def USER(self) -> Panel:
        import getpass

        return Panel(
            f"[#C5C8C6]Current User:[#61AFEF] {getpass.getuser()}",
            expand=False,
            border_style="#ABB2BF",
        )

    async def DiskInfo(self):
        tableofdisk = Table(
            show_lines=True, border_style="#ABB2BF", title="[#61AFEF]Disk Info"
        )
        headers = ["Device", "Total Size", "Used", "Free", "Usage"]
        alternative = None
        for header in headers:
            alternative = "#61AFEF" if (alternative == None) else None
            tableofdisk.add_column(header, style=alternative)

        partitions = await asyncio.to_thread(psutil.disk_partitions)

        for partition in partitions:

            usage = psutil.disk_usage(partition.mountpoint)
            tableofdisk.add_row(
                partition.device,
                f"{usage.total / (1024 ** 3):.2f} GB",
                f"{usage.used / (1024 ** 3):.2f} GB",
                f"{usage.free / (1024 ** 3):.2f} GB",
                f"{usage.percent}%",
            )
        return Panel(tableofdisk, border_style="#ABB2BF", expand=False)

    async def Processes(self):
        tableofproccess = Table(show_lines=True, border_style="#ABB2BF")
        headers = ["PID", "Name", "Status", "Memory (RAM)", "CPU Usage (%)"]
        alternative = None
        for header in headers:
            alternative = "#61AFEF" if (alternative == None) else None
            tableofproccess.add_column(header, style=alternative)
        for proc in psutil.process_iter(attrs=["pid", "name", "status", "memory_info"]):
            try:
                pid = proc.info["pid"]
                name = proc.info["name"]
                status = proc.info["status"]
                memory = proc.info["memory_info"].rss / (1024 * 1024)
                cpu_usage = proc.cpu_percent(interval=0.1)
                tableofproccess.add_row(
                    str(pid),
                    name,
                    str(status),
                    f"{memory:.2f} MB",
                    f"{cpu_usage:.2f}%",
                    style="#98C379",
                )

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return tableofproccess

    async def ProcessKill(self, pid):
        try:
            process = asyncio.to_thread(psutil.Process, pid)
            asyncio.to_thread(process.kill)
            return f"Process with PID {pid} has been terminated."
        except psutil.NoSuchProcess:
            return f"No process with PID {pid} exists."
        except psutil.AccessDenied:
            return f"Permission denied to terminate the process {pid}."
        except Exception:
            return f"Permission denied to terminate the process {pid}"
