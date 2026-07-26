# hard-link

Puts a microscope on the network. `hard-link` runs on the computer the hardware is
physically wired to, wraps Micro-Manager's MMCore in an RPyC server, and exposes it
as ordinary Python method calls to any client that can reach the port.

It is the device-server half of a two-part system. The client half is
[`deepthought`](https://github.com/ndsystems/deepthought), which turns those calls
into bluesky plans and closed-loop experiments.

## Status

**Paused, and preserved as a record.** Written in 2021 against Micro-Manager 2.0
gamma. Not maintained, and it will not start unmodified — the two halves of the system
were developed together, and some of what it imports lives in `deepthought`. Read it
as a design reference.

## Why a network boundary

Micro-Manager's device adapters are C++ and effectively tie you to the machine the
hardware is attached to — usually a Windows box that must stay exactly as configured.
Wrapping MMCore in an RPyC service breaks that coupling:

```
  microscope PC (Windows)                    analysis PC (any OS)
  ┌────────────────────────┐                 ┌────────────────────────┐
  │ devices (serial/USB)   │                 │                        │
  │   ↕                    │                 │                        │
  │ Micro-Manager adapters │   RPyC / TCP    │  deepthought client    │
  │   ↕                    │ ←─────────────→ │  bluesky plans         │
  │ MMCore (pymmcore)      │   port 18861    │  RunEngine             │
  │   ↕                    │                 │                        │
  │ hard-link              │                 │                        │
  └────────────────────────┘                 └────────────────────────┘
```

Four things follow. Analysis code runs on whatever OS suits it. A client that dies from
its own bad logic does not take the hardware down — the server keeps its state and the
next client reconnects. Acquisition logic can be debugged and restarted freely without
touching the microscope's configuration. And because a scope is now just an address,
one client can hold connections to several at once: run an instance of `hard-link` on
each microscope, and a single `deepthought` session drives them all through one
`MMCoreInterface`. The lab ran two this way, `bright_star` and `eva_green`.

## Contents

| Path | Purpose |
|---|---|
| `hard-link/start_server.py` | Loads MMCore with a device configuration, serves it as an RPyC `Microscope` service |
| `hard-link/configs.py` | Micro-Manager directory and config-file paths, read from `MM_DIR` / `MM_CONFIG` environment variables with defaults |
| `hard-link/devices.py` | Server-side device abstractions, and `SimMMC` — a simulated core returning random crops of a DAPI image, so a client can be developed with no microscope attached |
| `hard-link/mmconfigs/` | Micro-Manager configurations: `Bright_Star.cfg` (the real scope), `demo.cfg` |
| `hard-link/sim_data/` | Image used by `SimMMC` |

`SimMMC` is the piece most worth reusing: it lets the entire client stack be exercised
off the instrument.

## Requirements

Python 3, `pymmcore`, `rpyc`, `numpy`, `scikit-image`, `ophyd`, and a local
Micro-Manager 2.0 installation with a device configuration for your scope.

MIT licensed — see [LICENSE](LICENSE).
