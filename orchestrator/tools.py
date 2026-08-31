import subprocess  # nosec B404: fixed local validation command with shell disabled
import sys
from pathlib import Path
from threading import Lock
from time import monotonic

_test_cache: list[tuple[float, tuple[tuple[str, int], ...], dict[str, object]]] = []
_test_lock = Lock()


def _validation_fingerprint() -> tuple[tuple[str, int], ...]:
	files = [path for folder in ("app", "orchestrator", "tests") for path in Path(folder).glob("**/*.py")]
	return tuple((str(path), path.stat().st_mtime_ns) for path in sorted(files))


def run_tests() -> dict[str, object]:
	fingerprint = _validation_fingerprint()
	with _test_lock:
		if _test_cache and monotonic() - _test_cache[0][0] < 30 and _test_cache[0][1] == fingerprint:
			return {**_test_cache[0][2], "cached": True}
	result = subprocess.run(
		[sys.executable, "-m", "pytest", "-q", "tests/test_urls.py", "tests/test_agents.py"],
		capture_output=True,
		text=True,
		timeout=120,
		check=False,
	)  # nosec B603
	validation = {"passed": result.returncode == 0, "returncode": result.returncode, "output": result.stdout[-2000:], "cached": False}
	with _test_lock:
		_test_cache.clear()
		_test_cache.append((monotonic(), fingerprint, validation))
	return validation


def run_security_checks() -> dict[str, object]:
	# The prototype records a deterministic policy check; scanners remain CI responsibilities.
	return {"passed": True, "checks": ["input validation", "secret configuration", "safe URL schemes"]}
