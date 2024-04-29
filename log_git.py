#!/usr/bin/python3
'''
git hook script to log git command.
'''

import sys
import os
import re
import subprocess
import tempfile
import time
import logging
from logging.handlers import SysLogHandler

def setup_logger():
    # ロガーを作成します。
    logger = logging.getLogger(__name__)

    # SysLogHandlerを作成します。
    syslog_handler = SysLogHandler(address='/dev/log')
    logger.addHandler(syslog_handler)

    # StreamHandler（標準エラー出力）を作成します。
    stderr_handler = logging.StreamHandler()
    logger.addHandler(stderr_handler)

    # ログレベルを設定します。
    logger.setLevel(logging.INFO)

    return logger

def log_to_syslog_and_stderr(logger, *messages):
    result = ""
    for message in messages:
        result += message
    for line in result.split("\n"):
        logger.info(line)

# ロガーをセットアップします。
logger = setup_logger()

DEBUG_ON = True
GIT_PATH = "/usr/bin/git"
SEPARATOR = " "

RESET_COLOR   = "\033[0m"
MAZENTA_COLOR = "\033[35m"
RED_COLOR   = "\033[31m"
GREEN_COLOR = "\033[32m"
BLUE_COLOR  = "\033[34m"
YELLOW_COLOR = "\033[33m"
ERROR_COLOR = MAZENTA_COLOR
OK_COLOR    = GREEN_COLOR

def run_git_command_with_pipe(argv):
    '''
    Run git command with pipe.
    '''
    command = argv.copy()
    command.insert(0, GIT_PATH)
    workdir = os.getcwd()
    if DEBUG_ON:
        log_to_syslog_and_stderr(logger, BLUE_COLOR, f"DEBUG: [{workdir}]\n START ", SEPARATOR.join(command), RESET_COLOR)
    with subprocess.Popen(command) as process:
        exit_code = process.wait()
        if DEBUG_ON:
            color = OK_COLOR if exit_code == 0 else ERROR_COLOR
            log_to_syslog_and_stderr(logger, color, f"DEBUG: [{workdir}]\n DONE (code={exit_code}) ", SEPARATOR.join(command), RESET_COLOR)
        return exit_code

def main(argv):
    '''
    Main function.
    '''
    workdir = os.getcwd()
    if DEBUG_ON:
        log_to_syslog_and_stderr(logger, YELLOW_COLOR, f"DEBUG: [{workdir}]\n START: ", SEPARATOR.join(sys.argv), RESET_COLOR)
    exit_code = run_git_command_with_pipe(argv)
    if DEBUG_ON:
        color = OK_COLOR if exit_code == 0 else ERROR_COLOR
        log_to_syslog_and_stderr(logger, color, f"DEBUG: [{workdir}]\n DONE: ", SEPARATOR.join(sys.argv), RESET_COLOR)
    sys.exit(exit_code)

if __name__ == "__main__":
    main(sys.argv[1:])
