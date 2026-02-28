from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from libs.adapters.spool import DiskSpool, InMemorySpool, SpoolReader, SpoolWriter


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------

def _accept_writer(writer: SpoolWriter) -> None:
    """Compile-time check: implementations satisfy SpoolWriter."""
    writer.write({"key": "value"})


def _accept_reader(reader: SpoolReader) -> None:
    """Compile-time check: implementations satisfy SpoolReader."""
    reader.read_all()
    reader.purge_expired(60)


def test_in_memory_spool_satisfies_protocols() -> None:
    spool = InMemorySpool()
    _accept_writer(spool)
    _accept_reader(spool)


def test_disk_spool_satisfies_protocols(tmp_path: Path) -> None:
    spool = DiskSpool(tmp_path / "spool")
    _accept_writer(spool)
    _accept_reader(spool)


# ---------------------------------------------------------------------------
# InMemorySpool
# ---------------------------------------------------------------------------

class TestInMemorySpool:
    def test_write_and_read_all(self) -> None:
        spool = InMemorySpool()
        spool.write({"event": "login"})
        spool.write({"event": "logout"})

        messages = spool.read_all()
        assert len(messages) == 2
        assert messages[0] == {"event": "login"}
        assert messages[1] == {"event": "logout"}

    def test_read_all_returns_copies(self) -> None:
        spool = InMemorySpool()
        original: dict[str, Any] = {"event": "test"}
        spool.write(original)

        result = spool.read_all()
        result[0]["event"] = "mutated"

        assert spool.read_all()[0]["event"] == "test"

    def test_write_stores_copy(self) -> None:
        spool = InMemorySpool()
        msg: dict[str, Any] = {"event": "test"}
        spool.write(msg)
        msg["event"] = "mutated"

        assert spool.read_all()[0]["event"] == "test"

    def test_purge_expired_removes_old_entries(self) -> None:
        spool = InMemorySpool()

        # Insert an entry with a backdated timestamp.
        old_ts = time.time() - 120
        spool._entries.append((old_ts, {"event": "old"}))
        spool.write({"event": "new"})

        purged = spool.purge_expired(ttl_seconds=60)
        assert purged == 1
        assert len(spool.read_all()) == 1
        assert spool.read_all()[0]["event"] == "new"

    def test_purge_expired_returns_zero_when_nothing_to_purge(self) -> None:
        spool = InMemorySpool()
        spool.write({"event": "fresh"})

        assert spool.purge_expired(ttl_seconds=60) == 0

    def test_read_all_empty(self) -> None:
        spool = InMemorySpool()
        assert spool.read_all() == []


# ---------------------------------------------------------------------------
# DiskSpool
# ---------------------------------------------------------------------------

class TestDiskSpool:
    def test_creates_directory(self, tmp_path: Path) -> None:
        target = tmp_path / "nested" / "spool"
        DiskSpool(target)
        assert target.is_dir()

    def test_write_and_read_all(self, tmp_path: Path) -> None:
        spool = DiskSpool(tmp_path / "spool")
        spool.write({"event": "login"})
        spool.write({"event": "logout"})

        messages = spool.read_all()
        assert len(messages) == 2
        assert messages[0] == {"event": "login"}
        assert messages[1] == {"event": "logout"}

    def test_write_creates_json_files(self, tmp_path: Path) -> None:
        spool_dir = tmp_path / "spool"
        spool = DiskSpool(spool_dir)
        spool.write({"event": "test"})

        files = list(spool_dir.glob("*.json"))
        assert len(files) == 1
        content = json.loads(files[0].read_text(encoding="utf-8"))
        assert content == {"event": "test"}

    def test_filename_format(self, tmp_path: Path) -> None:
        spool_dir = tmp_path / "spool"
        spool = DiskSpool(spool_dir)
        spool.write({"event": "test"})

        files = list(spool_dir.glob("*.json"))
        name = files[0].stem  # without .json
        parts = name.split("_", 1)
        assert len(parts) == 2
        # First part is a parseable timestamp
        float(parts[0])
        # Second part is a hex event id
        assert len(parts[1]) == 32

    def test_purge_expired_removes_old_files(self, tmp_path: Path) -> None:
        spool_dir = tmp_path / "spool"
        spool = DiskSpool(spool_dir)

        # Create an old file manually.
        old_ts = time.time() - 120
        old_file = spool_dir / f"{old_ts}_deadbeef00000000deadbeef00000000.json"
        old_file.write_text(json.dumps({"event": "old"}), encoding="utf-8")

        spool.write({"event": "new"})

        purged = spool.purge_expired(ttl_seconds=60)
        assert purged == 1

        remaining = spool.read_all()
        assert len(remaining) == 1
        assert remaining[0]["event"] == "new"

    def test_purge_expired_returns_zero_when_nothing_to_purge(
        self, tmp_path: Path
    ) -> None:
        spool = DiskSpool(tmp_path / "spool")
        spool.write({"event": "fresh"})

        assert spool.purge_expired(ttl_seconds=60) == 0

    def test_read_all_empty(self, tmp_path: Path) -> None:
        spool = DiskSpool(tmp_path / "spool")
        assert spool.read_all() == []

    def test_read_all_skips_corrupt_files(self, tmp_path: Path) -> None:
        spool_dir = tmp_path / "spool"
        spool = DiskSpool(spool_dir)
        spool.write({"event": "good"})

        # Create a corrupt file.
        corrupt = spool_dir / f"{time.time()}_badc0ffee0000000badc0ffee0000000.json"
        corrupt.write_text("NOT JSON{{{", encoding="utf-8")

        messages = spool.read_all()
        assert len(messages) == 1
        assert messages[0] == {"event": "good"}

    def test_purge_skips_unparseable_filenames(self, tmp_path: Path) -> None:
        spool_dir = tmp_path / "spool"
        spool = DiskSpool(spool_dir)

        # Create a file with a non-numeric timestamp prefix.
        bad_name = spool_dir / "notanumber_abc.json"
        spool_dir.mkdir(parents=True, exist_ok=True)
        bad_name.write_text(json.dumps({"event": "bad"}), encoding="utf-8")

        purged = spool.purge_expired(ttl_seconds=1)
        assert purged == 0
        assert bad_name.exists()

    def test_accepts_string_directory(self, tmp_path: Path) -> None:
        spool = DiskSpool(str(tmp_path / "str_spool"))
        spool.write({"event": "test"})
        assert len(spool.read_all()) == 1
