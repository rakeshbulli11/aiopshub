import psutil


def get_system_metrics():
    """
    Collect system metrics from the environment
    where the backend is running.
    """

    cpu_usage = psutil.cpu_percent(interval=1)

    memory_usage = psutil.virtual_memory().percent

    disk_usage = psutil.disk_usage("/").percent

    network_usage = (
        psutil.net_io_counters().bytes_sent
        + psutil.net_io_counters().bytes_recv
    ) / (1024 * 1024)

    return {
        "cpu_usage": round(cpu_usage, 2),
        "memory_usage": round(memory_usage, 2),
        "disk_usage": round(disk_usage, 2),
        "network_usage": round(network_usage, 2),
    }