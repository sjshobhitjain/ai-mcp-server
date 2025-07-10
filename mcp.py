import threading
import time
from agents.logsentinel_agent import run_agent as run_logsentinel
from agents.mdr_agent import run_agent as run_mdr

def main():
    print("🎛️ Starting MCP Server with 2 AI agents...")

    # Create threads for each agent
    t1 = threading.Thread(target=run_logsentinel, name="LogSentinelAgent")
    t2 = threading.Thread(target=run_mdr, name="MDRWatchdogAgent")

    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("🛑 Shutting down MCP server.")
        exit()

if __name__ == "__main__":
    main()
