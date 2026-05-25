# JurisView

Plataforma que traduz processos do Juizado Especial Cível (JEC) para linguagem simples, com análise jurimétrica baseada em dados reais do CNJ.

## Como rodar

```bash
cd jurisview/backend
pip install -r ../requirements.txt
# Edite .env e coloque sua ANTHROPIC_API_KEY
python app.py
```

Em outro terminal/explorador, abra `jurisview/frontend/index.html` no navegador
(duplo clique funciona — o frontend chama `http://localhost:5000`).

## Arquitetura

```
 ┌──────────┐   POST /analisar   ┌──────────────┐
 │ Frontend │ ─────────────────► │ Flask backend│
 │  (HTML)  │ ◄───────────────── │   app.py     │
 └──────────┘     JSON           └──┬────────┬──┘
                                    │        │
                          ┌─────────▼──┐  ┌──▼────────────┐
                          │ DataJud CNJ│  │ Anthropic API │
                          │ (REST/ES)  │  │ (Claude Sonnet)│
                          └────────────┘  └───────────────┘
```

## Números de processo para teste

Use processos públicos reais. Sugestão: portal do TJSP
(`https://esaj.tjsp.jus.br/cpopg/open.do`) — copie o número CNJ completo de
qualquer processo público do JEC.

Tenha pronto para o demo:
- 1 processo em fase de conciliação
- 1 com sentença proferida
- 1 com recurso em andamento (grau G2)

## Fontes dos dados

- Movimentações processuais: **DataJud CNJ** (API pública, tempo quase-real)
- Estatísticas de prazo: **CNJ Justiça em Números 2024**
- Jurisprudência: **Súmulas STJ**, **TJSP 2024**, **CDC**

## Limites

- DataJud tem defasagem de horas/dias.
- Estimativas de prazo são médias do CNJ, não garantias.
- Estimativas de êxito são baseadas em jurisprudência consolidada, não no caso específico.
- Processos em segredo de justiça não aparecem na API.
- **Não substitui orientação jurídica profissional.**
