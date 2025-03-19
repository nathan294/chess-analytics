import dash
from dash import html

dash.register_page(__name__, name="home", path="/", redirect_from=["/home"], title=None)


def layout(**kwargs):
    return html.Div(
        className="relative md:bg-[url('/assets/images/home.jpg')] bg-cover bg-no-repeat bg-[right_50%_top_35%] w-full h-full",
        children=[
            html.Div(
                className="md:absolute md:top-[16%] md:left-[16%] flex flex-col p-4 rounded-lg shadow-lg max-w-[800px]",
                children=[
                    html.H1(className="text-3xl md:text-8xl font-semibold", children="Des statistiques détaillées"),
                    html.P(
                        className="mt-12",
                        children=[
                            "Vous êtes curieux d’en savoir plus sur un joueur Chess.com ? Ce site vous permet d’accéder en un instant à toutes ses statistiques détaillées.",
                            html.Br(),
                            html.Ul(
                                className="list-disc ml-12 mt-6",
                                children=[
                                    html.Li(
                                        [
                                            html.B("Historique des parties récentes: "),
                                            "Observez les parties récentes d'un joueur pour avoir une idée de sa forme actuelle.",
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.B("Consultez ses statistiques: "),
                                            "Obtenez en un coup d'oeil les classements d'un joueur et son taux de victoire sur les différents modes de jeu.",
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.B("Suivez ses performances: "),
                                            "Visualisez les motifs de victoires ou de défaites d'un joueur pour en comprendre plus sur la manière dont ses parties se terminent.",
                                        ]
                                    ),
                                    html.Li(
                                        [
                                            html.B("Analysez ses ouvertures les plus communes: "),
                                            "Consultez les résultats d'un joueur ouverture par ouverture.",
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
