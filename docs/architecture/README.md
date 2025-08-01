# Architecture Documentation

## Overview
This directory contains architectural documentation for the Serverless Presentation Generator.

## Contents
- System Architecture
- Component Diagrams
- Data Flow Diagrams
- Decision Records

## Architecture Principles

### Clean Architecture
The project follows clean architecture principles with clear separation of concerns:

- **Core Layer**: Business entities, use cases, and interfaces
- **Application Layer**: Handlers, services, and DTOs
- **Infrastructure Layer**: External services and persistence
- **Presentation Layer**: API controllers and serializers

### Dependency Inversion
Dependencies point inward toward the core business logic. External dependencies are injected through interfaces.

### Separation of Concerns
Each layer has a single responsibility and clear boundaries.
