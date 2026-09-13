def analyze_metrics(cpu, memory, disk):
    recommendations = []

    if cpu >= 90:
        recommendations.append(
            "Critical CPU usage. Check running processes and reduce unnecessary workloads."
        )
    elif cpu >= 70:
        recommendations.append(
            "High CPU usage. Monitor processes and consider optimizing the application."
        )

    if memory >= 90:
        recommendations.append(
            "Critical memory usage. Check memory-consuming processes and consider restarting services."
        )
    elif memory >= 70:
        recommendations.append(
            "High memory usage. Monitor RAM consumption and application processes."
        )

    if disk >= 90:
        recommendations.append(
            "Critical disk usage. Remove unnecessary files or increase storage capacity."
        )
    elif disk >= 80:
        recommendations.append(
            "Disk usage is high. Consider cleaning logs and temporary files."
        )

    if not recommendations:
        recommendations.append(
            "System health is normal. No immediate action is required."
        )

    return recommendations