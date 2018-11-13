"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2018 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""

import argparse
import sys


def parse(*, running_from_bundle, app="capture", port=None, **kwargs):
    parser = argparse.ArgumentParser()

    # Caveat: We need explicit defaults for app+port arguments in order to maintain
    #         the convenience to start Capture without having to pass any explicit
    #         arguments, e.g. `python3 main.py` instead of `python3 main.py capture`.
    target_ns = argparse.Namespace()
    target_ns.app = app
    target_ns.port = port
    target_ns.running_from_bundle = running_from_bundle

    if kwargs:
        target_ns.__dict__.update(kwargs)

    if target_ns.running_from_bundle:
        _setup_bundle_parsers(parser, namespace=target_ns)
    else:
        _setup_source_parsers(parser)
    _add_debug_profile_args(parser)

    return parser.parse_args(namespace=target_ns)


def _setup_source_parsers(main_parser):
    subparsers = main_parser.add_subparsers(
        title="Applications",
        description="Select which application you want to run, by default `capture`",
        dest="app",
    )
    parser_capture = subparsers.add_parser(
        "capture", help="Real-time processing and recording"
    )
    _add_remote_port_arg(parser_capture)

    parser_service = subparsers.add_parser("service", help="VR/AR interface")
    _add_remote_port_arg(parser_service)

    parser_player = subparsers.add_parser(
        "player", help="Process, visualize, and export recordings"
    )
    _add_recording_arg(parser_player)


def _setup_bundle_parsers(main_parser, namespace):
    if "pupil_player" in sys.executable:
        _add_recording_arg(main_parser)
        namespace.app = "player"
    else:
        _add_remote_port_arg(main_parser)
        if "pupil_capture" in sys.executable:
            namespace.app = "capture"
        else:
            namespace.app = "service"


def _add_remote_port_arg(parser):
    parser.add_argument("-P", "--port", type=int, help="Pupil Remote port")


def _add_recording_arg(parser):
    parser.add_argument("recording", nargs="?", help="path to recording")


def _add_debug_profile_args(parser):
    parser.add_argument(
        "--debug", help="display debug log messages", action="store_true"
    )
    parser.add_argument(
        "--profile", action="store_true", help="profile the application's CPU time"
    )


if __name__ == "__main__":
    args = parse(running_from_bundle=False)
    print(args)
