from pyspark.sql.dataframe import DataFrame


def count_movies_by_year(df: DataFrame) -> DataFrame:
    return (
        df.filter((df["type"] == "Movie") & (df["release_year"] != ""))
        .groupBy("release_year")
        .count()
        .orderBy("release_year")
    )


def count_movies_by_country(df: DataFrame) -> DataFrame:
    return (
        df.filter((df["type"] == "Movie") & (df["country"] != ""))
        .groupBy("country")
        .count()
        .orderBy("count", ascending=False)
    )
