from __future__ import annotations

import re
from typing import Any

from libs.common.errors import ValidationError

_FACILITY_NAMES: tuple[str, ...] = (
    "kern",
    "user",
    "mail",
    "daemon",
    "auth",
    "syslog",
    "lpr",
    "news",
    "uucp",
    "cron",
    "authpriv",
    "ftp",
    "ntp",
    "audit",
    "alert",
    "clock",
    "local0",
    "local1",
    "local2",
    "local3",
    "local4",
    "local5",
    "local6",
    "local7",
)

_SEVERITY_NAMES: tuple[str, ...] = (
    "emerg",
    "alert",
    "crit",
    "err",
    "warning",
    "notice",
    "info",
    "debug",
)

_MAX_PRI = 191

# RFC 3164 BSD syslog header:
#   <PRI>Mon DD HH:MM:SS hostname program[PID]: message
_PRI_RE = re.compile(r"^<(\d{1,3})>(.*)$", re.DOTALL)
_HEADER_RE = re.compile(
    r"^([A-Z][a-z]{2})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+"
    r"(\S+)\s+"
    r"([^\[:\s]+)"
    r"(?:\[(\d+)\])?:\s*(.*)$",
    re.DOTALL,
)


def parse_syslog_line(
    line: str,
    *,
    max_length: int = 8192,
) -> dict[str, Any]:
    """Parse a single RFC 3164 syslog line.

    Returns a dict with ``raw_message`` and ``attributes``.

    Raises :class:`~libs.common.errors.ValidationError` for empty lines
    or lines exceeding *max_length*.
    """
    if not line:
        raise ValidationError("syslog line must not be empty")

    if len(line) > max_length:
        raise ValidationError(
            f"syslog line exceeds max length of {max_length}",
        )

    pri_match = _PRI_RE.match(line)
    if pri_match is None:
        return {"raw_message": line, "attributes": {}}

    priority = int(pri_match.group(1))
    if priority > _MAX_PRI:
        raise ValidationError(
            f"PRI value {priority} exceeds maximum of {_MAX_PRI}",
        )

    facility = _FACILITY_NAMES[priority >> 3]
    severity = _SEVERITY_NAMES[priority & 0x07]

    remainder = pri_match.group(2)
    header_match = _HEADER_RE.match(remainder)

    attributes: dict[str, Any] = {
        "priority": priority,
        "facility": facility,
        "severity": severity,
    }

    if header_match is not None:
        attributes["hostname"] = header_match.group(4)
        attributes["program"] = header_match.group(5)
        pid = header_match.group(6)
        if pid is not None:
            attributes["pid"] = int(pid)

    return {"raw_message": line, "attributes": attributes}
