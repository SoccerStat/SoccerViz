"""Ask something: a question in plain French -> entities -> read-only SQL query -> result and its stat.

Same experience as the automated publishing: status bar, steps, header with power mode and chrono, decision screens,
history of the session with an "Ouvrir" button.
"""
import uuid
from datetime import datetime

import pandas as pd
import streamlit as st

from components.pages.instagram_publishing.automated import client
from components.pages.instagram_publishing.automated.decisions import clarify_entities
from components.pages.instagram_publishing.automated.panel import _chrono, _duration, _health_bar, _model_name, _power_badge
from components.pages.instagram_publishing.automated.styles import badge, esc, inject_css, stepper

STEPS = ["Question", "Entités", "Résultat"]
QUESTIONS_KEY = "automated_publishing__questions"  # {id: question}, in asking order
CURRENT_KEY = "automated_publishing__question_id"
STATUS_LABELS = {"clarify": "Ta décision est attendue", "done": "Terminé", "error": "Erreur"}
EXAMPLES = ("Combien de buts le PSG a-t-il marqués à domicile en Ligue 1 en 2024-2025 ?",
            "Qui sont les 5 meilleurs passeurs de Ligue 1 cette saison ?",
            "Quel club de Premier League concède le moins de tirs par match cette saison ?")


def _questions() -> dict:
    return st.session_state.setdefault(QUESTIONS_KEY, {})


def _number(value) -> str:
    if isinstance(value, float):
        return f"{value:,.2f}".replace(",", " ").replace(".", ",").rstrip("0").rstrip(",")
    return f"{value:,}".replace(",", " ")


def _status(entry: dict) -> str:
    answer = entry["answer"]
    if answer.get("status") == "clarify":
        return "clarify"
    return "error" if answer.get("error") else "done"


def _as_run(entry: dict, power: dict) -> dict:
    """The fields read by the badges of the automated publishing (power mode, chrono)."""
    status = _status(entry)
    end = entry.get("finished_at") or datetime.now()
    usage = entry["answer"].get("cloud_usage") or {"enabled": entry["power"], "model": power.get("model", "")}
    return {"status": "waiting" if status == "clarify" else status, "cloud_usage": usage,
            "elapsed_s": (end - entry["created_at"]).total_seconds(), "compute_s": entry["compute_s"]}


def _ask(entry: dict, **kwargs):
    """Calls the service and stores the answer in the entry (a "clarify" answer waits for the human)."""
    with st.spinner("Résolution des entités, écriture et exécution de la requête…"):
        try:
            answer = client.ask_question(entry["question"], entry["power"], **kwargs)
        except client.ApiError as e:
            st.error(str(e))
            return
    entry["answer"], entry["compute_s"] = answer, entry["compute_s"] + answer.get("duration_s", 0)
    entry["round"] += 1
    if answer.get("status") != "clarify":
        entry["finished_at"] = datetime.now()
    st.rerun()


#########
# VIEWS #
#########
def _form(power: dict):
    stepper(0, steps=STEPS)
    with st.container(border=True):
        st.markdown("#### Nouvelle question")
        st.caption("Exemples : " + " · ".join(f"« {e} »" for e in EXAMPLES))
        question = st.text_area("Question", key="automated_publishing__question", height=80,
                                placeholder=EXAMPLES[0], label_visibility="collapsed")
        power_mode = st.toggle(
            "⚡ Power mode", key="automated_publishing__question_power", disabled=not power.get("available"),
            help=f"La requête SQL est écrite par le modèle cloud ({_model_name(power.get('model', ''))}), "
                 "le local reprend la main en cas d'échec.")
        if st.button("Lancer la requête", type="primary", icon="🔎", disabled=not (question or "").strip(),
                     key="automated_publishing__ask"):
            entry = {"id": uuid.uuid4().hex[:8], "question": question.strip(), "power": power_mode,
                     "created_at": datetime.now(), "finished_at": None, "compute_s": 0, "round": 0, "answer": {}}
            _questions()[entry["id"]] = entry
            st.session_state[CURRENT_KEY] = entry["id"]
            _ask(entry)


def _header(entry: dict, power: dict):
    st.markdown(f"### {esc(entry['question'][:160])}")
    answer = entry["answer"]
    chips = [badge(f"Modèle SQL : {_model_name(answer['model'])}")] if answer.get("model") else []
    st.markdown(_power_badge(_as_run(entry, power)) + _chrono(_as_run(entry, power)) + "".join(chips),
                unsafe_allow_html=True)
    if st.button("Nouveau", icon="➕", key="automated_publishing__question_new"):
        st.session_state.pop(CURRENT_KEY, None)
        st.rerun()


def _entities(answer: dict):
    chips = [badge(f"{e['shown']} · {e['type']}", "ok") for e in answer["entities"]]
    chips += [badge(f"Saison {s}") for s in answer["seasons"]]
    st.markdown("".join(chips), unsafe_allow_html=True)


def _clarify_view(entry: dict):
    stepper(1, steps=STEPS)
    st.markdown("#### Préciser les entités")
    answer = entry["answer"]
    decision = clarify_entities({"id": f"question_{entry['id']}_{entry['round']}"},
                                {"resolved": answer["entities"], "unresolved": answer["unresolved"]})
    if decision is not None:
        _ask(entry, entities=answer["entities"], unresolved=answer["unresolved"],
             clarifications=decision["clarifications"])


def _result_view(entry: dict):
    answer = entry["answer"]
    stepper(len(STEPS), done=True, steps=STEPS)
    _entities(answer)
    if answer["error"]:
        st.error(f"La requête n'a pas abouti : {answer['error']}", icon="❌")
    else:
        stat = answer.get("stat")
        if stat:
            st.metric(stat["label"], _number(stat["value"]), help=" · ".join(stat["context"]) or None)
        frame = pd.DataFrame(answer["rows"], columns=answer["columns"])
        st.dataframe(frame, use_container_width=True, hide_index=True)
    with st.expander("Requête SQL et explication"):
        if answer["reasoning"]:
            st.markdown(answer["reasoning"])
        if answer["sql"]:
            st.code(answer["sql"], language="sql")
        for column, meaning in (answer.get("columns_meaning") or {}).items():
            st.markdown(f"- `{column}` : {meaning}")
        st.caption(f"{answer['attempts']} essai(s) de l'agent SQL")


def _history():
    entries = list(reversed(_questions().values()))
    if not entries:
        return
    with st.expander(f"🗂️ Questions précédentes ({len(entries)})"):
        for entry in entries:
            status = _status(entry)
            col1, col2, col3 = st.columns([5, 2, 1])
            col1.markdown(f"**{esc(entry['question'][:80])}**  \n`{entry['id']}` · {entry['created_at']:%H:%M}"
                          f" · ⏱ {_duration(entry['compute_s'])}")
            col2.markdown(badge(STATUS_LABELS[status], {"done": "ok", "error": "ko", "clarify": "accent"}[status]),
                          unsafe_allow_html=True)
            if col3.button("Ouvrir", key=f"automated_publishing__open_question_{entry['id']}"):
                st.session_state[CURRENT_KEY] = entry["id"]
                st.rerun()


def question_to_stat():
    inject_css()
    health = _health_bar(roles=("grounder", "sql"))  # the two models a question uses
    if health is None:
        return
    power = health.get("power_mode") or {}
    entry = _questions().get(st.session_state.get(CURRENT_KEY))
    if entry is None or not entry["answer"]:
        _form(power)
    else:
        _header(entry, power)
        if _status(entry) == "clarify":
            _clarify_view(entry)
        else:
            _result_view(entry)
    _history()
