from manager.manager import ProcessManager


class ProcessCMD:
    def __init__(self):
        self.manager = ProcessManager()

    def run(self, args):
        if not args:
            self.print_help()
            return

        cmd = args[0]
        list_cmds = ["list", "ls"]
        start_cmds = ["start", "run", "rn"]
        stop_cmds = ["stop", "kill"]
        create_cmds = ["create", "new", "nu"]
        logs_cmds = ["logs", "log", "lg"]
        delete_cmds = ["delete", "del", "remove", "rm"]

        if cmd in list_cmds:
            self.manager.list_processes()
        elif cmd in start_cmds:
            if len(args) < 2:
                print("[ERROR] Missing process name")
                return
            name = args[1]
            self.manager.start_process(name)
        elif cmd in stop_cmds:
            if len(args) < 2:
                print("[ERROR] Missing process name")
                return
            name = args[1]
            self.manager.stop_process(name)
        elif cmd in create_cmds:
            if len(args) < 2:
                print("[ERROR] Missing process name")
                return

            if len(args) < 3:
                print("[ERROR] Missing command")
                return

            name = args[1]
            cmd = args[2:]
            self.manager.create_process(name, cmd)
        elif cmd in logs_cmds:
            if len(args) < 2:
                print("[ERROR] Missing process name")
                return
            name = args[1]
            self.manager.logs(name)
        elif cmd in delete_cmds:
            if len(args) < 2:
                print("[ERROR] Missing process name")
                return
            name = args[1]
            self.manager.delete_process(name)
        else:
            self.print_help()

    def print_help(self):
        print("Usage: procm <command>")
        print("Commands:")
        print("\tcreate, new, nu                - Create a new process")
        print("\tlist, ls                       - List all running processes")
        print("\tstart, run, rn                 - Start a new process")
        print("\tstop, kill                     - Stop a running process")
        print("\tlogs, log, lg                  - View logs of a process")
        print("\tdelete, del, remove, rm        - Delete a process")
