# Simulation of the analog front-end

This directory contains a simulation of the analog front end. The different configurations of the analog front end can be selected by switching the two parameters for the resistors, which are being used in combination with the analog multiplexer.

## Running the Simulation

The simulation ca be run with ngspice from the command line by calling:

```bash
ngspice analog_frontend.cir
```

If you want to exit ngspice, you can do so by typing `exit` or pressing `Ctrl+D`.
