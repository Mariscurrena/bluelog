# BlueLog 🔒🟦

An ultra-lightweight, open-source Python library that seamlessly extends the native `logging` module to add ANSI color support in the terminal and a dedicated `SUCCESS` log level. 

Built with a cybersecurity mindset: clean, efficient, and zero-dependency.

## Features

* **Zero Third-Party Dependencies:** 100% built on top of Python's native `logging` module.
* **Custom `SUCCESS` Level:** Introduces a new severity level (numeric value: 25) sitting perfectly between `INFO` (20) and `WARNING` (30).
* **ANSI Color Formatting:** High-visibility, color-coded terminal output to spot critical events or successful exploits/mitigations at a glance.
* **Duplication Safe:** Smart initialization prevents duplicate handlers even if `get_logger` is invoked multiple times across different modules.

## Installation

You can install `BlueLog` directly from GitHub using `pip`:

```bash
pip install git+https://github.com/
```

## Quick Start
Using `BlueLog` is as straightforward as using the standard library:

```python
import logging
from bluelog import get_logger

# 1. Initialize the logger (Default level is INFO, but you can set any level)
logger = get_logger("CyberSecApp", level=logging.DEBUG)

# 2. Test the color-coded severity levels
logger.debug("Scanning network range... (Cyan)")
logger.info("Connection established with target host. (Green)")

# Here is your brand-new custom level!
logger.success("Exploit payload executed successfully! (Bright/Bold Green)")

logger.warning("Unusual traffic pattern detected on port 443. (Yellow)")
logger.error("Failed to parse incoming firewall log packet. (Red)")
logger.critical("Privilege escalation detected! System compromised. (White on Red)")
```

## Customizing the Output
The logger defaults to a clean, production-ready format:

`YYYY-MM-DD HH:MM:SS | LEVELNAME | LOGGER_NAME | MESSAGE`

Only the `LEVELNAME` prefix is colorized, keeping your main log messages clean, readable, and easy to parse or pipe into other security tools.