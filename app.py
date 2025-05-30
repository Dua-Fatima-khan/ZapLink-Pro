import streamlit as st
import pyshorteners
import qrcode
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="ZapLink Pro",
    layout="centered",
    page_icon="⚡",
)

# Custom CSS 
st.markdown("""
<style>
    :root {
        --primary: #4fc3f7;  /* Light blue accent */
        --secondary: #090b33; /* Dark blue background */
        --accent: #ffffff;   /* White text */
        --highlight: #00e676; /* Green for buttons */
    }

    /* Main background */
    .stApp {
        background-color: var(--secondary);
        color: var(--accent);
    }

    /* Headers with gradient text */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary) !important;
        background: linear-gradient(90deg, #4fc3f7, #00e676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #070927 !important;
        border-right: 1px solid rgba(79, 195, 247, 0.2) !important;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] * {
        color: var(--accent) !important;
    }

    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio label {
        color: var(--accent) !important;
    }

    /* Buttons with glow effect */
    .stButton>button {
        background-color: var(--highlight) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 10px rgba(0, 230, 118, 0.5) !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 0 15px rgba(0, 230, 118, 0.8) !important;
    }

    /* Input fields */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: var(--accent) !important;
        border: 1px solid var(--primary) !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }

    /* Slider */
    .stSlider>div>div>div>div {
        background: linear-gradient(90deg, #4fc3f7, #00e676) !important;
    }

    /* Success message */
    .stAlert.stAlert-success {
        background-color: rgba(0, 230, 118, 0.1) !important;
        border-left: 4px solid var(--highlight) !important;
        color: var(--accent) !important;
    }

    /* Code block */
    .stCodeBlock>div>pre {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border-left: 4px solid var(--primary) !important;
        color: var(--primary) !important;
    }

    /* Divider line */
    .stMarkdown hr {
        background: linear-gradient(90deg, transparent, var(--primary), transparent) !important;
        height: 1px !important;
        border: none !important;
    }

    /* QR Code container */
    .stImage>img {
        border: 2px solid var(--primary) !important;
        border-radius: 10px !important;
        box-shadow: 0 0 20px rgba(79, 195, 247, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.title("⚡ ZapLink Pro")
st.sidebar.markdown("""
<div style="color: #4fc3f7; font-size: 0.9rem;">
Your ultimate URL toolkit for developers
</div>
""", unsafe_allow_html=True)

mode = st.sidebar.radio(
    "Choose Tool",
    ["Shorten URL", "Generate QR Code"],
    help="Select your desired utility"
)

# --- MAIN CONTENT ---
st.title("ZapLink Pro")
st.markdown("""
<div style="color: #ffffff; font-size: 1.1rem; line-height: 1.6;">
⚡Shorten links instantly or create 
custom QR codes with professional styling.
</div>
""", unsafe_allow_html=True)

# --- SHORTEN URL ---
if mode == "Shorten URL":
    st.subheader("🔗 URL Shortener")
    with st.container():
        long_url = st.text_input(
            "Enter URL to shorten", 
            placeholder="https://yourlongurl.com",
            help="Paste any URL to get a shortened version"
        )

        if st.button("Shorten URL", key="shorten_btn"):
            if long_url:
                try:
                    s = pyshorteners.Shortener()
                    short_url = s.tinyurl.short(long_url)

                    st.success("Shortened URL created successfully!")
                    st.balloons()

                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.code(short_url)
                    with col2:
                        st.markdown(f"""
                        <a href="{short_url}" target="_blank" style="
                            background-color: #00e676;
                            color: #000;
                            padding: 0.5em 1em;
                            text-decoration: none;
                            border-radius: 8px;
                            display: inline-block;
                            font-weight: bold;
                            box-shadow: 0 0 10px rgba(0, 230, 118, 0.5);
                        ">Open</a>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.error("Error shortening URL. Please check your input.")
            else:
                st.warning("Please enter a URL first.")

# --- QR CODE GENERATOR ---
elif mode == "Generate QR Code":
    st.subheader("QR Code Generator")

    with st.container():
        qr_data = st.text_input(
            "Content to encode",
            placeholder="https://example.com or any text",
            help="Enter what you want to encode in the QR code"
        )

        col1, col2 = st.columns(2)
        with col1:
            fill_color = st.color_picker(
                "QR Color", 
                "#4fc3f7",
                help="Color of the QR code dots"
            )
        with col2:
            back_color = st.color_picker(
                "Background", 
                "#090b33",
                help="Background color of the QR code"
            )

        size = st.slider(
            "QR Size", 
            min_value=5, 
            max_value=20, 
            value=10,
            help="Adjust the pixel density of the QR code"
        )

        if st.button("Generate QR Code", key="qr_btn"):
            if qr_data:
                qr = qrcode.QRCode(
                    version=1,
                    box_size=size,
                    border=4
                )
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color=fill_color, back_color=back_color)

                buf = BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)

                st.success("QR Code generated successfully!")
                st.balloons()

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.image(buf, caption="Your QR Code", width=300)
                with col2:
                    st.download_button(
                        label="Download QR",
                        data=buf,
                        file_name="zap_qr.png",
                        mime="image/png",
                        help="Save QR code as PNG"
                    )
            else:
                st.warning("Please enter content to encode first.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #4fc3f7; font-size: 0.9rem;">
    <div>Built with ❤️ by Dua Fatima</div>
    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">    
    Copyright © 2025 - All Rights Reserved</div>
</div>
""", unsafe_allow_html=True)
