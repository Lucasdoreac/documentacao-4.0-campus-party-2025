# Documentação 4.0 na Era IA - Campus Party 2025

Este repositório contém todos os materiais para a apresentação "Documentação 4.0 na Era IA: Do Zero ao Avançado" da Campus Party 2025, por Lucas Dórea Cardoso e Aulus Diniz.

🌐 **[Acesse a apresentação online](https://lucasdoreac.github.io/documentacao-4.0-campus-party-2025/)** 🌐

Para instruções detalhadas, veja o [Guia de Uso](./COMO-USAR.md).

## 📚 Conteúdo Principal

### 📖 Documentação e Apresentação
- **[doc40-guia-pratico.md](./doc40-guia-pratico.md)**: Guia prático completo para implementar Documentação 4.0
- **[doc40-slides-atualizados.html](./doc40-slides-atualizados.html)**: Apresentação de slides usada na Campus Party

### 🔧 Scripts de Demo e Instalação
- **[doc40-instalacao-rapida.sh](./doc40-instalacao-rapida.sh)**: Script de instalação rápida para o ambiente de Documentação 4.0
- **[doc40-live-code-generator.py](./doc40-live-code-generator.py)**: Demonstração de geração de código com documentação integrada
- **[doc40-auto-demo-rapido.sh](./doc40-auto-demo-rapido.sh)**: Script de demonstração automática (versão rápida)
- **[doc40-auto-demo-simples.sh](./doc40-auto-demo-simples.sh)**: Script de demonstração automática (versão completa)

### 💻 Implementações Completas
- **[doc40-sistema.py](./doc40-sistema.py)**: Sistema completo com interface interativa que integra todos os componentes
- **[doc40-consulta.py](./doc40-consulta.py)**: Módulo de consulta à documentação usando busca agêntica
- **[doc40-gerador.py](./doc40-gerador.py)**: Módulo de geração de documentação a partir do código
- **[doc40-agente.py](./doc40-agente.py)**: Agente de manutenção de documentação
- **[doc40-completo.py](./doc40-completo.py)**: Implementação tudo-em-um do sistema com todas as funcionalidades

### 🧪 Recursos Adicionais
- **[demo-project/](./demo-project/)**: Projeto de exemplo para demonstrações
- **[publicar-github.sh](./publicar-github.sh)**: Script para publicar este projeto no seu GitHub
- **[IMPLEMENTACAO-COMPLETA.md](./IMPLEMENTACAO-COMPLETA.md)**: Detalhes sobre a implementação completa

## 🚀 Começando

Para começar a usar os recursos deste repositório:

1. Veja a apresentação de slides: `./doc40-slides-atualizados.html`
2. Leia o guia prático completo: `./doc40-guia-pratico.md`
3. Execute o script de instalação rápida: `./doc40-instalacao-rapida.sh`
4. Experimente a demonstração automática: `./doc40-auto-demo-rapido.sh`

## 🎥 Demonstração Automática

Para ver uma demonstração completa e automática do sistema de Documentação 4.0:

```bash
# Versão rápida (para testes)
./doc40-auto-demo-rapido.sh

# Versão completa (para apresentações)
./doc40-auto-demo-simples.sh

# Sistema interativo completo
python doc40-sistema.py

# Módulos individuais
python doc40-consulta.py --query "Como funciona a autenticação?"
python doc40-gerador.py geral --dir ./meu-projeto
python doc40-agente.py iniciar --intervalo 300
```

A demonstração mostrará:
1. Consulta à documentação usando busca agêntica
2. Geração automática de documentação
3. Agente de manutenção de documentação
4. Geração de código com documentação integrada

## ⚙️ Requisitos

- macOS, Linux ou Windows
- Bash ou shell compatível
- Python 3.8 ou superior
- Git
- Conta na Anthropic para a API do Claude
- Navegador web moderno

## 🔧 Instalação

```bash
# Executar o script de instalação rápida
./doc40-instalacao-rapida.sh

# Ou instalar manualmente:

# Instalar Claude Code CLI
curl -sSL https://raw.githubusercontent.com/anthropic/claude-code/main/install.sh | bash

# Verificar a instalação
claude-code --version

# Configurar a chave API
claude-code config set api_key sk_ant_...

# Instalar dependências Python
pip install anthropic python-dotenv requests click rich
```

## 🛠️ Componentes do Sistema

O sistema de Documentação 4.0 com Claude Code inclui:

1. **Busca Agêntica**: Consultas em linguagem natural sobre o código
2. **Geração Automática**: Documentação completa gerada a partir do código
3. **Manutenção Automática**: Atualização da documentação ao mudar o código
4. **Geração de Código**: Código e documentação nascem juntos
5. **Integração Contínua**: Tudo integrado ao fluxo de desenvolvimento

## 🙏 Agradecimentos

- Anthropic, por fornecer acesso ao Claude Code
- Equipe da Campus Party Brasil
- Todos os participantes da sessão

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

Criado por Lucas Dórea Cardoso e Aulus Diniz para a Campus Party 2025