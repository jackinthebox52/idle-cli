import sys
import code
import traceback
import signal
import select
import datetime
import io

def print_idle_info():
    python_version = sys.version.split()[0]
    build_date_str = sys.version.split('(')[1].split(',')[1].strip()
    build_date = datetime.datetime.strptime(build_date_str, "%b %d %Y").strftime("%b %d %Y")
    compiler = sys.version.split('[')[-1].split(']')[0]
    info_string = f"Python {python_version} ({sys.version_info.releaselevel}, {build_date}) [{compiler}] on {sys.platform}"
    print(info_string)
    print('Type "help", "copyright", "credits" or "license()" for more information. idle-cli.')
    #print('IDLE-CLE (GPL-3.0) by jackinthebox52: https://www.github.com/jackinthebox52/idle-cli')

class Tee(io.TextIOBase):
    def __init__(self, filename, mode='w', encoding='utf-8'):
        self.file = open(filename, mode, encoding=encoding)
        self.stdout = sys.stdout

    def write(self, data):
        self.file.write(data)
        self.file.flush()
        self.stdout.write(data)
        self.stdout.flush()

    def close(self):
        self.file.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python idle-cli.py OUTPUT_FILE")
        sys.exit(1)

    output_file = sys.argv[1]

    print_idle_info()

    console = code.InteractiveConsole()

    with Tee(output_file) as f:
        sys.stdout = f  # Redirect stdout to the Tee object

        console.write = f.write

        def handle_interrupt(signum, frame):
            interrupt_name = {
                signal.SIGINT: "KeyboardInterrupt",
                signal.SIGTSTP: "SuspensionInterrupt",
            }.get(signum, f"Signal {signum}")

            f.write(f"\n{interrupt_name}\n")
            #console.write(f"\n{interrupt_name}\n")
            console.resetbuffer()

            if signum == signal.SIGINT:
                nonlocal consecutive_interrupts
                consecutive_interrupts += 1

                if consecutive_interrupts >= 2:
                    raise KeyboardInterrupt("Exiting due to consecutive interrupts")
        
        consecutive_interrupts = 0

        for sig in [signal.SIGINT, signal.SIGTSTP]:
            signal.signal(sig, handle_interrupt)

        try:
            while True:
                try:
                    code_block = console.raw_input(">>> ")
                    f.write(code_block + "\n")

                    if code_block.lower() in ["exit()", "quit()"]:
                        break
                    more = console.push(code_block)
                    while more:
                        f.write("... ")
                        code_block = console.raw_input("... ")
                        f.write(code_block + "\n")
                        more = console.push(code_block)
                        
                    consecutive_interrupts = 0

                except KeyboardInterrupt as e:
                    if str(e) == "Exiting due to consecutive interrupts":
                        break
                    console.write("\nKeyboardInterrupt\n")
                    console.resetbuffer()
                except EOFError:
                    break
                except Exception:
                    traceback.print_exc()  # Print to the Tee object (both terminal and file)
        finally:
            sys.stdout = sys.__stdout__  # Restore original stdout

if __name__ == "__main__":
    main()
