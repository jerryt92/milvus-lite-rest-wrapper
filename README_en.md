[简体中文](README.md) | English

# Milvus Lite REST Wrapper Project Description

## Project Overview
**milvus-lite-rest-wrapper** is a project that provides a RESTful API wrapper for Milvus Lite, designed to offer a lightweight local vector database solution.

## Project Features
- **Lightweight**: Based on milvus-lite to achieve local operation
- **RESTful API**: Provides standard REST interfaces to access Milvus functionality
- **Local Storage**: Supports local database file storage

## Dependencies
The project depends on the milvus-lite project, which is a lightweight version of Milvus specifically designed for local and edge deployments.

## Windows Users
**Milvus Lite does not support Windows** (no Windows wheels on PyPI). To run this project on Windows, use one of these options:
- **WSL2**: Install Windows Subsystem for Linux and run this project inside WSL.
- **Docker**: Run Milvus Standalone in a container and connect via URI.
- **Remote instance**: Use Milvus Standalone or Zilliz Cloud and connect to a remote server.

## Use Cases
- Suitable for scenarios requiring vector search functionality without deploying a full Milvus cluster
- Local development and testing environments
- Lightweight embedded vector database applications

## Advantages of Local Operation
- No complex server deployment required
- Low resource consumption
- Fast startup and response
- Suitable for single-machine application scenarios

This project provides an excellent solution for developers who need vector database functionality while pursuing lightweight and local deployment options.

## Acknowledgements

The project depends on the [milvus-lite](https://github.com/milvus-io/milvus-lite) project, thanks to the contributions of the Milvus team.