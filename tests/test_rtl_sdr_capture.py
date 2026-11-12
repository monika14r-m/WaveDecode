import sys
from types import ModuleType

import pytest

from src.capture.rtl_sdr_capture import capture_samples


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"center_frequency": 0}, "center_frequency"),
        ({"center_frequency": -1}, "center_frequency"),
        ({"center_frequency": float("nan")}, "center_frequency"),
        ({"center_frequency": float("inf")}, "center_frequency"),
        ({"center_frequency": True}, "center_frequency"),
        ({"center_frequency": 100e6, "sample_rate": 0}, "sample_rate"),
        ({"center_frequency": 100e6, "sample_rate": float("nan")}, "sample_rate"),
        ({"center_frequency": 100e6, "sample_rate": True}, "sample_rate"),
        ({"center_frequency": 100e6, "num_samples": 0}, "num_samples"),
        ({"center_frequency": 100e6, "num_samples": 2.5}, "num_samples"),
        ({"center_frequency": 100e6, "num_samples": True}, "num_samples"),
        ({"center_frequency": 100e6, "device_index": -1}, "device_index"),
        ({"center_frequency": 100e6, "device_index": 1.5}, "device_index"),
        ({"center_frequency": 100e6, "device_index": True}, "device_index"),
    ],
)
def test_rejects_invalid_capture_configuration(kwargs, message):
    with pytest.raises(ValueError, match=message):
        capture_samples(**kwargs)


def test_configures_device_reads_requested_samples_and_closes(monkeypatch):
    class FakeSdr:
        def __init__(self, device_index):
            self.device_index = device_index
            self.closed = False
            self.samples_requested = None

        def read_samples(self, count):
            self.samples_requested = count
            return ["iq"] * count

        def close(self):
            self.closed = True

    created = []

    def fake_sdr_factory(device_index):
        device = FakeSdr(device_index)
        created.append(device)
        return device

    fake_module = ModuleType("rtlsdr")
    fake_module.RtlSdr = fake_sdr_factory
    monkeypatch.setitem(sys.modules, "rtlsdr", fake_module)

    samples = capture_samples(
        center_frequency=100e6,
        sample_rate=2.4e6,
        num_samples=8,
        gain="auto",
        device_index=2,
    )

    assert samples == ["iq"] * 8
    assert created[0].device_index == 2
    assert created[0].sample_rate == 2.4e6
    assert created[0].center_freq == 100e6
    assert created[0].gain == "auto"
    assert created[0].samples_requested == 8
    assert created[0].closed is True


def test_closes_device_when_capture_fails(monkeypatch):
    created = []

    class FakeSdr:
        def __init__(self, device_index):
            self.closed = False
            created.append(self)

        def read_samples(self, count):
            raise OSError("device disconnected")

        def close(self):
            self.closed = True

    fake_module = ModuleType("rtlsdr")
    fake_module.RtlSdr = FakeSdr
    monkeypatch.setitem(sys.modules, "rtlsdr", fake_module)

    with pytest.raises(OSError, match="device disconnected"):
        capture_samples(center_frequency=100e6, num_samples=4)

    assert created[0].closed is True
