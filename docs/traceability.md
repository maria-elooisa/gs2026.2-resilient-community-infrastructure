# Rastreabilidade dos requisitos do desafio

Esta tabela diferencia o que o repositório demonstra hoje do que precisa ser implementado ou medido antes da entrega. Nenhuma linha marcada como pendente deve ser descrita como teste concluído.

| Requisito | Estado neste protótipo | Evidência / próximo passo |
|---|---|---|
| RT-01 a RT-03 — camadas, autonomia local, redundância/modo degradado | Parcial | `edge/store_forward.py` modela buffer offline e replay. Desenhar nós por espaço e demonstrar ensaio de WAN de 30 min (RT-23). |
| RT-04 e RT-05 — certificado único, mTLS, revogação e rotação | Pendente | Criar CA da equipe, certificados distintos, configuração Mosquitto `require_certificate true`, teste de cliente válido/inválido e revogação. |
| RT-06 e RT-07 — VPN, MFA administrativo, segmentação | Pendente | Montar topologia WireGuard isolada, MFA no bastião e evidência de ACL/rotas. Nunca publicar serviço administrativo. |
| RT-08 — SQL Injection antes/depois | Demonstração local inicial | Rotas vulnerável e corrigida em `app/database.py`; repetir o payload local e anexar respostas/logs ao E3. |
| RT-09 — MFA e RBAC | Pendente | Adicionar autenticação e perfis do painel, com evidência por perfil. |
| RT-10 e RT-11 — SPF/DKIM/DMARC e phishing simulado | Apenas dados de exemplo | `data/phishing_metrics.csv` é fixture sintética, não resultado de campanha. Configurar domínio de laboratório e contas fictícias consentidas; registrar métricas reais. |
| RT-12 e RT-13 — logs centralizados, NTP e quatro detecções | Parcial | `detection/rules.py` implementa quatro regras de demonstração. Integrar fontes, sincronismo e SIEM; validar alertas e horários. |
| RT-14 — forense, hash, custódia e ATT&CK | Parcial | `forensics/incident_events.jsonl` é cenário sintético. Gerar manifesto, consolidar timeline e mapear técnicas no laudo. |
| RT-15 — resposta automatizada com aprovação humana | Pendente | Implementar ações reversíveis de baixo risco e gate de aprovação para impacto alto; demonstrar em sandbox. |
| RT-16 — IA defensiva com métricas | Pendente | Treinar e avaliar detector com telemetria sintética; reportar precisão, revocação e falsos positivos. |
| RT-17 — guardrails para LLM, se utilizado | Fora do escopo inicial | Só necessário se o grupo incluir LLM; testar injeção e vazamento, sem acesso a atuadores. |
| RT-18 — phishing/voz sintética | Planejado | Documentar palavra-código, validação fora de banda e treinamento. Conteúdo sintético e consentido. |
| RT-19 a RT-21 — privacidade, custos, manutenção e acessibilidade | Pendente no pacote E2 | Usar dados sintéticos; finalizar RIPD, custos de 12 meses, responsáveis e avaliação WCAG 2.1 AA no relatório. |
| RT-22 e RT-23 — métricas e caos WAN ≥ 30 min | Teste unitário parcial; medição real pendente | Registrar disponibilidade, MTTD, MTTR, autonomia, reconciliação e CPU/RAM/banda/energia durante interrupção controlada. |

## Evidências para E3/E4

Registre data/hora, versão do código e identificador do cenário. Remova tokens e dados pessoais. Guarde evidências locais em `artifacts/`, ignorado pelo Git, e revise/sanitize arquivos antes de anexá-los aos PDFs da entrega.
