"""Streamlit front of the SoccerAutomated pipeline: subject -> analysis -> publication."""
import streamlit as st

from components.pages.instagram_publishing.automated import client
from components.pages.instagram_publishing.automated.decisions import CHRONICLES, STEP_OF, TITLES, VIEWS, show_result
from components.pages.instagram_publishing.automated.styles import badge, esc, inject_css, stepper

RUN_KEY = "automated_publishing__run_id"
POLL_SECONDS = 2
STATUS_LABELS = {"running": "En cours", "waiting": "Ta décision est attendue", "done": "Terminé",
                 "error": "Erreur", "cancelled": "Annulé"}


def _health_bar() -> bool:
    health = client.health()
    if health is None:
        st.error(
            "Le service SoccerAutomated ne répond pas. Lance-le depuis le dossier SoccerAutomated :\n\n"
            "`.venv/bin/uvicorn api.server:app --port 8765`",
            icon="🔌",
        )
        return False
    parts = [
        badge("API", "ok"),
        badge("Ollama", "ok" if health.get("ollama") else "ko"),
        badge("Base de données", "ok" if health.get("database") else "ko"),
    ]
    parts += [badge(f"modèle manquant : {m}", "ko") for m in health.get("missing_models", [])]
    st.markdown("".join(parts), unsafe_allow_html=True)
    with st.popover("Modèles utilisés", icon="🧠"):
        for role, spec in health.get("models", {}).items():
            st.markdown(f"- **{role}** : `{spec}`")
    return True


def _start_form():
    with st.container(border=True):
        st.markdown("#### Nouveau post")
        mode = st.segmented_control(
            "Point de départ", ["subject", "topic"], default="subject", key="automated_publishing__mode",
            format_func=lambda m: "🎯 Un sujet précis" if m == "subject" else "🔭 Un thème d'actualité",
        )
        placeholder = ("Ex : PSG vs OM, le Classique en Ligue 1 cette saison" if mode == "subject"
                       else "Ex : la course au titre en Premier League")
        text = st.text_area("Sujet" if mode == "subject" else "Thème", key="automated_publishing__text",
                            placeholder=placeholder, height=80)
        col1, col2 = st.columns(2)
        chronicle = None
        if mode == "subject":
            chronicle = col1.selectbox("Chronique", list(CHRONICLES), key="automated_publishing__chronicle",
                                       format_func=lambda c: f"{c} · {CHRONICLES[c]}")
        else:
            col1.caption("La chronique sera proposée avec chaque sujet trouvé dans l'actualité.")
        platforms = col2.pills("Plateformes", ["instagram", "x"], selection_mode="multi",
                               default=["instagram", "x"], key="automated_publishing__platforms",
                               format_func=lambda p: "📸 Instagram" if p == "instagram" else "✖️ X (Twitter)")
        if st.button("Lancer la génération", type="primary", icon="🚀",
                     disabled=not (text or "").strip() or not platforms or not mode):
            try:
                run = client.create_run(mode, text.strip(), chronicle, platforms)
            except client.ApiError as e:
                st.error(str(e))
                return
            st.session_state[RUN_KEY] = run["id"]
            st.rerun()


def _history():
    try:
        runs = client.list_runs()
    except client.ApiError:
        return
    if not runs:
        return
    with st.expander(f"🗂️ Runs de la session ({len(runs)})"):
        for run in runs:
            col1, col2, col3 = st.columns([5, 2, 1])
            col1.markdown(f"**{esc(run['title'][:80])}**  \n`{run['id']}` · {run['created_at'][11:16]}")
            col2.markdown(badge(STATUS_LABELS.get(run["status"], run["status"]),
                                {"done": "ok", "error": "ko", "waiting": "accent"}.get(run["status"], "")),
                          unsafe_allow_html=True)
            if col3.button("Ouvrir", key=f"automated_publishing__open_{run['id']}"):
                st.session_state[RUN_KEY] = run["id"]
                st.rerun()


def _running_step(run: dict) -> int:
    if run["stage"] == "subject":
        return 0
    if run["stage"] == "publish":
        return 4
    messages = {p["message"] for p in run["progress"]}
    if "Faits validés" in messages:
        return 3
    if "Plan validé" in messages:
        return 2
    return 1


def _progress_log(run: dict, expanded: bool):
    with st.expander("Journal", expanded=expanded):
        for item in run["progress"][-12:]:
            st.markdown(f'<div class="sa-log">{item["at"]} · {esc(item["message"])}</div>', unsafe_allow_html=True)


@st.fragment(run_every=POLL_SECONDS)
def _poll(run_id: str):
    """Refreshes itself while the service works, then reruns the page to show the next step."""
    try:
        run = client.get_run(run_id)
    except client.ApiError as e:
        st.error(str(e))
        return
    if run["status"] != "running":
        st.rerun(scope="app")
    stepper(_running_step(run))
    last = run["progress"][-1]["message"] if run["progress"] else "Démarrage"
    with st.status(f"Traitement en cours… (dernière étape : {last})", state="running", expanded=False):
        st.caption("Les modèles tournent en local : compter environ 1 à 2 minutes par étape d'IA.")
    _progress_log(run, expanded=True)


def _run_view(run_id: str):
    try:
        run = client.get_run(run_id)
    except client.ApiError as e:
        st.error(str(e))
        if st.button("Nouveau post"):
            st.session_state.pop(RUN_KEY, None)
            st.rerun()
        return

    st.markdown(f"### {esc(run['title'][:120])}")
    col1, col2, _ = st.columns([1, 1, 4])
    if col1.button("Nouveau", icon="➕", key="automated_publishing__new"):
        st.session_state.pop(RUN_KEY, None)
        st.rerun()
    if run["status"] in ("running", "waiting") and col2.button(
            "Annuler", icon="🛑", key="automated_publishing__cancel_run"):
        client.cancel(run_id)
        st.rerun()

    if run["status"] == "running":
        _poll(run_id)
        return

    if run["status"] == "waiting":
        pending = run["pending"]
        stepper(STEP_OF[pending["type"]])
        st.markdown(f"#### {TITLES[pending['type']]}")
        decision = VIEWS[pending["type"]](run, pending)
        if decision is not None:
            try:
                client.decide(run_id, decision)
            except client.ApiError as e:
                st.error(str(e))
                return
            st.rerun()
        _progress_log(run, expanded=False)
        return

    if run["status"] == "done":
        stepper(len(STEP_OF), done=True)
        show_result(run)
    elif run["status"] == "error":
        st.error(run["error"].split("\n\n")[0], icon="❌")
        if "\n\n" in run["error"]:
            with st.expander("Détails techniques"):
                st.code(run["error"])
    else:
        st.info("Run annulé.", icon="🛑")
    _progress_log(run, expanded=False)


def automated_publishing():
    inject_css()
    if not _health_bar():
        return
    run_id = st.session_state.get(RUN_KEY)
    if run_id:
        _run_view(run_id)
    else:
        _start_form()
    _history()
