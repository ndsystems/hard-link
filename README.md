# Microscope Control System

A Python-based control system for microscopes using Micro-Manager (MMCore) with remote procedure call (RPC) capabilities.

## Overview

This system provides a robust interface for controlling microscope hardware through Micro-Manager, with the following features:

- Remote control capabilities through RPC
- Configurable hardware settings
- Safe hardware initialization and cleanup
- Environment-based configuration management

## Prerequisites

- Python 3.7+
- Micro-Manager 2.0 gamma or later
- Required Python packages:
  - pymmcore
  - rpyc
  - typing

## Installation

1. Clone this repository:
   `git clone <repository-url>`

2. Install the required Python packages:
   `pip install -r requirements.txt`

3. Set up your Micro-Manager installation:
   - Install Micro-Manager in your preferred location
   - Update the `MM_DIR` environment variable or use the default in `configs.py`
   - Place your microscope configuration file in the `mmconfigs` directory or update `MM_CONFIG`

## Configuration

The system can be configured through environment variables or default values in `configs.py`:

- `MM_DIR`: Path to Micro-Manager installation
  - Default: `C:\Program Files\Micro-Manager-2.0gamma`
- `MM_CONFIG`: Path to microscope configuration file
  - Default: `./mmconfigs/Bright_Star.cfg`
- Server settings:
  - Port: 18861
  - Hostname: localhost

## Usage

1. Start the microscope server:
   `python start_server.py`

2. The server will initialize the MMCore instance and wait for client connections

## Error Handling

The system includes robust error handling for:
- MMCore initialization
- Configuration loading
- Directory management
- Hardware connections
- Client connections/disconnections

## Project Structure

- `configs.py`: Configuration management
- `start_server.py`: Main server implementation with MMCore control
- `mmconfigs/`: Directory for microscope configuration files
