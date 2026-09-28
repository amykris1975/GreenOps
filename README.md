<div align="center">

![GreenOps Banner](https://capsule-render.vercel.app/api?type=waving&color=00b894&height=200&section=header&text=GreenOps%20Enterprise&fontSize=70&animation=fadeIn&fontAlignY=35&desc=AI-Powered%20Sustainable%20DevOps&descAlignY=55&descAlign=50)

# 🌿 GreenOps Enterprise

[![Gemini API](https://img.shields.io/badge/AI-Gemini%20API-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)
[![Carbon API](https://img.shields.io/badge/Data-UK%20National%20Grid-00b894?style=for-the-badge&logo=leaf&logoColor=white)](https://carbonintensity.org.uk/)
[![Python](https://img.shields.io/badge/Code-Python%203.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>


## Overview

**GreenOps** is an autonomous AI agent that optimizes cloud deployments based on real-time carbon intensity. Instead of deploying blindly, it checks the grid status and intelligently schedules workloads for "green windows"—reducing carbon emissions by up to **40%**.

### **Powered By**
*    **Google Gemini API**: The reasoning engine that decides *when* to deploy. Model selection is explicit runtime configuration, not a committed secret or hard-coded project setting.
*    **UK National Grid Carbon Intensity API**: Real-time energy generation data (Wind, Solar, Gas, Coal).



## Want to Run Locally?

A dedicated local execution mode for testing on your laptop is here!!

 **[Click Here for Local Setup Guide](Local/README.md)**

## Secure Gemini Configuration

1. Copy [`.env.example`](.env.example) for local reference only; never commit a real `.env` or paste a key into a notebook, shell transcript, issue, PR, or screenshot.
2. Provide `GEMINI_API_KEY` through the approved secret manager or runtime environment. `GOOGLE_API_KEY` is supported only as a backwards-compatible fallback.
3. Set `GREENOPS_GEMINI_MODEL` only if you need to override the template's model preference. The selected model must be enabled for the key's Google AI Studio project.
4. Run `python -m unittest discover -s tests -v` before enabling live requests.

The [Gemini integration handoff for Caleb McCombs](docs/gemini-handoff-for-caleb-mccombs.md) records the security, review, and collaboration boundaries for this change. It does not grant repository access or imply an affiliation.

## Deterministic Release Controls

GreenOps uses Gemini for explanations and recommendations, not for approval or execution authority. The repository's [deterministic systems check](docs/deterministic-systems-check.md) defines a fail-closed carbon gate, controlled emergency overrides, and the required human review evidence. The scheduled GitHub workflow validates those invariants before it permits the test matrix to run.


---

## The Problem vs. Solution

### **The Problem: Invisible Carbon**
*   Cloud computing emits **more carbon than the airline industry**.
*   Deploying a heavy job at **6 PM (Coal/Gas)** = **300g CO2/kWh**.
*   Deploying the same job at **2 AM (Wind)** = **<50g CO2/kWh**.
*   Most DevOps tools **ignore this completely**.

### **The Solution: Autonomous Agent**
GreenOps acts as a "Sustainability Gatekeeper":
1.  **Intercepts** deployment requests.
2.  **Checks** live grid data via API.
3.  **Decides**:
    *   ✅ **Green Grid?** Deploy immediately.
    *   🏭 **Dirty Grid?** Schedule for later (e.g., 3 AM).
    *   🚨 **Critical Emergency?** Override and deploy instantly.

---

##  Architecture

<img width="1112" height="567" alt="Image" src="https://github.com/user-attachments/assets/3149f53b-72d1-4f96-ab9e-e28c93ba7d2e" />


## Process Flow

<img width="2724" height="423" alt="Image" src="https://github.com/user-attachments/assets/a103340d-71bd-44d4-a0d4-5f938ad2b371" />

---

## Real-World Scenarios

| Scenario | Grid Status | Agent Decision | Impact |
|:---|:---|:---|:---|
| **Nightly Build** |  Dirty (Gas) | **Wait 6 hours** for Wind peak | **-84% Carbon** |
| **Security Hotfix** |  Dirty (Gas) | **Deploy Immediately** (Critical) |  **Safety First** |
| **Data Migration** |  Moderate | **Wait 22 hours** for Solar peak |  **Human Choice** |




## Acknowledgments
Built for the **Google AI Agents Hackathon** (November 2025).

*   **LLM**: Gemini API (runtime-selected model)
*   **Data**: Carbon Intensity API (National Grid ESO)



##  Future Improvement

We are building the future of sustainable DevOps. Here is what's coming next:

- [ ] **Kubernetes Operator**: A K8s controller to auto-schedule pods based on node carbon intensity.
- [ ] **Multi-Region Arbitrage**: "Follow the Wind" routing—moving workloads from UK (calm) to Spain (windy) automatically.
- [ ] **Hardware Awareness**: Integration with NVIDIA MIG to throttle GPU power during dirty grid windows.
- [ ] **CI/CD Plugins**: Native plugins for GitHub Actions and GitLab CI.


## 🤝 How to Contribute

We welcome contributions from the community! Whether it's fixing bugs, adding new features, or improving documentation.

1.  **Fork** the repository.
2.  **Create a Branch**: `git checkout -b feature/AmazingFeature`.
3.  **Commit** your changes: `git commit -m 'Add some AmazingFeature'`.
4.  **Push** to the branch: `git push origin feature/AmazingFeature`.
5.  **Open a Pull Request**.

### **Ideas for Contribution**
*   Add support for other grid APIs (e.g., ElectricityMaps, WattTime).
*   Create a Docker container for the agent.
*   Improve the visualization dashboard.



## License
Distributed under the [License](LICENSE)  See for more information.

---

<div align="center">

**Code Smarter. Breathe Easier.** 🌿

</div>
