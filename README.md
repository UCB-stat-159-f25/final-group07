[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/sSkqmNLf)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/UCB-stat-159-f25/final-group07/HEAD?urlpath=%2Fdoc%2Ftree%2Fmain.ipynb)

Link to MyST Deployment: [MyST Deployment](https://ucb-stat-159-f25.github.io/final-group07/)

# TIMS Fatal Crash Analysis

## Overview & Motivation
This project analyzes **TIMS (Traffic Information Management System) data** related to **fatal traffic crashes**. The motivation behind this project is to better understand patterns and trends in fatal crashes, with a particular emphasis on **geographical clustering**. Identifying spatial patterns can help highlight high-risk locations and support traffic safety planning and policy decision-making.

---

## Analysis Conducted
The analysis in this project includes:
- Data cleaning and preprocessing of TIMS fatal crash data
- Exploratory analysis of crash trends and characteristics
- Geographic and spatial clustering to identify high-risk areas
- Visualization of fatal crash locations and spatial patterns

All analysis is performed using reproducible Jupyter notebooks.

---

## Running the Analysis

### Execute All Notebooks

To run the full analysis pipeline from scratch:

```bash
make all
```

This installs the local project package and executes all Jupyter notebooks.

---

### Build HTML Documentation

To generate the HTML report using MyST:

```bash
make html
```

The output will be available in the `_build/` directory.

---

## Cleaning Generated Files

Remove all generated outputs and build artifacts:

```bash
make clean
```
---

## Automation & Help

To view all available Makefile commands:

```bash
make help
```
---

## Requirements
- Conda
- Bash-compatible shell
- MyST for HTML documentation generation

---

## Notes
This project is designed for reproducible, automated data analysis using Conda, Make, and Jupyter notebooks.
