import streamlit as st


def publish_vs_post(template_path):

    with st.expander("Home logo"):
        ""

    with st.expander("Away logo"):
        ""

    with st.expander("First slide"):
        ""

    with st.expander("Away slides"):
        nb_away_slides = st.number_input(
            key="publish_vs__nb_away_slides",
            label="How many slides for the away team?",
            min_value=0,
            max_value=10,
            value=1,
            step=1
        )

        slides_text = []
        for i in nb_away_slides:
            with st.expander(f"Content of the away slide {i + 1}"):
                title = st.text_input(f"Title", key=f"publish_vs__away_slide_{i}__title")
                stat = st.text_input(f"Stat", key=f"publish_vs__away_slide_{i}__stat")
                sub_title = st.text_input(f"Stat", key=f"publish_vs__away_slide_{i}__sub_title")
                sub_sub_title = st.text_input(f"Stat", key=f"publish_vs__away_slide_{i}__sub_sub_title")

                slides_text.append({
                    "title": title,
                    "stat": stat,
                    "stat_shape": stat,
                    "sub_title": sub_title,
                    "sub_sub_title": sub_sub_title
                })

    with st.expander("Intermediate slide"):
        ""

    with st.expander("Home slides"):
        nb_home_slides = st.number_input(
            key="publish_vs__nb_home_slides",
            label="How many slides for the home team?",
            min_value=0,
            max_value=10,
            value=1,
            step=1
        )

        slides_text = []
        for i in nb_home_slides:
            with st.expander(f"Content of the home slide {i + 1}"):
                title = st.text_input(f"Title", key=f"publish_vs__home_slide_{i}__title")
                stat = st.text_input(f"Stat", key=f"publish_vs__home_slide_{i}__stat")
                sub_title = st.text_input(f"Stat", key=f"publish_vs__home_slide_{i}__sub_title")
                sub_sub_title = st.text_input(f"Stat", key=f"publish_vs__home_slide_{i}__sub_sub_title")

                slides_text.append({
                    "title": title,
                    "stat": stat,
                    "stat_shape": stat,
                    "sub_title": sub_title,
                    "sub_sub_title": sub_sub_title
                })

    # # --- Bouton pour la génération ---
    # if st.button("🚀 Générer le PowerPoint et les images", type="primary"):
    #     st.info("Génération en cours...")
    #     # Appel de la fonction de génération (voir Phase 2)
    #     st.session_state.powerpoint_path, st.session_state.slides_png_paths = generer_ppt_et_png(
    #         template_path, textes_slides
    #     )
    #     st.success(f"Fichier PowerPoint généré : {st.session_state.powerpoint_path}")
    #     st.success("Images PNG générées avec succès !")

    # # --- Étape 4: Publication ---
    # if st.session_state.slides_png_paths:
    #     st.header("4. Publier sur Instagram")
    #     caption = st.text_area("Légende pour le post Instagram", height=100, value="#football #stats")

    #     if st.button("📤 Publier sur Instagram"):
    #         st.info("Connexion à Instagram et publication...")
    #         # Appel de la fonction de publication (voir Phase 4)
    #         publier_sur_instagram(st.session_state.slides_png_paths, caption)
    #         st.success("Post publié avec succès !")
