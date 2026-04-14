# SPDX-FileCopyrightText: 2026 {{ cookiecutter.author }}
#
# SPDX-License-Identifier: MIT

"""Custom command definitions for {{ cookiecutter.connector_target }} connector."""

# Standard
from enum import StrEnum

# InOrbit
from inorbit_connector.commands import CommandModel, ExcludeUnsetMixin  # noqa: F401


class CustomScripts(StrEnum):
    """Script names for custom commands.

    Values must match the ``filename`` argument in the corresponding ActionDefinition
    in ``cac/actions.yaml``.
    """

    # TODO: Add command names, e.g.:
    # PAUSE_ROBOT = "pauseRobot"
    # RESUME_ROBOT = "resumeRobot"
    pass
