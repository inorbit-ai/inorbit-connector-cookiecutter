# SPDX-FileCopyrightText: 2026 {{ cookiecutter.author }}
#
# SPDX-License-Identifier: MIT

"""{{ cookiecutter.connector_target }} multi-robot connector for InOrbit."""

# Standard
from typing import override

# InOrbit
from inorbit_connector.commands import CommandFailure, parse_custom_command_args
from inorbit_connector.connector import (
    CommandResultCode,
    FleetConnector,
)
from inorbit_connector.models import MapConfigTemp
from inorbit_edge.robot import COMMAND_CUSTOM_COMMAND

# Local
from {{cookiecutter.connector_slug}}_connector import __version__ as connector_version
from {{cookiecutter.connector_slug}}_connector.src.config.models import {{cookiecutter.connector_slug_pascal}}ConnectorConfig


class {{cookiecutter.connector_slug_pascal}}Connector(FleetConnector):
    """Connector between {{ cookiecutter.connector_target }} and InOrbit.

    Inherits from FleetConnector and implements {{ cookiecutter.connector_target }}-specific logic.
    """

    def __init__(self, config: {{cookiecutter.connector_slug_pascal}}ConnectorConfig) -> None:
        """Initialize the connector.

        Args:
            config: {{ cookiecutter.connector_target }} connector configuration
        """
        super().__init__(
            config,
            register_user_scripts=True,
            create_user_scripts_dir=True,
            publish_connector_system_stats=True,
        )

        self._logger.info("Initialized {{ cookiecutter.connector_target }} Connector")

    @override
    async def _connect(self) -> None:
        """Connect to {{ cookiecutter.connector_target }} API and start polling."""
        self._logger.info("Connected to {{ cookiecutter.connector_target }} API")

    @override
    async def _disconnect(self) -> None:
        """Disconnect from {{ cookiecutter.connector_target }} API and stop polling."""
        self._logger.info("Disconnected from {{ cookiecutter.connector_target }} API")

    @override
    async def _execution_loop(self) -> None:
        """Main execution loop - publish cached robot data to InOrbit."""
        for robot_id in self.robot_ids:
            self.publish_robot_key_values(robot_id, {
                "connector_version": connector_version,
            })
        self._logger.debug("Executing main execution loop")

    @override
    async def _inorbit_robot_command_handler(
        self, robot_id: str, command_name: str, args: list, options: dict
    ) -> None:
        """Handle InOrbit commands for a specific robot.

        Validation and parsing of command arguments is handled by the CommandModel classes.
        If the arguments are invalid, a CommandFailure will be raised and the error will be
        handled accordingly and logged as an error.

        Args:
            robot_id: Robot ID that received the command
            command_name: Name of the command
            args: Command arguments
            options: Command options including result_function
        """
        self._logger.debug(
            f"Received command '{command_name}' for robot '{robot_id}'\n"
            f"  Args: {args}\n"
            f"  Options: {options}"
        )

        result_fn = options["result_function"]

        if command_name == COMMAND_CUSTOM_COMMAND:
            script_name, script_args = parse_custom_command_args(args)
            # TODO: Import CustomScripts from .commands and add cases here
            match script_name:
                case _:
                    raise CommandFailure(
                        execution_status_details=f"Unknown command: {script_name}",
                        stderr=f"Command '{script_name}' is not supported",
                    )

        result_fn(CommandResultCode.SUCCESS)

    @override
    async def fetch_robot_map(
        self, robot_id: str, frame_id: str
    ) -> MapConfigTemp | None:
        """Fetch a map from the {{ cookiecutter.connector_target }} API.

        This method is called automatically by the base class when a pose is published
        with a frame_id that doesn't have a pre-configured map.

        Args:
            robot_id: Robot ID requesting the map
            frame_id: Frame ID of the map to fetch

        Returns:
            MapConfigTemp with map data, or None if fetch fails
        """
        self._logger.info(f"Fetching map '{frame_id}' for robot '{robot_id}'")

        try:
            # Fetch the map

            return MapConfigTemp(
                image=bytes(),
                map_id=frame_id,
                map_label="",
                origin_x=0.0,
                origin_y=0.0,
                resolution=0.0,
            )

        except Exception as ex:
            self._logger.error(
                f"Failed to fetch map '{frame_id}' from {{ cookiecutter.connector_target }} API: {ex}"
            )
            return None
