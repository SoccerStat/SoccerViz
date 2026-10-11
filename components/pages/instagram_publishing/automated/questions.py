"""Question -> SQL -> stat: ask the database a question in plain French and read the result, and the query."""
import pandas as pd
import streamlit as st

from components.pages.instagram_publishing.automated import client
from components.pages.instagram_publishing.automated.styles import badge, inject_css

HISTORY_KEY = "automated_publishing__questions"
EXAMPLES = ("Combien de buts le PSG a-t-il marqués à domicile en Ligue 1 en 2024-2025 ?",
            "Qui sont les 5 meilleurs passeurs de Ligue 1 cette saison ?",
            "Quel club de Premier League concède le moins de tirs par match cette saison ?")


def _number(value) -> str:
    if isinstance(value, float):
        return f"{value:,.2f}".replace(",", " ").replace(".", ",").rstrip("0").rstrip(",")
    return f"{value:,}".replace(",", " ")


def _form(power_available: bool):
    with st.container(border=True):
        st.markdown("#### Pose une question à la base")
        st.caption("Exemples : " + " · ".join(f"« {e} »" for e in EXAMPLES))
        question = st.text_area("Question", key="automated_publishing__question", height=80,
                                placeholder=EXAMPLES[0], label_visibility="collapsed")
        power = st.toggle("⚡ Power mode", key="automated_publishing__question_power", disabled=not power_available,
                          help="La requête SQL est écrite par le modèle cloud (repli local en cas d'échec).")
        if st.button("Lancer la requête", type="primary", icon="🔎", disabled=not (question or "").strip(),
                     key="automated_publishing__ask"):
            with st.spinner("Résolution des entités, écriture et exécution de la requête…"):
                try:
                    answer = client.ask_question(question.strip(), power)
                except client.ApiError as e:
                    st.error(str(e))
                    return
            st.session_state.setdefault(HISTORY_KEY, []).insert(0, answer)


def _answer(answer: dict):
    st.markdown(f"**{answer['question']}**")
    chips = [badge(f"{e['shown']} · {e['type']}", "ok") for e in answer["entities"]]
    chips += [badge(f"{u['mention']} : {'ambigu' if u['status'] == 'ambiguous' else 'introuvable'}", "ko")
              for u in answer["unresolved"]]
    chips += [badge(f"Saison {s}") for s in answer["seasons"]]
    st.markdown("".join(chips), unsafe_allow_html=True)
    for u in answer["unresolved"]:
        if u["candidates"]:
            st.caption(f"« {u['mention']} » : précise la question, par exemple avec {', '.join(u['candidates'][:3])}.")

    if answer["error"]:
        st.error(f"La requête n'a pas abouti : {answer['error']}", icon="❌")
    else:
        stat = answer.get("stat")
        if stat:
            st.metric(stat["label"], _number(stat["value"]), help=" · ".join(stat["context"]) or None)
        frame = pd.DataFrame(answer["rows"], columns=answer["columns"])
        st.dataframe(frame, use_container_width=True, hide_index=True)
        st.download_button("Télécharger le résultat (CSV)", frame.to_csv(index=False).encode("utf-8"), icon="⬇️",
                           file_name="resultat.csv", key=f"automated_publishing__csv_{id(answer)}")
    with st.expander("Requête SQL et explication"):
        if answer["reasoning"]:
            st.markdown(answer["reasoning"])
        if answer["sql"]:
            st.code(answer["sql"], language="sql")
        for column, meaning in (answer.get("columns_meaning") or {}).items():
            st.markdown(f"- `{column}` : {meaning}")
    usage = answer.get("cloud_usage") or {}
    cost = f" · ~{usage['cost_usd']:.3f} $".replace(".", ",") if usage.get("calls") else ""
    st.caption(f"Modèle : {answer['model'] or '—'} · {answer['attempts']} essai(s) · ⏱ {answer['duration_s']} s{cost}")


def question_to_stat():
    inject_css()
    health = client.health()
    if health is None:
        st.error("Le service SoccerAutomated ne répond pas.", icon="🔌")
        return
    _form(bool((health.get("power_mode") or {}).get("available")))
    history = st.session_state.get(HISTORY_KEY, [])
    if history:
        with st.container(border=True):
            _answer(history[0])
    if len(history) > 1:
        with st.expander(f"🗂️ Questions précédentes ({len(history) - 1})"):
            for answer in history[1:]:
                _answer(answer)
                st.divider()
