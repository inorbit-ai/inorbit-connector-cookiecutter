# SPDX-FileCopyrightText: 2026 {{ cookiecutter.author }}
#
# SPDX-License-Identifier: MIT

"""Configuration models for {{ cookiecutter.connector_target }} connector."""

# Third Party
from pydantic import model_validator

# InOrbit
from inorbit_connector.models import ConnectorRootConfig, ConnectorSpecificConfig, RobotConfig

CONNECTOR_TYPE = "{{cookiecutter.connector_slug}}"


class {{cookiecutter.connector_slug_pascal}}RobotConfig(RobotConfig):
    """Robot configuration with {{ cookiecutter.connector_target }}-specific fields.

    Extends base RobotConfig to include Fleet robot ID.

    Attributes:
        robot_id (str): InOrbit robot ID
        fleet_robot_id (int): Robot ID in {{ cookiecutter.connector_target }}
        cameras (list): Camera configurations (inherited)
    """

    fleet_robot_id: int


class {{cookiecutter.connector_slug_pascal}}Config(ConnectorSpecificConfig):
    """Custom configuration fields for {{ cookiecutter.connector_target }} connector.

    These are fleet-wide settings shared by all robots.

    Attributes:
        fleet_host (str): Fleet server IP or hostname
        fleet_port (int): Fleet server port
        fleet_username (str): Fleet API username
        fleet_password (str): Fleet API password
    """

    CONNECTOR_TYPE = CONNECTOR_TYPE

    fleet_host: str
    fleet_port: int = 80
    fleet_username: str
    fleet_password: str
    # Optional field examples:
    # log_level: str | None = None
    # timeout_seconds: int | None = None


class {{cookiecutter.connector_slug_pascal}}ConnectorConfig(ConnectorRootConfig[{{cookiecutter.connector_slug_pascal}}Config]):
    """Configuration for {{ cookiecutter.connector_target }} connector.

    Inherits from ConnectorRootConfig and adds {{cookiecutter.connector_target}}-specific fields.

    Attributes:
        fleet (list[{{cookiecutter.connector_slug_pascal}}RobotConfig]): List of robot configurations
    """

    fleet: list[{{cookiecutter.connector_slug_pascal}}RobotConfig]  # type: ignore[assignment]

    @model_validator(mode="after")
    def validate_unique_fleet_robot_ids(self) -> "{{cookiecutter.connector_slug_pascal}}ConnectorConfig":
        """Validate that fleet_robot_id values are unique across the fleet.

        Returns:
            {{cookiecutter.connector_slug_pascal}}ConnectorConfig: The validated configuration

        Raises:
            ValueError: If fleet_robot_id values are not unique
        """
        fleet_ids = [robot.fleet_robot_id for robot in self.fleet]
        if len(fleet_ids) != len(set(fleet_ids)):
            raise ValueError("fleet_robot_id values must be unique")
        return self
