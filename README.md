# WatermarkCheck demo

## Run in Google Colab (recommended for tomorrow)

1. Upload `app.py`, `watermark_engine.py`, and `requirements.txt` to the Colab session (or put them in the same Drive folder and change into it).
2. Select **Runtime → Change runtime type → T4 GPU** when available.
3. Run:

```python
!pip install -q -r requirements.txt
```

4. Start Streamlit with a public tunnel:

```python
!streamlit run app.py &>/content/streamlit.log &
!npx --yes localtunnel --port 8501
```

Open the `https://...loca.lt` URL printed by LocalTunnel. Keep the Colab cell running. If the tunnel asks for a password, run `!curl -s https://loca.lt/mytunnelpassword` in another cell and enter the returned IP. The first app load downloads GPT-2 weights.

## Run on a computer

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## What to demonstrate

Generate a watermarked and an ordinary sample from the same prompt; analyze both and show the z-score, p-value and decision. Then use **Deletion test** to compare the source against a word-deleted version. Keep the Colab notebook and screenshots as a fallback if the tunnel or network is unreliable.

The app uses the same `WatermarkingConfig` parameters recorded in the working Colab implementation. Detection is specifically for this configured statistical watermark, not a general-purpose AI-text detector.
