"""One view per human decision of the SoccerAutomated pipeline.

Each view returns the decision to send to the service, or None while the user has not submitted.
"""
from typing import Optional

import pandas as pd
import streamlit as st

from components.pages.instagram_publishing.automated import client
from components.pages.instagram_publishing.automated.styles import badge, esc, slide_html

CHRONICLES = {
    "Focus": "Portrait d'un club ou d'un joueur",
    "VS": "Face-à-face entre deux entités",
    "A few time ago": "Évolution dans le temps",
}
DEFAULT_THEME = "#0B1F3A"
X_MAX_CHARS = 280


def _warnings(warnings: list[str], expanded: bool = False):
    if warnings:
        with st.expander(f"⚠️ {len(warnings)} avertissement(s)", expanded=expanded):
            for warning in warnings:
                st.markdown(f"- {warning}")


def _feedback_form(key: str, label: str, button: str) -> Optional[dict]:
    with st.form(key=f"{key}__feedback", border=False):
        feedback = st.text_area(label, key=f"{key}__feedback_text", height=80,
                                placeholder="Ex : ajoute un angle sur les buts en fin de match")
        if st.form_submit_button(button, icon="🔁") and feedback.strip():
            return {"action": "retry", "feedback": feedback.strip()}
    return None


###########
# SUBJECT #
###########
def clarify_entities(run: dict, pending: dict) -> Optional[dict]:
    st.info("Certaines entités n'ont pas été trouvées avec certitude dans la base. Précise-les.", icon="🔎")
    if pending["resolved"]:
        st.markdown("Déjà résolues : " + "".join(badge(e["name"], "ok") for e in pending["resolved"]),
                    unsafe_allow_html=True)
    clarifications = []
    with st.form(key=f"{run['id']}__clarify"):
        for i, entity in enumerate(pending["unresolved"]):
            st.markdown(f"**« {esc(entity['mention'])} »** · {entity['type']} · "
                        f"{'ambigu' if entity['status'] == 'ambiguous' else 'introuvable'}")
            options = [f"{c['name']} (score {c.get('score')})" for c in entity["candidates"]]
            choice = st.radio("Choix", options + ["✏️ Reformuler", "⏭️ Ignorer cette entité"],
                              key=f"{run['id']}__clarify_{i}", label_visibility="collapsed")
            reformulation = st.text_input("Reformulation", key=f"{run['id']}__reformulate_{i}",
                                          placeholder="Nom complet, ex : Paris Saint-Germain")
            item = {"mention": entity["mention"], "entity_type": entity["type"]}
            if choice in options:
                candidate = entity["candidates"][options.index(choice)]
                item.update(chosen_id=candidate["id"], chosen_name=candidate["name"])
            elif choice.startswith("⏭️"):
                item["skip"] = True
            else:
                item["reformulation"] = reformulation
            clarifications.append(item)
            st.divider()
        if st.form_submit_button("Valider", type="primary", icon="✅"):
            return {"action": "approve", "clarifications": clarifications}
    return None


def choose_subject(run: dict, pending: dict) -> Optional[dict]:
    st.markdown("#### Sujets proposés à partir de l'actualité")
    columns = st.columns(min(3, max(1, len(pending["subjects"]))))
    for i, subject in enumerate(pending["subjects"]):
        with columns[i % len(columns)].container(border=True):
            st.markdown(badge(subject["chronicle"], "accent"), unsafe_allow_html=True)
            st.markdown(f"**{esc(subject['subject'])}**")
            if subject.get("feedback"):
                st.caption(subject["feedback"])
            chronicle = st.selectbox("Chronique", list(CHRONICLES), key=f"{run['id']}__chronicle_{i}",
                                     index=list(CHRONICLES).index(subject["chronicle"]))
            if st.button("Choisir ce sujet", key=f"{run['id']}__choose_{i}", icon="👉", use_container_width=True):
                return {"action": "approve", "index": i, "chronicle": chronicle}
    with st.expander(f"📰 {len(pending['articles'])} articles sources"):
        for article in pending["articles"]:
            st.markdown(f"- [{article['title']}]({article['url']})")
    return _feedback_form(run["id"] + "__subjects", "Aucun ne convient ? Oriente la génération :",
                          "Proposer d'autres sujets")


def review_prompt(run: dict, pending: dict) -> Optional[dict]:
    subject = pending["subject"]
    st.markdown(badge(subject["chronicle"], "accent") + f" **{esc(subject['subject'])}**", unsafe_allow_html=True)
    st.markdown("Entités : " + "".join(badge(f"{e['name']} · {e['type']}", "ok") for e in pending["entities"]),
                unsafe_allow_html=True)
    prompt = st.text_area("Prompt d'analyse (modifiable)", value=pending["prompt"], height=160,
                          key=f"{run['id']}__prompt")
    if st.button("Valider et lancer l'analyse", type="primary", icon="🚀", key=f"{run['id']}__prompt_ok"):
        decision = {"action": "approve"}
        if prompt.strip() != pending["prompt"].strip():
            decision["prompt"] = prompt.strip()
        return decision
    return _feedback_form(run["id"] + "__prompt", "Ou demande une nouvelle version :", "Régénérer le prompt")


############
# ANALYSIS #
############
def review_plan(run: dict, pending: dict) -> Optional[dict]:
    st.markdown(
        "Saisons : " + "".join(badge(s.replace("_", "-")) for s in pending["seasons"])
        + (" · Compétition : " + badge(pending["competition_id"]) if pending["competition_id"] else ""),
        unsafe_allow_html=True,
    )
    tasks = pd.DataFrame([{
        "Garder": True,
        "Angle": t["label"],
        "Entité": t["entity_name"] + (f" vs {t['other_entity_name']}" if t.get("other_entity_name") else ""),
        "Périmètre": t["scope"],
        "Pourquoi": t.get("reason", ""),
    } for t in pending["tasks_data"]])
    edited = st.data_editor(
        tasks, key=f"{run['id']}__plan_editor", hide_index=True, use_container_width=True,
        disabled=["Angle", "Entité", "Périmètre", "Pourquoi"],
        column_config={"Garder": st.column_config.CheckboxColumn(width="small")},
    )
    keep_sql = True
    if pending["custom_questions"]:
        st.markdown("**Questions hors catalogue (SQL généré par l'IA, à valider ensuite)**")
        for question in pending["custom_questions"]:
            st.markdown(f"- {question}")
        keep_sql = st.toggle("Exécuter ces requêtes libres", value=True, key=f"{run['id']}__keep_sql")
    _warnings(pending["warnings"])

    if st.button("Lancer l'analyse", type="primary", icon="▶️", key=f"{run['id']}__plan_ok"):
        removed = [i for i, keep in enumerate(edited["Garder"]) if not keep]
        if len(removed) == len(tasks):
            st.error("Garde au moins un angle.")
            return None
        return {"action": "approve", "remove_tasks": removed, "drop_custom_questions": not keep_sql}
    return _feedback_form(run["id"] + "__plan", "Ou demande un autre plan :", "Replanifier")


def review_facts(run: dict, pending: dict) -> Optional[dict]:
    facts = pending["facts_data"]
    col1, col2, col3 = st.columns(3)
    col1.metric("Faits calculés", len(facts))
    col2.metric("Faits classés 1er ou dernier", sum(1 for f in facts if f.get("rank") in (1, f.get("rank_of"))))
    col3.metric("Avertissements", len(pending["warnings"]))

    table = pd.DataFrame([{
        "Exclure": False,
        "Id": f["id"],
        "Valeur": f["display"],
        "Rang": f.get("rank_text") or "",
        "Métrique": f["label"],
        "Entité": f["entity_name"],
        "Comparaison": f.get("comparison") or "",
        "Périmètre": f["scope"] + (f" · {f['sample']}" if f.get("sample") else ""),
        "Intérêt": round(f["score"], 2),
    } for f in facts])
    edited = st.data_editor(
        table, key=f"{run['id']}__facts_editor", hide_index=True, use_container_width=True, height=420,
        disabled=[c for c in table.columns if c != "Exclure"],
        column_config={
            "Exclure": st.column_config.CheckboxColumn(width="small"),
            "Intérêt": st.column_config.ProgressColumn(min_value=0, max_value=1, format="%.2f"),
        },
    )
    _warnings(pending["warnings"])

    approve_custom = []
    for i, custom in enumerate(pending["custom_results"]):
        with st.expander(f"🧪 SQL libre : {custom['question']}", expanded=True):
            st.code(custom["sql"] or "-", language="sql")
            if custom.get("reasoning"):
                st.caption(custom["reasoning"])
            if custom["error"]:
                st.error(custom["error"])
                continue
            st.dataframe(pd.DataFrame(custom["rows"], columns=custom["columns"]), hide_index=True)
            if st.checkbox("J'ai vérifié ce résultat, il peut être utilisé", key=f"{run['id']}__custom_{i}"):
                approve_custom.append(i)

    if st.button("Rédiger le post avec ces faits", type="primary", icon="✍️", key=f"{run['id']}__facts_ok"):
        excluded = edited.loc[edited["Exclure"], "Id"].tolist()
        return {"action": "approve", "exclude": excluded, "approve_custom": approve_custom}
    return _feedback_form(run["id"] + "__facts", "Pas satisfait ? Replanifie l'analyse :", "Replanifier")


def _slide_colors(draft: dict, side: Optional[str]) -> str:
    colors = draft.get("colors")
    if colors and side in ("home", "away"):
        return f"linear-gradient(160deg, {colors[f'{side}_primary']}, {colors[f'{side}_secondary']})"
    return f"linear-gradient(160deg, {DEFAULT_THEME}, #1B3A66)"


def _platforms(run: dict) -> list[str]:
    return run["request"].get("platforms") or ["instagram", "x"]


def _post_preview(draft: dict, with_cover: bool = True):
    """Preview of the Instagram carousel (cover, one slide per stat, closing slide)."""
    slides = []
    if with_cover:
        slides.append(slide_html(
            " vs ".join(e["name"] for e in draft["entities"] if e["id"] in draft["sides"].values())
            or draft["chronicle"], draft["title"], draft["chronicle"], draft["intro"],
            _slide_colors(draft, "home" if draft["sides"] else None), cover=True,
        ))
    for card in draft["cards"]:
        slides.append(slide_html(card["title"], card["stat"], card["sub_title"], card["text"],
                                 _slide_colors(draft, card["side"])))
    if with_cover:
        slides.append(slide_html("En résumé", "", "", draft["conclusion"],
                                 _slide_colors(draft, "away" if draft["sides"] else None)))
    st.markdown(f'<div class="sa-slides">{"".join(slides)}</div>', unsafe_allow_html=True)


def _instagram_preview(caption: str, hashtags: list[str]):
    st.markdown("**📸 Légende Instagram**")
    st.markdown(f'<div class="sa-post"><div class="head">soccerstat</div>{esc(caption)}\n\n'
                f'<span style="color:#00376B">{esc(" ".join(hashtags))}</span></div>', unsafe_allow_html=True)


def _social_preview(caption: str, hashtags: list[str], thread: list[str], platforms: list[str]):
    columns = iter(st.columns(len(platforms)))
    if "instagram" in platforms:
        with next(columns):
            _instagram_preview(caption, hashtags)
    if "x" in platforms:
        with next(columns):
            _x_preview(thread)


def x_length(text: str) -> int:
    """Approximation of X's weighted length (emojis count double), as on the service side."""
    return sum(2 if ord(ch) > 0x10FF else 1 for ch in text)


def _x_thread_editor(run_id: str, thread: list[str]) -> Optional[list[dict]]:
    """Kept and edited tweets ([{"index", "text"}]), or None when the thread is unchanged."""
    kept = []
    for i, tweet in enumerate(thread):
        col1, col2 = st.columns([1, 12])
        keep = col1.checkbox(f"{i + 1}", value=True, key=f"{run_id}__keep_{i}", help="Décocher pour exclure ce post")
        text = col2.text_area(f"Post {i + 1}", value=tweet, height=110, key=f"{run_id}__tweet_{i}",
                              disabled=not keep, label_visibility="collapsed")
        length = x_length(text)
        col2.caption(f"{length}/{X_MAX_CHARS} caractères" + (" · trop long, il sera coupé" if length > X_MAX_CHARS
                                                             else "") + ("" if keep else " · exclu"))
        if keep:
            kept.append({"index": i, "text": text.strip()})
    if not kept:
        st.warning("Garde au moins un post, sinon le thread X est vide.", icon="⚠️")
    if len(thread) - 1 not in {k["index"] for k in kept} and kept and "#" in thread[-1]:
        st.caption("Les hashtags du dernier post exclu seront ajoutés au dernier post gardé.")
    unchanged = [k["text"] for k in kept] == [t.strip() for t in thread]
    return None if unchanged else kept


def _x_preview(thread: list[str]):
    st.markdown(f"**✖️ Thread X ({len(thread)} posts)**")
    for i, tweet in enumerate(thread, start=1):
        over = x_length(tweet) > X_MAX_CHARS
        st.markdown(f'<div class="sa-tweet">{esc(tweet)}<div class="meta{" over" if over else ""}">'
                    f'{i}/{len(thread)} · {x_length(tweet)}/{X_MAX_CHARS} caractères</div></div>',
                    unsafe_allow_html=True)


def review_draft(run: dict, pending: dict) -> Optional[dict]:
    draft, platforms = pending["draft"], _platforms(run)
    instagram = "instagram" in platforms
    if instagram:  # X is text only: no visual to preview
        st.markdown("#### Aperçu du carrousel")
        _post_preview(draft)
    _social_preview(draft["caption"], draft["hashtags"], draft["x_thread"], platforms)
    _warnings(draft["warnings"])

    edits = {}
    if instagram:
        with st.expander("✏️ Retoucher la légende avant validation"):
            caption = st.text_area("Légende", value=draft["caption"], height=220, key=f"{run['id']}__caption")
            hashtags = st.text_input("Hashtags", value=" ".join(draft["hashtags"]), key=f"{run['id']}__hashtags")
        if caption.strip() != draft["caption"].strip():
            edits["caption"] = caption.strip()
        tags = [t if t.startswith("#") else f"#{t}" for t in hashtags.split()]
        if tags != draft["hashtags"]:
            edits["hashtags"] = tags
    if "x" in platforms and draft["x_thread"]:
        with st.expander("✏️ Retoucher le thread X (modifier ou exclure des posts)"):
            x_thread = _x_thread_editor(run["id"], draft["x_thread"])
        if x_thread is not None:
            edits["x_thread"] = x_thread
    label = "Valider le brouillon et générer les visuels" if instagram else "Valider le thread"
    empty_thread = edits.get("x_thread") == []
    if st.button(label, type="primary", icon="🎨" if instagram else "✅", key=f"{run['id']}__draft_ok",
                 disabled=empty_thread):
        return {"action": "approve", "edits": edits}
    return _feedback_form(run["id"] + "__draft", "Ou demande une réécriture :", "Réécrire")


###############
# PUBLICATION #
###############
def _gallery(run_id: str, files: list[str]):
    columns = st.columns(4)
    for i, _ in enumerate(files):
        try:
            columns[i % 4].image(client.rendered_file(run_id, i), use_container_width=True)
        except client.ApiError as e:
            columns[i % 4].warning(str(e))


def _slides_editor(run: dict, pending: dict):
    """Edit the filled copy of the template in PowerPoint, then re-export the slides shown above."""
    with st.container(border=True):
        st.markdown("**🖍️ Modifier les slides**")
        st.caption("Ouvre la maquette dans PowerPoint, fais tes retouches et enregistre (⌘S), puis régénère les "
                   "slides : ce sont elles qui seront publiées.")
        col1, col2, col3 = st.columns(3)
        if col1.button("Ouvrir dans PowerPoint", icon="📂", use_container_width=True, key=f"{run['id']}__open_pptx"):
            try:
                client.open_pptx(run["id"])
            except client.ApiError as e:
                st.error(str(e))
        if col2.button("Régénérer les slides", icon="🔄", use_container_width=True, key=f"{run['id']}__refresh"):
            with st.spinner("Export des slides depuis PowerPoint…"):
                try:
                    client.refresh_slides(run["id"])
                except client.ApiError as e:
                    st.error(str(e))
                    return
            st.rerun()
        try:
            col3.download_button("Télécharger la maquette", client.pptx(run["id"]), icon="⬇️",
                                 file_name=pending["pptx_file"].rsplit("/", 1)[-1], use_container_width=True,
                                 key=f"{run['id']}__download_pptx")
        except client.ApiError:
            pass


def validate_publication(run: dict, pending: dict) -> Optional[dict]:
    available = pending["platforms"]  # platforms whose copy was written; they can only be removed here
    if pending["files"]:  # Instagram carousel (X is text only)
        st.markdown(f"#### Visuels générés ({len(pending['files'])})")
        _gallery(run["id"], pending["files"])
    if pending.get("pptx_file") and "instagram" in available:
        _slides_editor(run, pending)
    caption, _, hashtags = pending["caption"].rpartition("\n\n")
    _social_preview(caption, hashtags.split(), pending["x_thread"], available)
    _warnings(pending["warnings"])

    with st.container(border=True):
        platforms = st.pills("Plateformes", available, selection_mode="multi", default=available,
                             key=f"{run['id']}__platforms",
                             format_func=lambda p: "📸 Instagram" if p == "instagram" else "✖️ X (Twitter)")
        live = st.toggle("Publication réelle (sinon simulation : rien n'est publié)", key=f"{run['id']}__live")
        confirmed = True
        if live:
            confirmed = st.checkbox("Je confirme la publication publique sur les plateformes sélectionnées",
                                    key=f"{run['id']}__confirm")
        col1, col2 = st.columns([3, 1])
        label = "Publier maintenant" if live else "Terminer en simulation"
        if col1.button(label, type="primary", icon="📤" if live else "🧪", use_container_width=True,
                       disabled=not platforms or not confirmed, key=f"{run['id']}__publish"):
            return {"action": "approve", "platforms": platforms, "dry_run": not live}
        if col2.button("Annuler", icon="🛑", use_container_width=True, key=f"{run['id']}__publish_cancel"):
            return {"action": "cancel"}
    return None


def show_result(run: dict):
    result = run["result"] or {}
    for publication in result.get("publication_results", []):
        name = "Instagram" if publication["platform"] == "instagram" else "X"
        if not publication["success"]:
            st.error(f"{name} : échec - {publication['detail']}")
        elif publication["dry_run"]:
            st.info(f"{name} : simulation terminée, rien n'a été publié.", icon="🧪")
        else:
            st.success(f"{name} : publié ! {publication.get('url') or ''}", icon="🎉")
    if not result.get("publication_results"):
        st.info("Publication annulée. Le brouillon et les visuels sont archivés.", icon="🗄️")
    if result.get("rendered_files"):
        _gallery(run["id"], result["rendered_files"])
        st.caption(f"Dossier : {result['rendered_files'][0].rsplit('/', 2)[0]}")
    if result.get("pptx_file"):
        st.caption(f"Présentation PowerPoint remplie : {result['pptx_file']}")
    draft = result.get("draft")
    if draft and draft.get("caption"):
        st.download_button("Télécharger la légende", draft["caption"] + "\n\n" + " ".join(draft["hashtags"]),
                           file_name="caption.txt", icon="⬇️")


VIEWS = {
    "clarify_entities": clarify_entities,
    "choose_subject": choose_subject,
    "review_prompt": review_prompt,
    "review_plan": review_plan,
    "review_facts": review_facts,
    "review_draft": review_draft,
    "validate_publication": validate_publication,
}
STEP_OF = {"clarify_entities": 0, "choose_subject": 0, "review_prompt": 0, "review_plan": 1,
           "review_facts": 2, "review_draft": 3, "validate_publication": 4}
TITLES = {
    "clarify_entities": "Préciser les entités",
    "choose_subject": "Choisir un sujet",
    "review_prompt": "Valider le prompt d'analyse",
    "review_plan": "Valider le plan d'analyse",
    "review_facts": "Contrôler les faits calculés",
    "review_draft": "Relire le brouillon",
    "validate_publication": "Publier",
}
