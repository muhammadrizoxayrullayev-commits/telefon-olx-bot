"""
runner.py - 24/7 Auto-Restart Supervisor Daemon
Ensures continuous 24/7 operation with automatic recovery, logging, and crash-proof supervision.
"""

import sys
import time
import subprocess
import logging
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [SUPERVISOR] %(levelname)-8s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(BASE_DIR / "runner.log", encoding="utf-8")
    ]
)
logger = logging.getLogger("Supervisor")


def run_supervisor():
    """Supervises bot.py, auto-restarting on unexpected termination"""
    python_exe = sys.executable
    bot_script = BASE_DIR / "bot.py"

    logger.info("==================================================")
    logger.info("🚀 Starting 24/7 Telegram Bot Supervisor...")
    logger.info(f"Target script: {bot_script}")
    logger.info(f"Python interpreter: {python_exe}")
    logger.info("==================================================")

    consecutive_crashes = 0
    start_time = time.time()

    while True:
        try:
            logger.info("Starting bot process...")
            process = subprocess.Popen(
                [python_exe, str(bot_script)],
                cwd=str(BASE_DIR)
            )

            # Wait for process to finish
            exit_code = process.wait()
            run_duration = time.time() - start_time

            if exit_code == 0:
                logger.info(f"Bot exited normally (code 0) after {run_duration:.1f}s. Restarting in 2s...")
                consecutive_crashes = 0
            else:
                consecutive_crashes += 1
                logger.warning(
                    f"Bot stopped with exit code {exit_code}. "
                    f"Consecutive crashes: {consecutive_crashes}. "
                    f"Lasted: {run_duration:.1f}s."
                )

            # Backoff delay if crashing too rapidly
            sleep_time = min(30, 2 * consecutive_crashes) if consecutive_crashes > 3 else 2
            logger.info(f"Waiting {sleep_time} seconds before auto-restarting...")
            time.sleep(sleep_time)
            start_time = time.time()

        except KeyboardInterrupt:
            logger.info("Supervisor stopped by user (Ctrl+C). Terminating bot...")
            try:
                process.terminate()
            except Exception:
                pass
            break
        except Exception as e:
            logger.error(f"Supervisor unexpected error: {e}", exc_info=True)
            time.sleep(5)


if __name__ == "__main__":
    run_supervisor()
