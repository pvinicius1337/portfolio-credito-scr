# Portfólio — Previsão de Inadimplência de Crédito

Projeto de portfólio ponta a ponta usando dados do SCR.data (Banco Central do Brasil).

## Status

Em desenvolvimento — etapa atual: coleta e armazenamento de dados.

## Notas sobre os dados

### `numero_de_operacoes` = -1 (SCR.data, Versão 2)

No arquivo bruto, ~27% das linhas (83.491 de 313.638 em jan/2025) trazem o valor `-1` no campo `numero_de_operacoes`.

- A Metodologia Versão 1 do SCR.data documenta uma regra de sigilo: quando o número de operações é ≤ 15, o valor divulgado é o texto `"<=15"`.
- A Metodologia Versão 2 (a que usamos neste projeto) **não documenta** essa regra explicitamente — o campo é descrito apenas como "número de operações de crédito para um dado recorte de dados".
- Como `-1` é estruturalmente impossível para uma contagem real (nunca existe "-1 operação"), tratamos como uma provável convenção de supressão por sigilo bancário, adaptada da regra da V1 (um código numérico no lugar do texto `"<=15"`).

**Decisão adotada:** convertido para valor ausente (`NaN`, via `pandas.Int64`) na etapa de ingestão, em vez de manter como -1 ou descartar a linha inteira — os demais valores da linha (ex: `carteira_ativa`) continuam válidos e não devem ser perdidos.

**Isso é uma suposição, não um fato confirmado pela documentação oficial do BC.** Se surgir evidência em contrário, revisar este tratamento.