import psutil

def calculateMetric(serverIp, serverName):
    """
    Calculates a metric for deciding least loaded server
    The metric should be a number between 0 and 100.
    At the moment lower metric is concidered better.

    TODO could improve how the metric is calculated
    """
    metric = psutil.cpu_percent()
    return {"ip": serverIp, "name": serverName, "usage": str(metric) }