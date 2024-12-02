from pyspark.sql.functions import col

def process_data(df):
    # Realiza algunas transformaciones sobre los datos
    processed_df = df.filter(col("event_type") == "Pass") \
                     .withColumn("pass_length", 
                                (col("pass_end_location").cast("string").substr(1, 2).cast("double") - 
                                 col("location").cast("string").substr(1, 2).cast("double")))
    return processed_df
