import shutil
import subprocess
from typing import List

import resource
from django.conf import settings

from code_runner.celery import app


def __compile(cmd):
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        user=settings.RESTRICTED_USER,
    )
    output, err = proc.communicate()

    return output, err


def __execute(cmd, timeout: int):
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
        output = b""
        err = b"TLE"
        exec_time = ""

    return output, err, exec_time


@app.task
def async_execute(cmds: List[List[str]], timeout: int, path: str, lang: str):
    """
    Tasks API for handling all async code compilations and executions
    """
    if len(cmds) == 2:
        _, err = __compile(cmds[0])
        if len(err.decode("utf-8")):
            shutil.rmtree(path)
            return {
                "lang": lang,
                "output": "",
                "err": {
                    "compilation_error": err.decode("utf-8"),
                    "runtime_error": "",
                },
                "exec_time": None,
            }
        output, err, exec_time = __execute(cmd=cmds[1], timeout=timeout)
    elif len(cmds) == 1:
        output, err, exec_time = __execute(cmd=cmds[0], timeout=timeout)
    else:
        raise ValueError("cmds should be at-most length 2")

    shutil.rmtree(path)

    return {
        "lang": lang,
        "output": output.decode("utf-8"),
        "err": {
            "compilation_error": "",
            "runtime_error": err.decode("utf-8"),
        },
        "exec_time": exec_time,
    }
