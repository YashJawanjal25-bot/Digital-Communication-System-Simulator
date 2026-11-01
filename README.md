# 📡 Digital Communication System Simulator

An interactive **Digital Communication System Simulator** built using Python and Streamlit. It simulates a baseband digital communication link using Gray-coded **BPSK, QPSK, and 16-QAM** modulation over an Additive White Gaussian Noise (AWGN) channel.

The project performs Monte Carlo simulations, calculates Bit Error Rate (BER), compares simulated results with theoretical BER curves, and visualizes signal constellation diagrams.

🚀 **Live Demo:** [Add your Streamlit App URL here]

## ✨ Features

- **Multiple Modulation Techniques:** BPSK, QPSK, and 16-QAM.
- **AWGN Channel:** Simulates noise effects on transmitted signals.
- **Interactive Simulation:** Adjust Eb/N0, target errors, and simulation bit limits.
- **BER Analysis:** Compare simulated and theoretical BER.
- **Interactive BER Graphs:** Visualize BER versus Eb/N0 using Plotly.
- **Constellation Visualization:** Compare ideal and noisy constellation points.
- **Signal Analysis:** Compare transmitted and received binary data.
- **CSV Export:** Download BER simulation results.
- **Monte Carlo Simulation:** Evaluate communication system performance.

## 🛠️ Technologies Used

- Python
- NumPy
- SciPy
- Pandas
- Matplotlib
- Plotly
- Streamlit

## 📊 Modulation Techniques

| Technique | Bits per Symbol | Constellation |
|---|---:|---|
| BPSK | 1 | 2 points |
| QPSK | 2 | 4 points |
| 16-QAM | 4 | 16 points |

All modulation schemes use Gray coding and normalized unit average symbol energy.

## 📖 Theory

**Transmitter:** Random binary data is generated and mapped into complex modulation symbols.

**Channel:** The AWGN channel adds Gaussian noise based on the selected Eb/N0 value.

**Receiver:** Hard-decision minimum-Euclidean-distance detection recovers the transmitted bits.

**Bit Error Rate:**

BER = Number of bit errors / Total transmitted bits

### Theoretical BER Expressions

- BPSK: Pb = Q(√(2 × Eb/N0))
- QPSK: Pb = Q(√(2 × Eb/N0))
- 16-QAM: Pb ≈ (3/8) × erfc(√(0.4 × Eb/N0))

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd YOUR_REPOSITORY_NAME
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch the Streamlit application

```bash
streamlit run app.py
```

### 4. Run the original simulation

```bash
python run_simulation.py
```

The original simulation generates:

- `results/ber_vs_snr.png`
- `results/constellations.png`
- `results/verification.txt`

## 📁 Project Structure

```text
Digital-Communication-System-Simulator/
│
├── app.py
├── run_simulation.py
├── requirements.txt
├── README.md
│
├── digital_comm_sim/
│   ├── __init__.py
│   ├── bits.py
│   ├── channel.py
│   ├── modulation.py
│   ├── simulate.py
│   ├── plots.py
│   └── theory.py
│
└── results/
```

## 📈 Simulation Results

The Monte Carlo simulation evaluates BER over an Eb/N0 range of 0–10 dB and compares the results with theoretical reference curves.

| Eb/N0 (dB) | BPSK Simulated | QPSK Simulated | 16-QAM Simulated |
|---:|---:|---:|---:|
| 0 | 7.78e-02 | 7.79e-02 | 1.41e-01 |
| 5 | 5.94e-03 | 5.69e-03 | 4.13e-02 |
| 10 | 3.60e-06 | 3.40e-06 | 1.86e-03 |

Results demonstrate that BER decreases as Eb/N0 increases. Gray-coded QPSK has approximately the same theoretical bit-error performance as BPSK, while 16-QAM offers higher spectral efficiency with greater noise sensitivity.

## ☁️ Deployment

The interactive application can be deployed using **Streamlit Community Cloud**.

1. Push the project to GitHub.
2. Connect your GitHub repository to Streamlit Community Cloud.
3. Select `app.py` as the main application file.
4. Deploy and access the application through its public URL.

## 🔮 Future Improvements

- Soft-decision decoding and Log-Likelihood Ratios (LLRs).
- Rayleigh and Rician fading channels.
- Forward Error Correction using convolutional and LDPC codes.
- Higher-order modulation such as 64-QAM and 256-QAM.
- Pulse shaping and matched filtering.
- Eye diagram and signal spectrum visualization.

## 👨‍💻 Author

Developed as an Electrical and Electronics / Electronics and Telecommunication engineering portfolio project to explore digital modulation, communication channels, and BER performance analysis.

---

**If you find this project useful, consider giving it a ⭐ on GitHub!**
