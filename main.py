import os
import polars as pl

caminho_entrada = r"aruivos_em_csv/pasta"
caminho_saida = r"_parquet"

os.makedirs(caminho_saida, exist_ok=True)
caminho_parquet = os.path.join(caminho_saida, "Oodo_func_2026_parquet.parquet")

dfs = []

for raiz, _, arquivos in os.walk(caminho_entrada):
    if caminho_saida in raiz:
        continue
    for arquivo in arquivos:
        if arquivo.lower().endswith(".csv"):
            caminho_csv = os.path.join(raiz, arquivo)
            nome_limpo = arquivo[:-4] if arquivo.lower().endswith(".csv") else arquivo
            df = pl.read_csv(
                caminho_csv,
                infer_schema_length=10000,
                ignore_errors=True,
            ).with_columns(
                pl.lit(nome_limpo).alias("nome_do_arquivo")
            )
            dfs.append(df)
            print(f"Lido: {arquivo}")

if dfs:
    df_final = pl.concat(dfs, how="diagonal_relaxed")
    df_final.write_parquet(caminho_parquet, compression="snappy")
    print(f"Salvo com sucesso: {caminho_parquet}")