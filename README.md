# GS Cyber 2026.2 — Resilient Community Infrastructure

Laboratório local e isolado para o protótipo E2 e para preparar evidências dos testes E3/E4. Todos os registros e identidades usados aqui são fictícios. O ambiente não envia e-mails, não acessa sistemas externos e publica o painel somente em `127.0.0.1`.

## Requisitos

- Python 3.11 ou superior, para executar o painel e os testes locais.
- Docker Desktop com Docker Compose v2, como opção para iniciar o painel em container.

## Início rápido

```powershell
docker compose up --build
```

Abra `http://127.0.0.1:8080/`. Para encerrar, use `Ctrl+C` e depois `docker compose down`.

Sem Docker, inicie o painel diretamente com Python:

```powershell
python -m app.server
```

O painel oferece `/health`, `/access-history/vulnerable?q=...` e `/access-history/fixed?q=...`. Os dois últimos caminhos consultam somente dados sintéticos. A rota vulnerável existe exclusivamente para demonstrar a falha no próprio laboratório; não a exponha à rede.

## Demonstração local de SQL Injection

Em outro terminal PowerShell:

```powershell
curl.exe --get --data-urlencode "q=' OR '1'='1" http://127.0.0.1:8080/access-history/vulnerable
curl.exe --get --data-urlencode "q=' OR '1'='1" http://127.0.0.1:8080/access-history/fixed
```

A primeira consulta retorna os registros sintéticos. A segunda trata o conteúdo como texto e não retorna registros. Salve as respostas e horários como evidência; não use alvos externos nem credenciais reais.

## Testes automatizados

```powershell
python -m unittest discover -s tests -v
```

Os testes verificam a diferença entre as consultas vulnerável e parametrizada, o buffer local durante uma interrupção simulada, a reconciliação idempotente e a detecção dos quatro eventos mínimos do cenário.

## Componentes do protótipo

- `app/`: painel web e consultas SQLite com conjunto de dados sintéticos.
- `edge/`: modelo de borda offline-first, fila local SQLite e reconciliação idempotente.
- `detection/`: regras locais para login VPN anômalo, padrão de SQL Injection, certificado inválido e comando de atuador fora do perfil.
- `forensics/`: eventos sintéticos do INC-VA-0712 e ferramenta para gerar hash SHA-256, manifesto e cadeia de custódia inicial.
- `data/`: dados exclusivamente fictícios para demonstrações e campanha simulada.
- `tests/`: testes repetíveis sem acessar a Internet.
- `docs/`: matriz de rastreabilidade entre requisitos do professor e evidências que a equipe ainda precisa produzir.

## Evidências forenses de exemplo

```powershell
python forensics/create_evidence.py --collector equipe-lab --location maquina-local
```

O comando cria arquivos em `artifacts/` com horários UTC, hashes e campos de cadeia de custódia. Substitua os campos de coletor por integrantes reais somente no relatório final; não inclua dados pessoais no repositório público.

## Teste de continuidade

O teste de unidade prova rapidamente o comportamento do buffer e da reconciliação. Para cumprir RT-23, a equipe ainda precisa executar e registrar uma interrupção real e controlada do enlace do laboratório por pelo menos 30 minutos, medir disponibilidade, MTTD, MTTR, autonomia e perda, e guardar os resultados em `artifacts/`. Não interrompa a conexão de produção ou de terceiros.

## Segurança do repositório

- Não coloque chaves privadas, senhas, tokens, dados pessoais ou credenciais reais no Git.
- O Compose vincula a porta do painel ao loopback (`127.0.0.1`). Preserve essa configuração.
- A demonstração ofensiva deve permanecer confinada ao serviço vulnerável deste Compose.
- `artifacts/` é ignorado pelo Git para evitar publicar evidências ainda não revisadas.

## Escopo e próximos passos

Este repositório é a base executável do E2, não uma alegação de que todos os RTs já foram implementados. A matriz `docs/traceability.md` separa o que o protótipo demonstra do que ainda requer configuração, teste ou evidência. Em particular, emissão e revogação de certificados mTLS, VPN WireGuard com MFA administrativo, SPF/DKIM/DMARC, campanha de phishing com contas fictícias, SIEM, IA defensiva com métricas, RIPD, custos, acessibilidade e teste WAN de 30 minutos precisam de configuração e evidências adicionais antes da entrega final.
