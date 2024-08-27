import sys
import code
import traceback
import signal
import select
import datetime

def print_idle_info():
    python_version = sys.version.split()[0] 
   
    build_date_str = sys.version.split('(')[1].split(',')[1].strip()
    build_date = datetime.datetime.strptime(build_date_str, "%b %d %Y").strftime("%b %d %Y")

    compiler = sys.version.split('[')[-1].split(']')[0]

    info_string = f"Python {python_version} ({sys.version_info.releaselevel}, {build_date}) [{compiler}] on {sys.platform}"
    print(info_string)
    print('Type "help", "copyright", "credits" or "license()" for more information. idle-cli.')
    #print('IDLE-CLE (GPL-3.0) by jackinthebox52: https://www.github.com/jackinthebox52/idle-cli')


def main():
    if len(sys.argv) != 2:
        print("Usage: python idle-cli.py OUTPUT_FILE")
        sys.exit(1)

    output_file = sys.argv[1]

    print_idle_info()

    console = code.InteractiveConsole()
    with open(output_file, "w") as f:
        def write_and_print(data):
            f.write(data)
            print(data, end="")

        console.write = write_and_print

        def handle_interrupt(signum, frame):
            interrupt_name = {
                signal.SIGINT: "KeyboardInterrupt",
                signal.SIGTSTP: "SuspensionInterrupt",
            }.get(signum, f"Signal {signum}")

            console.write(f"\n{interrupt_name}\n")
            console.resetbuffer()

            if signum == signal.SIGINT:
                nonlocal consecutive_interrupts
                consecutive_interrupts += 1
                if consecutive_interrupts >= 2:
                    raise KeyboardInterrupt("Exiting due to consecutive interrupts")

        consecutive_interrupts = 0

        for sig in [signal.SIGINT, signal.SIGTSTP]
            signal.signal(sig, handle_interrupt)

        try:
            while True:
                try:
                    code_block = console.raw_input(">>> ")
                    if code_block.lower() in ["exit()", "quit()"]:
                        break
                    more = console.push(code_block)
                    while more:
                        code_block = console.raw_input("... ")
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
                    traceback.print_exc(file=f)
        finally:
            f.close()

if __name__ == "__main__":
    main()
