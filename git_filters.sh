#!/bin/bash

# filter for the project file: remove last modification timestamp
git config --local filter.kicad_project.clean "sed -E 's/^update=.*$/update=Date/'"
git config --local filter.kicad_project.smudge cat

# filter for the schematics file: remove numbering of power flags because they don't appear in the BOM and kicad renumbers them many times
git config --local filter.kicad_sch.clean "sed -E 's/#(PWR|FLG)[0-9]+/#\1?/'"
git config --local filter.kicad_sch.smudge cat

