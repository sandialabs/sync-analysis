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

### Network Monitor (`network-monitor`)
Provides monitoring and observability for the distributed ledger network using Prometheus and Grafana.

**Features:**
- Real-time network metrics collection
- Grafana dashboard for visualization
- Prometheus-based data storage
- Docker-based monitoring stack

### Social Agent (`social-agent`)
Simulates social agents that interact with the ledger system, generating realistic network traffic and transaction patterns.

**Features:**
- Configurable agent connectivity and activity levels
- Variable agent population sizes
- Peer-to-peer communication
- Realistic social interaction patterns

## Quick Start

Run a basic experiment with 4 journals and 4 agents running at periodicity 2 (i.e. 2^2 = 4 seconds between blocks), each with network monitoring, 2 outgoing peers and 32 key-value pairs per node, and an activity level of 0 (i.e., 0^2 = 1 read/write per period).

```bash
firewheel experiment -r synchronic_web.ledger_journal:4:2 synchronic_web.network_monitor synchronic_web.social_agent:2:32:0 control_network minimega.launch
```

### Accessing the Monitoring Dashboard

To access the Grafana monitoring dashboard:

1. Set up port forwarding to the monitor node:
   ```bash
   firewheel ssh -L 3000:localhost:3000 monitor.net
   ```

2. Open your browser and navigate to `http://localhost:3000` to view the Grafana dashboard.

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
firewheel experiment -r synchronic_web.ledger_journal:2:2 synchronic_web.network_monitor synchronic_web.social_agent:1:16:0 control_network minimega.launch
```

### Medium Scale Simulation
```bash
firewheel experiment -r synchronic_web.ledger_journal:8:2 synchronic_web.network_monitor synchronic_web.social_agent:4:64:1 control_network minimega.launch
```

### Large Scale Deployment
```bash
firewheel experiment -r synchronic_web.ledger_journal:16:2 synchronic_web.network_monitor synchronic_web.social_agent:8:128:2 control_network minimega.launch
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
