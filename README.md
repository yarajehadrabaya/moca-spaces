# Hybrid Explainable AI MoCA System (Arabic)

This repository contains the modular implementation of a hybrid AI-assisted scoring system for the Arabic Montreal Cognitive Assessment (MoCA).

Each module corresponds to a cognitive domain and is deployed as an independent Hugging Face Space.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22983116.svg)](https://doi.org/10.5281/zenodo.22983116)

## Archived Release

The validated `v1.0.0` code release is archived on Zenodo:

**DOI:** [10.5281/zenodo.22983116](https://doi.org/10.5281/zenodo.22983116)

---

## 🧠 System Modules

| Module | Description |
|--------|-------------|
| moca-memory-test | Hybrid deterministic + LLM scoring for delayed recall |
| moca-attention-test | Rule-based scoring for attention tasks |
| moca-fluency-test | Deterministic lexical processing for verbal fluency |
| moca-language-test | LLM-assisted naming and sentence repetition |
| moca-abstraction-test | Constrained semantic similarity evaluation |
| moca-orientation-test | Deterministic rule-based orientation scoring |
| moca-vision-test | Computer vision analysis for visuospatial tasks |

---

## ⚙️ Architecture

The system follows a hybrid explainable AI design:

- Deterministic rule-based scoring for objective tasks
- Computer vision for drawing analysis
- Constrained large language model reasoning for semantic tasks
- Safety override mechanisms
- Domain-level score traceability

---

## 📦 Deployment

Each module is implemented using:

- FastAPI
- Python
- OpenCV (vision tasks)
- Qwen2.5-7B-Instruct (LLM tasks)

---

## 🔒 Data Privacy

No personal data are stored in this repository. All participant data were anonymized prior to analysis.

---

## 🎓 Research Context

Developed as part of a clinical validation study on AI-assisted cognitive screening for Arabic-speaking populations.

---

## 🔐 Configuration

The language, memory, abstraction, attention, orientation, and vision modules
use Hugging Face Inference API access. Set the `HF_TOKEN` environment variable
in each deployment environment; do not commit tokens or `.env` files.

## 📄 License

Unless otherwise stated, the source code and documentation in this repository
are licensed under the **Creative Commons Attribution 4.0 International License
(CC BY 4.0)**. You may share and adapt the material with appropriate credit, a
link to the license, and an indication of changes.

License: https://creativecommons.org/licenses/by/4.0/

## Citation

If you use this code in academic research, please cite:

> Hybrid Explainable AI MoCA System (Arabic) (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.22983116

