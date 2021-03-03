import os
import subprocess

import resource
from django.conf import settings

from code_runner.celery import app


@app.task
def async_execute(cmd: list, timeout: int, path: str, lang: str):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        user=settings.RESTRICTED_USER,
    )

    try:
        usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        output, err = proc.communicate(timeout=timeout)
        usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        exec_time = usage_end.ru_utime - usage_start.ru_utime
    except subprocess.TimeoutExpired:
        proc.kill()
        output = ""
        err = "TLE"
        exec_time = ""

    os.remove(path)

    return dict(
        {
            "lang": lang,
            "output": output,
            "err": err,
            "exec_time": exec_time,
        }
    )
