"""Main entry point for the Nightcore Dashboard Backend."""

import asyncio
import contextlib
import signal

from src.setup import create_api_server


async def main() -> None:
    """Main function to start the Nightcore Dashboard Backend."""
    # Set up logging
    # Create API Server
    server = create_api_server()
    server_task = asyncio.create_task(server.serve())

    loop = asyncio.get_running_loop()

    def shutdown() -> None:
        server.should_exit = True

    # Register signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, shutdown)

    try:
        await server_task
    except asyncio.CancelledError:
        pass  # add logging
    except Exception:
        pass  # add logging
    finally:
        # Cleanup resources
        pass  # add logging


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
