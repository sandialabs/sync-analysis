# FIREWHEEL Model Components

This directory contains FIREWHEEL model components for simulating distributed ledger systems with social agents.

## Components

### Ledger Journal (`ledger-journal`)
A distributed ledger component that provides journaling capabilities for tracking transactions and state changes across the network.

**Features:**
- Configurable periodicity for journal updates
- Server and desktop deployment modes
- Docker-based containerization
- Network peering capabilities

### Social Agent (`social-agent`)
Simulates social agents that interact with the ledger system, generating realistic network traffic and transaction patterns.

**Features:**
- Configurable agent connectivity and activity levels
- Variable agent population sizes
- Peer-to-peer communication
- Realistic social interaction patterns

## Quick Start

Run a basic experiment with 4 journal nodes, 2 agent routers, 2 social agents with size 32 and activity level 0:

```bash
firewheel experiment -r synchronic_web.ledger_topology:4:2 synchronic_web.social_agent:2:32:0 control_network minimega.launch
```

## Parameter Reference

### Ledger Topology Parameters
- **Number of nodes**: Total journal nodes in the network
- **Periodicity**: Update frequency for journal synchronization

### Social Agent Parameters
- **Connectivity**: Number of peer connections per agent
- **Size**: Agent population size
- **Activity**: Activity level (0 = low, higher values = more active)

## Example Configurations

### Small Test Environment
```bash
firewheel experiment -r synchronic_web.ledger_topology:2:1 synchronic_web.social_agent:1:16:0 control_network minimega.launch
```

### Medium Scale Simulation
```bash
firewheel experiment -r synchronic_web.ledger_topology:8:4 synchronic_web.social_agent:4:64:1 control_network minimega.launch
```

### Large Scale Deployment
```bash
firewheel experiment -r synchronic_web.ledger_topology:16:8 synchronic_web.social_agent:8:128:2 control_network minimega.launch
```

## Requirements

- FIREWHEEL framework
- Docker support
- Ubuntu 22.04 base images
- Sufficient system resources for containerized workloads

## Architecture

The simulation creates a network topology with:
- Journal nodes running distributed ledger services
- Social agents generating transaction patterns
- Router infrastructure connecting components
- Control network for experiment management
