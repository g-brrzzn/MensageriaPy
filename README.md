# MensageriaPY

O sistema garante que cada mensagem seja registrada com um carimbo lógico no momento do envio e do consumo, armazenada em um buffer de mensagens, e que suporte transmissão unicast, multicast e broadcast. Cada entrada do log identifica o produtor e o consumidor, juntamente com seus respectivos carimbos de tempo, para fins de conferência.

## Visão Geral

- **Mensageria Distribuída:** Implementa um barramento de mensagens que possibilita a comunicação distribuída entre clientes.
- **Carimbos Lógicos:** As mensagens recebem timestamps lógicos no envio e no consumo para garantir a ordenação.
- **Buffer de Mensagens:** Armazena mensagens com identificadores do produtor; no consumo, registra o consumidor e o timestamp correspondente.
- **Modos de Transmissão:** Suporta unicast, multicast e broadcast.
- **Nomeação de Clientes e Canais:** Facilita a identificação e agrupamento de clientes e canais de comunicação.
- **Log:** Utiliza um arquivo de texto simples para registrar eventos, atendendo aos requisitos de auditoria sem a necessidade de um banco de dados.

## Planejamento Ágil

O projeto foi planejado utilizando metodologias Scrum com os seguintes itens principais:
- **Histórias de Usuário:**
  - *Como usuário, posso enviar mensagens para um ou múltiplos destinatários (unicast, multicast, broadcast).*
  - *Como usuário, desejo que cada mensagem tenha um carimbo lógico para garantir a ordenação correta.*
  - *Como administrador, desejo que o sistema opere de forma distribuída.*
  - *Como auditor, desejo um log que registre o produtor, o consumidor e os timestamps de cada mensagem.*
  - *Como usuário, desejo a nomeação clara de clientes e canais.*
- **Divisão das Sprints:**
  - **Sprint 1:** Configuração das classes básicas de mensagens e comunicação.
  - **Sprint 2:** Integração com o corretor de mensagens, adição de carimbos lógicos e registro em log.
  - **Sprint 3:** Implementação da nomeação de clientes/canais, interface gráfica (opcional) e protocolo de testes.

## Protocolo de Testes

O sistema foi testado com os seguintes procedimentos:
- **Teste de Unicast:** Verificar se mensagens enviadas por um usuário são entregues apenas ao destinatário indicado e registradas com os carimbos lógicos corretos.
- **Teste de Multicast:** Assegurar que mensagens destinadas a múltiplos destinatários sejam entregues e registradas corretamente.
- **Teste de Broadcast:** Confirmar que mensagens broadcast em um canal alcancem todos os usuários registrados nesse canal.
- **Teste de Carimbos Lógicos:** Comparar os timestamps de envio e consumo para manter a ordem.
- **Verificação de Log:** Checar o arquivo de log para confirmar que as entradas registram corretamente os dados do produtor, consumidor e os timestamps.

## Instalação e Execução

1. Clone o repositório:
   ```bash
   git clone github.com/g-brrzzn/MensageriaPy
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd MensageriaPY
   ```
3. Execute o projeto:
   ```bash
   python mensageria_main.py
   ```
4. Verifique o arquivo `registro_mensagens.txt` para conferir os detalhes do log.

---
