
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from simulate import simulate_ber, sweep
from modulation import BITS_PER_SYMBOL, get_constellation, modulate
from channel import awgn
from theory import THEORY
from bits import generate_bits

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Digital Communication Simulator",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Digital Communication System Simulator")
st.caption("Interactive simulation of digital modulation over an AWGN channel")

# ---------------- SIDEBAR ----------------

st.sidebar.header("Simulation Settings")

schemes = {
    "BPSK": "BPSK",
    "QPSK": "QPSK",
    "16-QAM": "QAM16"
}

selected_name = st.sidebar.selectbox(
    "Select Modulation Technique",
    list(schemes.keys())
)

scheme = schemes[selected_name]

snr = st.sidebar.slider(
    "Eb/N0 (dB)",
    min_value=0,
    max_value=20,
    value=8
)

max_bits = st.sidebar.select_slider(
    "Maximum Number of Bits",
    options=[20000, 50000, 100000, 200000, 500000, 1000000],
    value=200000,
    format_func=lambda x: f"{x:,}"
)

target_errors = st.sidebar.slider(
    "Target Errors",
    min_value=10,
    max_value=200,
    value=100,
    step=10
)

st.sidebar.info(
    "Channel: AWGN\n\n"
    "Detection: Hard Decision\n\n"
    "Constellation: Gray-coded"
)


# ---------------- SINGLE POINT SIMULATION ----------------

@st.cache_data(show_spinner=False)
def run_single_simulation(scheme, snr, target_errors, max_bits):
    return simulate_ber(
        scheme,
        float(snr),
        target_errors=target_errors,
        max_bits=max_bits,
        seed=1234
    )


@st.cache_data(show_spinner=False)
def run_ber_sweep(scheme, target_errors, max_bits, step):
    eb_values = np.arange(0, 20 + step, step, dtype=float)

    result = sweep(
        scheme,
        eb_values,
        target_errors=target_errors,
        max_bits=max_bits
    )

    return result


@st.cache_data(show_spinner=False)
def run_constellation(scheme, snr, n_symbols=2000):
    symbols, labels = get_constellation(scheme)
    k = BITS_PER_SYMBOL[scheme]

    bits = generate_bits(n_symbols * k, seed=7)
    tx = modulate(bits, scheme)
    rx = awgn(tx, float(snr), k, seed=8)

    return (
        symbols.real,
        symbols.imag,
        rx.real,
        rx.imag
    )


# ---------------- TABS ----------------

tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Overview",
    "📊 BER Analysis",
    "⭐ Constellation",
    "📡 Signal Analysis"
])


# ---------------- TAB 1 ----------------

with tab1:

    st.subheader("Simulation Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric("Modulation", selected_name)
    col2.metric("Eb/N0", f"{snr} dB")
    col3.metric("Channel", "AWGN")

    st.divider()

    st.markdown("### Digital Communication Process")

    st.markdown("""
    **Transmitter → Modulator → AWGN Channel → Demodulator → Receiver**

    1. Generate random binary data.
    2. Convert bits into digital modulation symbols.
    3. Transmit through a noisy AWGN channel.
    4. Recover the transmitted bits using demodulation.
    5. Calculate Bit Error Rate (BER).
    """)

    st.info(
        "Select the modulation technique and simulation settings "
        "from the sidebar, then run the simulation below."
    )

    if st.button("🚀 Run Simulation", type="primary", use_container_width=True):

        with st.spinner("Running Monte Carlo simulation..."):

            ber, errors, bits = run_single_simulation(
                scheme, snr, target_errors, max_bits
            )

            theory_ber = float(THEORY[scheme](snr))

            st.session_state["single_result"] = {
                "scheme": scheme,
                "snr": snr,
                "ber": ber,
                "errors": errors,
                "bits": bits,
                "theory": theory_ber
            }

    if "single_result" in st.session_state:

        result = st.session_state["single_result"]

        if result["scheme"] == scheme and result["snr"] == snr:

            st.divider()
            st.subheader("Simulation Results")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Simulated BER", f'{result["ber"]:.3e}')
            c2.metric("Theoretical BER", f'{result["theory"]:.3e}')
            c3.metric("Bit Errors", f'{result["errors"]:,}')
            c4.metric("Bits Simulated", f'{result["bits"]:,}')

            st.success("Simulation completed successfully.")


# ---------------- TAB 2 ----------------

with tab2:

    st.subheader("BER vs Eb/N0 Performance Analysis")

    st.write(
        "Compare simulated BER against theoretical BER "
        "for the selected modulation technique."
    )

    step = st.selectbox(
        "SNR Step Size",
        [1, 2, 5],
        index=1,
        format_func=lambda x: f"{x} dB"
    )

    if st.button("📈 Generate BER Curve", type="primary"):

        with st.spinner("Calculating BER across SNR values..."):

            result = run_ber_sweep(
                scheme, target_errors, max_bits, step
            )

            st.session_state["ber_result"] = result
            st.session_state["ber_scheme"] = scheme

    if (
        "ber_result" in st.session_state
        and st.session_state["ber_scheme"] == scheme
    ):

        result = st.session_state["ber_result"]

        eb = result["eb_n0_db"]
        simulated = result["ber"]
        theoretical = THEORY[scheme](eb)

        fig = go.Figure()

        valid = simulated > 0

        fig.add_trace(go.Scatter(
            x=eb[valid],
            y=simulated[valid],
            mode="lines+markers",
            name="Simulated BER"
        ))

        fig.add_trace(go.Scatter(
            x=eb,
            y=theoretical,
            mode="lines",
            name="Theoretical BER",
            line=dict(dash="dash")
        ))

        fig.update_layout(
            title=f"{scheme}: BER vs Eb/N0",
            xaxis_title="Eb/N0 (dB)",
            yaxis_title="Bit Error Rate",
            yaxis_type="log",
            template="plotly_white",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### BER Results Table")

        df = pd.DataFrame({
            "Eb/N0 (dB)": eb,
            "Simulated BER": simulated,
            "Theoretical BER": theoretical,
            "Errors": result["errors"],
            "Bits Simulated": result["bits"]
        })

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "⬇️ Download BER Results CSV",
            data=df.to_csv(index=False),
            file_name=f"{scheme}_BER_results.csv",
            mime="text/csv"
        )

    else:
        st.info("Click Generate BER Curve to calculate performance.")


# ---------------- TAB 3 ----------------

with tab3:

    st.subheader("Signal Constellation Diagram")

    st.write(
        "Observe how noise affects transmitted constellation points."
    )

    if st.button("Generate Constellation", type="primary"):

        with st.spinner("Generating constellation..."):

            clean_x, clean_y, noisy_x, noisy_y = run_constellation(
                scheme, snr
            )

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=noisy_x,
                y=noisy_y,
                mode="markers",
                name="Received noisy symbols",
                marker=dict(size=5, opacity=0.4)
            ))

            fig.add_trace(go.Scatter(
                x=clean_x,
                y=clean_y,
                mode="markers",
                name="Ideal constellation",
                marker=dict(size=12, symbol="circle-open")
            ))

            fig.update_layout(
                title=f"{scheme} Constellation at {snr} dB",
                xaxis_title="In-phase (I)",
                yaxis_title="Quadrature (Q)",
                xaxis=dict(scaleanchor="y", scaleratio=1),
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Click Generate Constellation to visualize the signals.")


# ---------------- TAB 4 ----------------

with tab4:

    st.subheader("Transmitted vs Received Bits")

    st.write(
        "Visualize the effect of the AWGN channel on binary transmission."
    )

    if st.button("Analyze Signal Transmission", type="primary"):

        k = BITS_PER_SYMBOL[scheme]

        bits = generate_bits(200 * k, seed=42)
        tx = modulate(bits, scheme)
        rx = awgn(tx, float(snr), k, seed=43)
        recovered = demodulate(rx, scheme)

        errors = int(np.sum(bits != recovered))

        st.metric("Transmission Errors", errors)

        display_count = 40

        bit_df = pd.DataFrame({
            "Bit Position": np.arange(display_count),
            "Transmitted": bits[:display_count],
            "Received": recovered[:display_count],
        })

        st.dataframe(bit_df, use_container_width=True)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=bit_df["Bit Position"],
            y=bit_df["Transmitted"],
            mode="lines+markers",
            name="Transmitted bits"
        ))

        fig.add_trace(go.Scatter(
            x=bit_df["Bit Position"],
            y=bit_df["Received"],
            mode="markers",
            name="Received bits"
        ))

        fig.update_layout(
            title="Transmitted vs Received Binary Data",
            xaxis_title="Bit Position",
            yaxis_title="Binary Value",
            yaxis=dict(tickmode="array", tickvals=[0, 1]),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Click Analyze Signal Transmission to compare bits.")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Digital Communication System Simulator | "
    "Python • Streamlit • NumPy • SciPy • Plotly | "
    "AWGN Channel Simulation"
)
