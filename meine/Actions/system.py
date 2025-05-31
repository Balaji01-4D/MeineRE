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
        return f"""[{get_theme_colors()['accent']}]DATE : {date}\nTIME : {time}
         [{get_theme_colors()["primary"]}]"primary"\n
        [{get_theme_colors()["secondary"]}] "secondary"\n ,
        [{get_theme_colors()["warning"]}]"warning"\n,
        [{get_theme_colors()["error"]}]"error"\n,
        [{get_theme_colors()["success"]}]"success": \n,
        [{get_theme_colors()["accent"]}]"accent": \n
        [{get_theme_colors()["foreground"]}]"foreground"\n,
        [{get_theme_colors()["background"]}]"background"\n,
        [{get_theme_colors()["foreground"]}]"foreground"\n,
        [{get_theme_colors()["panel"]}]"panel"\n,
        [{get_theme_colors()["boost"]}]"boost"\n,
        """

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

    async def Battery(self) -> Panel:
        theme = get_theme_colors()
        battery = await asyncio.to_thread(psutil.sensors_battery)

        if battery:
            BtPercent = round(battery.percent)
            progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(bar_width=30, complete_style=theme['accent']),
                "{task.percentage:>3.0f}%",
            )
            bt = progress.add_task(
                f"[bold cyan]  BATTERY % ", total=100, completed=BtPercent
            )
            progress.update(bt, completed=BtPercent)

            status_message = (
                f"[{theme['accent']}]{'Charging' if battery.power_plugged else 'Not Charging'}"
            )
            status = Panel(
                f"[{theme['foreground']}]Battery Status: {status_message}",
                expand=False,
                border_style=theme['primary'],
            )
            gp = Group(progress, status)
            return gp

        return f"[{theme['error']}]No battery information available.",

    async def NetWork(self) -> Panel:
        theme = get_theme_colors()
        net_info = await asyncio.to_thread(psutil.net_if_addrs)

        net = Table(title=f"Network Information",border_style=theme['primary'],title_style=theme['accent'])

        net.add_column(f"Interface", no_wrap=True, header_style=theme['accent'])
        net.add_column(f"Address", no_wrap=True, header_style=theme['accent'])
        net.add_column(f"Family", no_wrap=True, justify="left", header_style=theme['accent'])

        for interface, addresses in net_info.items():
            for address in addresses:
                net.add_row(interface, address.address, address.family.name,style=theme['foreground'])

        return net

    async def ENV(self) -> Table:
        theme = get_theme_colors()
        env_vars = await asyncio.to_thread(os.environ.items)

        env = Table(show_lines=True, title=f"[{theme['accent']}]ENV", border_style=theme['primary'])
        env.add_column(f"key", no_wrap=True, header_style=theme['accent'])
        env.add_column(f"value", no_wrap=True, header_style=theme['accent'])

        for key, value in env_vars:
            env.add_row(key, value,style=theme['foreground'])

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


    async def DiskInfo(self):
        theme = get_theme_colors()


        tableofdisk = Table(
            show_lines=True, border_style=theme['primary'], title=f"[{theme['primary']}]Disk Info"
        )
        headers = ["Device", "Total Size", "Used", "Free", "Usage"]
        alternative = None
        for header in headers:
            alternative = theme['foreground']
            tableofdisk.add_column(header, style=alternative, header_style=theme['accent'])

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
        return tableofdisk

    async def Processes(self):
        theme = get_theme_colors()
        tableofproccess = Table(show_lines=True, border_style=theme['primary'])
        headers = ["PID", "Name", "Status", "Memory (RAM)", "CPU Usage (%)"]
        for header in headers:
            tableofproccess.add_column(header, style=theme['foreground'], header_style=theme['foreground'])
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
