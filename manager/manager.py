import json
import os
import signal
from typing import List


class ProcessManager:
    def __init__(self, db_file="pmdb.json"):
        self.DB_FILE = db_file
        self.processes = {}
        self.load()

    # ---------------- DB ----------------

    def load(self):
        """Load process state from disk"""
        if os.path.exists(self.DB_FILE):
            with open(self.DB_FILE, "r") as f:
                try:
                    self.processes = json.load(f)
                except json.JSONDecodeError:
                    self.processes = {}
        else:
            self.processes = {}
            self.save()

    def save(self):
        """Persist state to disk"""
        with open(self.DB_FILE, "w") as f:
            json.dump(self.processes, f, indent=2)

    def list_processes(self):
        """List all running processes"""
        if not self.processes:
            print("No running processes.")
            return

        print("-" * 30)
        print("Name", "PID", "Status")
        print("-" * 30)
        for name, process in self.processes.items():
            pid = process.get("pid", "Unknown")
            status = process.get("status", "Unknown")
            print(f"{name}: {pid} ({status})")

    def create_process(self, name: str, cmd: List[str]):
        """Create a new process entry"""

        if name in self.processes:
            print(f"[ERROR] Process '{name}' already exists")
            return

        self.processes[name] = {
            "cmd": cmd,
            "pid": None,
            "status": "created",
            "restart": False,
        }

        self.save()
        print(f"[CREATED] {name} -> {' '.join(cmd)}")

    def stop_process(self, name: str):
        """Stop a running process"""
        if name not in self.processes:
            print(f"[ERROR] Process '{name}' not found")
            return

        process = self.processes[name]
        if process.get("pid") is None:
            print(f"[ERROR] Process '{name}' is not running")
            return

        pid = process["pid"]
        os.kill(pid, signal.SIGTERM)
        process["pid"] = None
        process["status"] = "stopped"
        self.save()
        print(f"[STOPPED] {name} (pid: {pid})")

    def restart_process(self, name: str):
        """Restart a running process"""
        if name not in self.processes:
            print(f"[ERROR] Process '{name}' not found")
            return

        process = self.processes[name]
        if process.get("pid") is None:
            print(f"[ERROR] Process '{name}' is not running")
            return

        pid = process["pid"]
        os.kill(pid, signal.SIGTERM)
        process["pid"] = None
        process["status"] = "restarting"
        self.save()
        print(f"[RESTARTING] {name} (pid: {pid})")
        self.start_process(name)

    def start_process(self, name: str):
        """Start a process"""
        if name not in self.processes:
            print(f"[ERROR] Process '{name}' not found")
            return

        process = self.processes[name]
        if process.get("pid") is not None:
            print(f"[ERROR] Process '{name}' is already running")
            return

        cmd = process["cmd"]
        pid = os.fork()
        if pid == 0:
            try:
                os.execvp(cmd[0], cmd)
            except Exception as e:
                print(f"[ERROR] {e}")
                exit(1)
        else:
            process["pid"] = pid
            process["status"] = "running"
            self.save()
            print(f"[STARTED] {name} (pid: {pid})")

    def delete_process(self, name: str):
        """Delete a process"""
        if name not in self.processes:
            print(f"[ERROR] Process '{name}' not found")
            return

        process = self.processes[name]
        if process.get("pid") is not None:
            pid = process["pid"]
            os.kill(pid, signal.SIGTERM)
            process["pid"] = None
            process["status"] = "stopped"
            self.save()
            print(f"[STOPPED] {name} (pid: {pid})")

        del self.processes[name]
        self.save()
        print(f"[DELETED] {name}")

    def logs(self, name: str):
        """Show logs for a process"""
        if name not in self.processes:
            print(f"[ERROR] Process '{name}' not found")
            return

        process = self.processes[name]
        if process.get("pid") is None:
            print(f"[ERROR] Process '{name}' is not running")
            return

        pid = process["pid"]
        try:
            with open(f"/proc/{pid}/fd/1", "r") as f:
                for line in f:
                    print(line.strip())
        except Exception as e:
            print(f"[ERROR] {e}")
