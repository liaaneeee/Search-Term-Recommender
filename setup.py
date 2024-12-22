from setuptools import setup, find_packages

setup(
    name="Search Term Recommender",
    packages=find_packages(),
    package_data={"searchtermRecommender": ["icons/*.svg"]},
    entry_points={
        "orange.widgets": (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/example/widgets/__init__.py
        "Search Term Recommender = searchtermRecommender",),

        # Register widget help
        "orange.canvas.help": (
            "html-index = searchtermRecommender:WIDGET_HELP_PATH",)
    },
)