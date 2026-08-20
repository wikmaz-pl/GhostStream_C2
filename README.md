# Wikmaz GhostStream C2 👻
![Version](https://img.shields.io/badge/version-1.6.0-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A stealth, local-first Command & Control (C2) system for sharing highly classified video materials with built-in self-destruction and optional WebRTC reaction capture. Designed for maximum security, zero traces, and automated deployment.

<div align="center">
  <h3>Created & Maintained by <b>Wikmaz</b></h3>
  <a href="https://github.com/wikmaz-pl"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" /></a>
  <a href="https://www.youtube.com/@Wikmazpl"><img src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" /></a>
  <a href="https://wikmaz.pl"><img src="https://img.shields.io/badge/Website-000000?style=for-the-badge&logo=google-chrome&logoColor=white" /></a>
  <br><br>
  <b>☕ Support the Developer / Wspieraj Rozwój Narzędzi:</b><br>
  <a href="https://ko-fi.com/wikmaz"><img src="https://ko-fi.com/img/githubbutton_sm.svg" height="36"></a>
  <a href="https://suppi.pl/wikmaz"><img src="https://img.shields.io/badge/🍕_Suppi-Wsparcie-FF5E5B?style=for-the-badge" height="36"></a>
</div>

---

## 💻 System Requirements / Wymagania Systemowe

| Requirement | Version / Details | Notes |
| :--- | :--- | :--- |
| **Python** | `3.11` (Strictly Recommended) | Ensure Python is added to system PATH. |
| **Dependencies** | `Flask`, `PyInstaller` | Automatically installed via compile script. |
| **Tools** | `FFmpeg` | Required for video optimization/compression. Must be in PATH. |
| **GitHub CLI** | `gh` | Required for automated GitHub Deployment & Releases. |

---

## 🚀 How to Run / Instrukcja Uruchomienia

### Opcja 1: Szybki Start (Gotowy plik EXE) / Quick Start
1. Go to the **Releases** tab on the right side of this GitHub page.
2. Download `GhostStream_C2_Release.zip`.
3. Extract the ZIP file.
4. Run `Wikmaz_GhostStream_C2.exe`. The application will automatically build its internal folder structure.

### Opcja 2: Kompilacja ze Źródeł / Build from Source
Jeśli chcesz samodzielnie zbudować aplikację z kodu źródłowego:
1. Skopiuj to repozytorium na swój dysk.
2. Uruchom plik `1_Compile_to_EXE.bat`.
3. Skrypt automatycznie utworzy wirtualne środowisko (VENV), pobierze *Flask* oraz *PyInstaller*, skompiluje projekt i stworzy gotową paczkę `GhostStream_C2_Release.zip`!

---

## ⚙️ Features / Główne Funkcje
* **In-Memory Stream Proxy:** Wideo nie jest cachowane, ulega autodestrukcji po odtworzeniu.
* **Auto-Language (i18n):** Automatycznie dostosowuje interfejs (EN/PL) do przeglądarki celu.
* **Zero-Config Cloudflare Tunnel:** Generuje publiczny link `https` omijając NAT/Firewall.
* **Granular Surveillance:** Opcjonalne wymuszanie dostępu do kamery dla wygenerowanych haseł.
* **FFmpeg Optymalization:** Kompresja wideo do 480p/720p z flagą `+faststart` dla słabych łącz.

---
*For business inquiries and contact: admin@softhause.wikmaz.pl*
