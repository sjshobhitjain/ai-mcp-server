import threading
import time
import traceback

print("✅ MCP Server starting...")

try:
    from agents.logsentinel_agent import run_agent as run_logsentinel
    print("✅ Imported LogSentinel agent")
except Exception as e:
    print("❌ Failed to import LogSentinel agent:", e)
    traceback.print_exc()

try:
    from agents.mdr_agent import run_agent as run_mdr
    print("✅ Imported MDR agent")
except Exception as e:
    print("❌ Failed to import MDR agent:", e)
    traceback.print_exc()

def main():
    print("🚀 Starting both agents...")

    t1 = threading.Thread(target=run_logsentinel, name="LogSentinel")
    t2 = threading.Thread(target=run_mdr, name="MDR")

    t1.start()
    t2.start()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("🛑 MCP Server shutting down.")

if __name__ == "__main__":
    main()
