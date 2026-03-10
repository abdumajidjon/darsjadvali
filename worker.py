"""Taskiq worker runner"""

from taskiq.cli import run_worker

from app.workers.tasks import broker

if __name__ == "__main__":
    run_worker(broker)
