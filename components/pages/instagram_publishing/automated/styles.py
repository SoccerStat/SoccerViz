import html

import streamlit as st

ACCENT = "#FF6B6B"
STEPS = ["Sujet", "Plan d'analyse", "Faits", "Brouillon", "Publication"]

CSS = f"""
<style>
.sa-stepper {{ display: flex; justify-content: space-between; margin: 0.5rem 0 1.5rem 0; }}
.sa-step {{ flex: 1; text-align: center; position: relative; font-size: 0.85rem; color: #9AA0A6; }}
.sa-step::before {{ content: ""; position: absolute; top: 17px; left: -50%; width: 100%; height: 3px;
                   background: #E3E6EA; z-index: 0; }}
.sa-step:first-child::before {{ display: none; }}
.sa-step.done::before, .sa-step.active::before {{ background: {ACCENT}; }}
.sa-dot {{ position: relative; z-index: 1; width: 36px; height: 36px; line-height: 36px; margin: 0 auto 6px auto;
          border-radius: 50%; background: #E3E6EA; color: white; font-weight: 700; }}
.sa-step.done .sa-dot {{ background: {ACCENT}; }}
.sa-step.active .sa-dot {{ background: white; color: {ACCENT}; border: 3px solid {ACCENT}; line-height: 30px; }}
.sa-step.active, .sa-step.done {{ color: #262730; font-weight: 600; }}

.sa-badge {{ display: inline-block; padding: 2px 10px; margin: 2px 4px 2px 0; border-radius: 999px;
            font-size: 0.78rem; font-weight: 600; background: #F0F2F6; color: #262730; }}
.sa-badge.ok {{ background: #E6F4EA; color: #1E7B34; }}
.sa-badge.ko {{ background: #FCE8E6; color: #B3261E; }}
.sa-badge.accent {{ background: #FFE3E3; color: #C62828; }}

.sa-slides {{ display: flex; gap: 14px; overflow-x: auto; padding: 4px 2px 14px 2px; }}
.sa-slide {{ flex: 0 0 230px; height: 288px; border-radius: 14px; padding: 16px; color: white;
            display: flex; flex-direction: column; justify-content: space-between;
            box-shadow: 0 4px 14px rgba(0,0,0,0.15); }}
.sa-slide .who {{ font-size: 0.72rem; font-weight: 700; letter-spacing: 0.04em; text-transform: uppercase;
                 opacity: 0.85; }}
.sa-slide .stat {{ font-size: 3rem; font-weight: 900; line-height: 1; text-align: center; }}
.sa-slide .label {{ font-size: 0.8rem; font-weight: 700; text-align: center; text-transform: uppercase; }}
.sa-slide .text {{ font-size: 0.78rem; text-align: center; opacity: 0.95; }}
.sa-slide.cover .stat {{ font-size: 1.6rem; text-transform: uppercase; }}

.sa-post {{ border: 1px solid #E3E6EA; border-radius: 14px; padding: 14px 16px; background: white;
           white-space: pre-wrap; font-size: 0.9rem; }}
.sa-post .head {{ font-weight: 700; margin-bottom: 6px; }}
.sa-tweet {{ border: 1px solid #E3E6EA; border-radius: 14px; padding: 12px 14px; margin-bottom: 8px;
            background: white; white-space: pre-wrap; font-size: 0.88rem; }}
.sa-tweet .meta {{ color: #9AA0A6; font-size: 0.75rem; margin-top: 6px; }}
.sa-tweet .meta.over {{ color: #B3261E; font-weight: 700; }}
.sa-log {{ font-family: ui-monospace, monospace; font-size: 0.8rem; color: #5F6368; }}
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def esc(text) -> str:
    return html.escape(str(text or ""))


def badge(text: str, kind: str = "") -> str:
    return f'<span class="sa-badge {kind}">{esc(text)}</span>'


def stepper(active: int, done: bool = False):
    items = []
    for i, label in enumerate(STEPS):
        state = "done" if done or i < active else ("active" if i == active else "")
        mark = "✓" if state == "done" else str(i + 1)
        items.append(f'<div class="sa-step {state}"><div class="sa-dot">{mark}</div>{esc(label)}</div>')
    st.markdown(f'<div class="sa-stepper">{"".join(items)}</div>', unsafe_allow_html=True)


def slide_html(who: str, stat: str, label: str, text: str, background: str, cover: bool = False) -> str:
    return (
        f'<div class="sa-slide{" cover" if cover else ""}" style="background:{background}">'
        f'<div class="who">{esc(who)}</div><div class="stat">{esc(stat)}</div>'
        f'<div class="label">{esc(label)}</div><div class="text">{esc(text)}</div></div>'
    )
