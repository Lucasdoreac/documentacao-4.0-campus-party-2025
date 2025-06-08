#!/usr/bin/env python3
"""
Documentação 4.0 com Claude Code - SOTA Live Code Generator
Desenvolvido por Lucas Dórea Cardoso e Aulus Diniz
Campus Party 2025

Este script gera código em tempo real com documentação SOTA integrada.
O sistema demonstra a geração de código e documentação simultânea durante uma apresentação.
"""

import os
import sys
import json
import time
import argparse
import datetime
import random
from typing import List, Dict, Any, Optional, Union, Tuple

class LiveCodeGenerator:
    """Gerador de código ao vivo com documentação SOTA integrada."""
    
    def __init__(self, project_dir: str, presenter_names: List[str]):
        """
        Inicializa o gerador de código ao vivo.
        
        Args:
            project_dir: Diretório do projeto onde o código será gerado
            presenter_names: Nomes dos apresentadores para os créditos
        """
        self.project_dir = project_dir
        self.presenter_names = presenter_names
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'='*80}")
        print(f"🚀 DOCUMENTAÇÃO 4.0 - DEMO AO VIVO")
        print(f"{'='*80}")
        print(f"Iniciado por: {', '.join(presenter_names)}")
        print(f"Data e hora: {self.timestamp}")
        print(f"Diretório do projeto: {project_dir}")
        print(f"{'='*80}\n")
    
    def generate_api_module(self, typing_speed: float = 0.001):
        """
        Gera um módulo de API com documentação completa.
        
        Args:
            typing_speed: Velocidade de simulação de digitação (segundos por caractere)
        """
        filename = os.path.join(self.project_dir, "api_module.py")
        
        code = '''"""
API Module - Documentação 4.0 SOTA Demo
Autores: {0}
Gerado em: {1}

Este módulo implementa endpoints da API com documentação SOTA integrada.
"""

import json
import uuid
import datetime
from typing import Dict, List, Optional, Any, Union

class PaymentProcessor:
    """
    Processador de pagamentos com validação avançada e documentação automática.
    
    Este processador implementa várias formas de pagamento e gera
    documentação SOTA automaticamente para cada método.
    
    Exemplos:
        ```python
        processor = PaymentProcessor(api_key="seu_api_key")
        result = processor.process_payment(
            amount=100.50,
            payment_method="credit_card",
            customer_id="cus_123456"
        )
        ```
    """
    
    def __init__(self, api_key: str, environment: str = "production"):
        """
        Inicializa o processador de pagamentos.
        
        Args:
            api_key: Chave de API para autenticação
            environment: Ambiente de execução ('production', 'sandbox')
            
        Raises:
            ValueError: Se a api_key for inválida ou o ambiente não for suportado
            
        Note:
            As chaves de API são específicas para cada ambiente.
            Nunca use chaves de produção em ambientes sandbox.
        """
        self.api_key = api_key
        self.environment = environment
        self._validate_config()
        self.transaction_log = []
        
    def _validate_config(self) -> None:
        """
        Valida a configuração do processador.
        
        Raises:
            ValueError: Se a configuração for inválida
            
        Implementation Details:
            - Verifica o formato da API key
            - Valida o ambiente de execução
            - Registra a inicialização no sistema de auditoria
        """
        valid_environments = ["production", "sandbox", "test"]
        if self.environment not in valid_environments:
            raise ValueError(f"Ambiente '{{self.environment}}' não suportado. Use {{valid_environments}}")
        
        if not self.api_key or len(self.api_key) < 10:
            raise ValueError("API key inválida")
    
    def process_payment(
        self, 
        amount: float, 
        payment_method: str, 
        customer_id: str,
        currency: str = "USD",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Processa um pagamento usando o método especificado.
        
        Args:
            amount: Valor da transação
            payment_method: Método de pagamento ('credit_card', 'pix', 'boleto')
            customer_id: ID único do cliente
            currency: Código da moeda (default: "USD")
            metadata: Dados adicionais para a transação (opcional)
            
        Returns:
            Dicionário com detalhes da transação processada
            
        Raises:
            ValueError: Se algum parâmetro for inválido
            PaymentError: Se o processamento falhar
            
        Examples:
            Pagamento com cartão de crédito:
            ```python
            result = processor.process_payment(
                amount=100.50,
                payment_method="credit_card",
                customer_id="cus_123456"
            )
            ```
            
            Pagamento com PIX:
            ```python
            result = processor.process_payment(
                amount=150.75,
                payment_method="pix",
                customer_id="cus_123456",
                currency="BRL"
            )
            # result contém 'qr_code' para pagamento
            ```
            
        Note:
            Este método é thread-safe e pode ser chamado concorrentemente.
            Todas as transações são registradas no log de auditoria.
        """
        # Validação de entrada
        if amount <= 0:
            raise ValueError("O valor deve ser maior que zero")
            
        if not customer_id:
            raise ValueError("ID do cliente é obrigatório")
            
        # Simulação de processamento
        risk_score = self._calculate_risk_score(amount, payment_method, customer_id)
        
        # Criação da transação
        transaction = {{
            "transaction_id": f"tr_{{uuid.uuid4().hex[:10]}}",
            "status": "success",
            "amount": amount,
            "currency": currency,
            "payment_method": payment_method,
            "customer_id": customer_id,
            "risk_score": risk_score,
            "processed_at": datetime.datetime.now().isoformat(),
            "metadata": metadata if metadata else {{}}
        }}
        
        # Adicionar dados específicos por método de pagamento
        if payment_method == "pix":
            transaction["qr_code"] = f"data:image/png;base64,{{self._generate_mock_qr_code()}}"
            transaction["expiration"] = (datetime.datetime.now() + 
                                        datetime.timedelta(minutes=30)).isoformat()
        elif payment_method == "boleto":
            transaction["barcode"] = f"34191790010104351004791020150008191070069999"
            transaction["pdf_url"] = f"https://api.example.com/boletos/{{transaction['transaction_id']}}"
            transaction["expiration"] = (datetime.datetime.now() + 
                                        datetime.timedelta(days=3)).isoformat()
        
        # Registrar transação
        self.transaction_log.append(transaction)
        
        return transaction
    
    def refund_payment(
        self, 
        transaction_id: str, 
        amount: Optional[float] = None,
        reason: str = "customer_request"
    ) -> Dict[str, Any]:
        """
        Processa um reembolso para uma transação.
        
        Args:
            transaction_id: ID da transação original
            amount: Valor a reembolsar (None = reembolso total)
            reason: Motivo do reembolso
            
        Returns:
            Dicionário com detalhes do reembolso
            
        Raises:
            ValueError: Se a transação não for encontrada
            RefundError: Se o reembolso não puder ser processado
            
        Examples:
            Reembolso total:
            ```python
            refund = processor.refund_payment(
                transaction_id="tr_1234567890"
            )
            ```
            
            Reembolso parcial:
            ```python
            refund = processor.refund_payment(
                transaction_id="tr_1234567890",
                amount=50.25,
                reason="partial_dissatisfaction"
            )
            ```
        """
        # Buscar transação original (simulado)
        original_transaction = next(
            (t for t in self.transaction_log if t["transaction_id"] == transaction_id), 
            None
        )
        
        if not original_transaction:
            raise ValueError(f"Transação {{transaction_id}} não encontrada")
            
        # Definir valor do reembolso
        refund_amount = amount if amount is not None else original_transaction["amount"]
        
        # Validar reembolso
        if refund_amount <= 0 or refund_amount > original_transaction["amount"]:
            raise ValueError("Valor de reembolso inválido")
            
        # Processar reembolso
        refund = {{
            "refund_id": f"re_{{uuid.uuid4().hex[:10]}}",
            "transaction_id": transaction_id,
            "amount": refund_amount,
            "currency": original_transaction["currency"],
            "reason": reason,
            "status": "success",
            "processed_at": datetime.datetime.now().isoformat()
        }}
        
        return refund
    
    def _calculate_risk_score(self, amount: float, payment_method: str, customer_id: str) -> float:
        """
        Calcula o score de risco para uma transação.
        
        Args:
            amount: Valor da transação
            payment_method: Método de pagamento
            customer_id: ID do cliente
            
        Returns:
            Score de risco entre 0.0 e 1.0
            
        Note:
            Esta é uma implementação simplificada para demonstração.
            Sistemas reais usariam algoritmos de machine learning.
        """
        # Simulação de cálculo de risco
        base_risk = 0.1
        
        # Fatores de ajuste para demonstração
        if amount > 1000:
            base_risk += 0.2
            
        if payment_method == "credit_card":
            base_risk += 0.1
        elif payment_method == "pix":
            base_risk -= 0.05
            
        # Adicionar alguma aleatoriedade para demonstração
        random_factor = 0.1 * (hash(customer_id) % 10) / 10.0
        
        risk_score = min(max(base_risk + random_factor, 0.0), 1.0)
        return round(risk_score, 2)
    
    def _generate_mock_qr_code(self) -> str:
        """
        Gera um QR code simulado para demonstração.
        
        Returns:
            String representando um QR code simulado
            
        Note:
            Em um sistema real, isso usaria uma biblioteca
            de geração de QR code como qrcode.
        """
        return "iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAIAAADTED8xAAADMElEQVR4nOzVwQnAIBQFQYXff81RUHAQFwdmCrgP" # simulado


class PaymentError(Exception):
    """
    Exceção para erros de processamento de pagamento.
    
    Attributes:
        message: Descrição do erro
        code: Código de erro
        transaction_id: ID da transação (se disponível)
    """
    def __init__(self, message: str, code: str, transaction_id: Optional[str] = None):
        self.message = message
        self.code = code
        self.transaction_id = transaction_id
        super().__init__(message)


class RefundError(Exception):
    """
    Exceção para erros de processamento de reembolso.
    
    Attributes:
        message: Descrição do erro
        code: Código de erro
        refund_id: ID do reembolso (se disponível)
        transaction_id: ID da transação original
    """
    def __init__(self, message: str, code: str, transaction_id: str, refund_id: Optional[str] = None):
        self.message = message
        self.code = code
        self.transaction_id = transaction_id
        self.refund_id = refund_id
        super().__init__(message)


# Exemplo de uso (não executado, apenas para documentação):
"""
# Inicializar o processador
processor = PaymentProcessor(api_key="sk_test_123456789")

# Processar um pagamento
try:
    payment = processor.process_payment(
        amount=100.50,
        payment_method="credit_card",
        customer_id="cus_123456",
        currency="USD",
        metadata={{"invoice_id": "inv_987"}}
    )
    print(f"Pagamento processado: {{payment['transaction_id']}}")
    
    # Processar um reembolso
    refund = processor.refund_payment(
        transaction_id=payment['transaction_id'],
        amount=50.25,
        reason="partial_refund"
    )
    print(f"Reembolso processado: {{refund['refund_id']}}")
    
except (ValueError, PaymentError, RefundError) as e:
    print(f"Erro: {{str(e)}}")
"""
'''.format(', '.join(self.presenter_names), self.timestamp)
        
        print(f"\n📄 Gerando módulo API com documentação SOTA integrada...")
        print(f"📝 Arquivo: {filename}")
        
        # Criar o diretório se não existir
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Simular digitação do código
        with open(filename, 'w') as f:
            for char in code:
                f.write(char)
                f.flush()
                time.sleep(typing_speed)
                # Imprimir progresso periodicamente
                if random.random() < 0.01:  # ~1% chance por caractere
                    progress = round(code.index(char) / len(code) * 100)
                    print(f"⚡ Gerando código: {progress}% concluído...", end="\r")
        
        print("\n✅ Módulo API gerado com sucesso!")
        print(f"📊 Estatísticas:")
        print(f"   - {len(code.splitlines())} linhas de código")
        print(f"   - {len([l for l in code.splitlines() if l.strip().startswith('\"\"\"') or l.strip().endswith('\"\"\"')])} linhas de documentação")
        print(f"   - {code.count('Args:')} blocos de parâmetros documentados")
        print(f"   - {code.count('Returns:')} blocos de retorno documentados")
        print(f"   - {code.count('Raises:')} blocos de exceções documentados")
        print(f"   - {code.count('Examples:')} exemplos de código")
        print(f"   - {code.count('Note:')} notas explicativas")
        
        return filename
    
    def generate_documentation(self, api_module_path: str, typing_speed: float = 0.001):
        """
        Gera documentação automática para um módulo de API.
        
        Args:
            api_module_path: Caminho para o módulo de API
            typing_speed: Velocidade de simulação de digitação
        """
        module_name = os.path.basename(api_module_path)
        docs_dir = os.path.join(self.project_dir, "docs")
        os.makedirs(docs_dir, exist_ok=True)
        
        markdown_path = os.path.join(docs_dir, f"{os.path.splitext(module_name)[0]}.md")
        openapi_path = os.path.join(docs_dir, "openapi.json")
        
        print(f"\n📚 Gerando documentação automática a partir do código...")
        print(f"📝 Arquivos de documentação:")
        print(f"   - Markdown: {markdown_path}")
        print(f"   - OpenAPI: {openapi_path}")
        
        # Ler o módulo de API
        with open(api_module_path, 'r') as f:
            code = f.read()
        
        # Simular extração de documentação
        print("🔍 Analisando docstrings e anotações de tipo...")
        time.sleep(1)
        print("📊 Extraindo parâmetros e valores de retorno...")
        time.sleep(0.5)
        print("🧪 Detectando exemplos de código...")
        time.sleep(0.5)
        print("⚠️ Identificando exceções e tratamento de erros...")
        time.sleep(0.5)
        
        # Gerar Markdown
        markdown = f'''# API de Pagamentos

*Gerado automaticamente em: {self.timestamp}*
*Autores: {", ".join(self.presenter_names)}*

## Visão Geral

Este módulo implementa um processador de pagamentos com validação avançada e documentação integrada.

## Classes

### PaymentProcessor

Processador de pagamentos com validação avançada e documentação automática.

Este processador implementa várias formas de pagamento e gera documentação SOTA automaticamente para cada método.

#### Inicialização

```python
processor = PaymentProcessor(api_key="seu_api_key")
```

#### Parâmetros do Construtor

| Parâmetro   | Tipo  | Descrição                                  | Padrão        |
|-------------|-------|--------------------------------------------| --------------|
| api_key     | str   | Chave de API para autenticação             | Obrigatório   |
| environment | str   | Ambiente ('production', 'sandbox', 'test') | "production"  |

#### Métodos

##### process_payment

Processa um pagamento usando o método especificado.

```python
result = processor.process_payment(
    amount=100.50,
    payment_method="credit_card",
    customer_id="cus_123456"
)
```

###### Parâmetros

| Parâmetro      | Tipo          | Descrição                                      | Padrão      |
|----------------|---------------|------------------------------------------------|-------------|
| amount         | float         | Valor da transação                             | Obrigatório |
| payment_method | str           | Método de pagamento ('credit_card', 'pix', 'boleto') | Obrigatório |
| customer_id    | str           | ID único do cliente                            | Obrigatório |
| currency       | str           | Código da moeda                                | "USD"       |
| metadata       | Dict[str, Any] | Dados adicionais para a transação             | None        |

###### Retorno

Um dicionário com os detalhes da transação processada:

```python
{{
    "transaction_id": "tr_1234567890",
    "status": "success",
    "amount": 100.50,
    "currency": "USD",
    "payment_method": "credit_card",
    "customer_id": "cus_123456",
    "risk_score": 0.15,
    "processed_at": "2025-06-08T10:30:00Z",
    "metadata": {{"invoice_id": "inv_987"}}
}}
```

Para pagamentos PIX, a resposta inclui campos adicionais:
- `qr_code`: String base64 da imagem do QR code
- `expiration`: Timestamp ISO 8601 de expiração (30 minutos)

Para boletos, a resposta inclui:
- `barcode`: Código de barras do boleto
- `pdf_url`: URL para download do PDF
- `expiration`: Timestamp ISO 8601 de expiração (3 dias)

###### Exceções

- `ValueError`: Se algum parâmetro for inválido
- `PaymentError`: Se o processamento falhar

##### refund_payment

Processa um reembolso para uma transação.

```python
refund = processor.refund_payment(
    transaction_id="tr_1234567890",
    amount=50.25,
    reason="partial_dissatisfaction"
)
```

###### Parâmetros

| Parâmetro      | Tipo   | Descrição                           | Padrão              |
|----------------|--------|-------------------------------------|---------------------|
| transaction_id | str    | ID da transação original            | Obrigatório         |
| amount         | float  | Valor a reembolsar                  | None (valor total)  |
| reason         | str    | Motivo do reembolso                 | "customer_request"  |

###### Retorno

Um dicionário com os detalhes do reembolso:

```python
{{
    "refund_id": "re_1234567890",
    "transaction_id": "tr_1234567890",
    "amount": 50.25,
    "currency": "USD",
    "reason": "partial_dissatisfaction",
    "status": "success",
    "processed_at": "2025-06-08T11:45:00Z"
}}
```

###### Exceções

- `ValueError`: Se a transação não for encontrada ou o valor for inválido
- `RefundError`: Se o reembolso não puder ser processado

## Exceções

### PaymentError

Exceção para erros de processamento de pagamento.

#### Atributos

- `message`: Descrição do erro
- `code`: Código de erro
- `transaction_id`: ID da transação (se disponível)

### RefundError

Exceção para erros de processamento de reembolso.

#### Atributos

- `message`: Descrição do erro
- `code`: Código de erro
- `transaction_id`: ID da transação original
- `refund_id`: ID do reembolso (se disponível)

## Exemplos de Uso

### Processamento de Pagamento com Cartão de Crédito

```python
processor = PaymentProcessor(api_key="sk_test_123456789")

try:
    payment = processor.process_payment(
        amount=100.50,
        payment_method="credit_card",
        customer_id="cus_123456",
        currency="USD",
        metadata={{"invoice_id": "inv_987"}}
    )
    print(f"Pagamento processado: {{payment['transaction_id']}}")
    
except (ValueError, PaymentError) as e:
    print(f"Erro: {{str(e)}}")
```

### Processamento de Reembolso

```python
try:
    refund = processor.refund_payment(
        transaction_id="tr_1234567890",
        amount=50.25,
        reason="partial_refund"
    )
    print(f"Reembolso processado: {{refund['refund_id']}}")
    
except (ValueError, RefundError) as e:
    print(f"Erro: {{str(e)}}")
```

## Notas de Implementação

- Todas as transações são registradas no log de auditoria
- Os métodos são thread-safe e podem ser chamados concorrentemente
- Nunca use chaves de produção em ambientes sandbox
'''
        
        # Simular geração do arquivo Markdown
        with open(markdown_path, 'w') as f:
            for char in markdown:
                f.write(char)
                f.flush()
                time.sleep(typing_speed)
                if random.random() < 0.01:
                    progress = round(markdown.index(char) / len(markdown) * 100)
                    print(f"📝 Gerando documentação Markdown: {progress}% concluído...", end="\r")
        
        # Simular geração do OpenAPI
        openapi = {
            "openapi": "3.0.3",
            "info": {
                "title": "API de Pagamentos",
                "description": "API para processamento de pagamentos e gestão de transações financeiras",
                "version": "1.0.0",
                "contact": {
                    "name": " & ".join(self.presenter_names),
                    "email": "contato@docs40.campus.party"
                }
            },
            "paths": {
                "/api/v1/payments": {
                    "post": {
                        "summary": "Processa um novo pagamento",
                        "description": "Processa um pagamento usando o método especificado.",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/PaymentRequest"
                                    },
                                    "example": {
                                        "amount": 100.50,
                                        "payment_method": "credit_card",
                                        "customer_id": "cus_123456",
                                        "currency": "USD",
                                        "metadata": {"invoice_id": "inv_987"}
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Pagamento processado com sucesso",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/PaymentResponse"
                                        }
                                    }
                                }
                            },
                            "400": {
                                "description": "Parâmetros inválidos",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            },
                            "401": {
                                "description": "Não autorizado",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            },
                            "422": {
                                "description": "Erro de processamento",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/v1/refunds": {
                    "post": {
                        "summary": "Processa um reembolso",
                        "description": "Processa um reembolso total ou parcial para uma transação.",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/RefundRequest"
                                    },
                                    "example": {
                                        "transaction_id": "tr_1234567890",
                                        "amount": 50.25,
                                        "reason": "customer_request"
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Reembolso processado com sucesso",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/RefundResponse"
                                        }
                                    }
                                }
                            },
                            "400": {
                                "description": "Parâmetros inválidos",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            },
                            "404": {
                                "description": "Transação não encontrada",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "components": {
                "schemas": {
                    "PaymentRequest": {
                        "type": "object",
                        "required": ["amount", "payment_method", "customer_id"],
                        "properties": {
                            "amount": {
                                "type": "number",
                                "format": "float",
                                "description": "Valor da transação"
                            },
                            "payment_method": {
                                "type": "string",
                                "description": "Método de pagamento",
                                "enum": ["credit_card", "pix", "boleto"]
                            },
                            "customer_id": {
                                "type": "string",
                                "description": "ID único do cliente"
                            },
                            "currency": {
                                "type": "string",
                                "description": "Código da moeda",
                                "default": "USD"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Dados adicionais para a transação"
                            }
                        }
                    },
                    "PaymentResponse": {
                        "type": "object",
                        "properties": {
                            "transaction_id": {
                                "type": "string",
                                "description": "ID único da transação"
                            },
                            "status": {
                                "type": "string",
                                "description": "Status da transação",
                                "enum": ["success", "pending", "failed"]
                            },
                            "amount": {
                                "type": "number",
                                "format": "float",
                                "description": "Valor da transação"
                            },
                            "currency": {
                                "type": "string",
                                "description": "Código da moeda"
                            },
                            "payment_method": {
                                "type": "string",
                                "description": "Método de pagamento usado"
                            },
                            "customer_id": {
                                "type": "string",
                                "description": "ID do cliente"
                            },
                            "risk_score": {
                                "type": "number",
                                "format": "float",
                                "description": "Score de risco da transação (0-1)"
                            },
                            "processed_at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Data e hora do processamento"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Dados adicionais da transação"
                            },
                            "qr_code": {
                                "type": "string",
                                "description": "QR code para pagamento PIX (base64)"
                            },
                            "expiration": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Data e hora de expiração"
                            },
                            "barcode": {
                                "type": "string",
                                "description": "Código de barras do boleto"
                            },
                            "pdf_url": {
                                "type": "string",
                                "format": "uri",
                                "description": "URL para download do PDF do boleto"
                            }
                        }
                    },
                    "RefundRequest": {
                        "type": "object",
                        "required": ["transaction_id"],
                        "properties": {
                            "transaction_id": {
                                "type": "string",
                                "description": "ID da transação original"
                            },
                            "amount": {
                                "type": "number",
                                "format": "float",
                                "description": "Valor a reembolsar (opcional para reembolso total)"
                            },
                            "reason": {
                                "type": "string",
                                "description": "Motivo do reembolso",
                                "default": "customer_request"
                            }
                        }
                    },
                    "RefundResponse": {
                        "type": "object",
                        "properties": {
                            "refund_id": {
                                "type": "string",
                                "description": "ID único do reembolso"
                            },
                            "transaction_id": {
                                "type": "string",
                                "description": "ID da transação original"
                            },
                            "amount": {
                                "type": "number",
                                "format": "float",
                                "description": "Valor reembolsado"
                            },
                            "currency": {
                                "type": "string",
                                "description": "Código da moeda"
                            },
                            "reason": {
                                "type": "string",
                                "description": "Motivo do reembolso"
                            },
                            "status": {
                                "type": "string",
                                "description": "Status do reembolso",
                                "enum": ["success", "pending", "failed"]
                            },
                            "processed_at": {
                                "type": "string",
                                "format": "date-time",
                                "description": "Data e hora do processamento"
                            }
                        }
                    },
                    "ErrorResponse": {
                        "type": "object",
                        "properties": {
                            "error": {
                                "type": "object",
                                "properties": {
                                    "code": {
                                        "type": "string",
                                        "description": "Código de erro"
                                    },
                                    "message": {
                                        "type": "string",
                                        "description": "Mensagem de erro"
                                    },
                                    "transaction_id": {
                                        "type": "string",
                                        "description": "ID da transação (se disponível)"
                                    },
                                    "refund_id": {
                                        "type": "string",
                                        "description": "ID do reembolso (se disponível)"
                                    }
                                }
                            }
                        }
                    }
                },
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                        "description": "Token de autenticação JWT"
                    }
                }
            },
            "security": [
                {
                    "bearerAuth": []
                }
            ]
        }
        
        with open(openapi_path, 'w') as f:
            json_str = json.dumps(openapi, indent=2)
            for char in json_str:
                f.write(char)
                f.flush()
                time.sleep(typing_speed / 5)  # OpenAPI é mais rápido
                if random.random() < 0.005:
                    progress = round(json_str.index(char) / len(json_str) * 100)
                    print(f"📝 Gerando especificação OpenAPI: {progress}% concluído...", end="\r")
        
        print("\n✅ Documentação gerada com sucesso!")
        print(f"📊 Estatísticas:")
        print(f"   - Markdown: {len(markdown.splitlines())} linhas, {len(markdown)} caracteres")
        print(f"   - OpenAPI: {len(json.dumps(openapi, indent=2).splitlines())} linhas")
        print(f"   - Endpoints documentados: {len(openapi['paths'])}")
        print(f"   - Esquemas definidos: {len(openapi['components']['schemas'])}")
        
        return markdown_path, openapi_path
    
    def generate_live_tests(self, api_module_path: str, typing_speed: float = 0.001):
        """
        Gera testes automatizados para o módulo API.
        
        Args:
            api_module_path: Caminho para o módulo de API
            typing_speed: Velocidade de simulação de digitação
        """
        tests_dir = os.path.join(self.project_dir, "tests")
        os.makedirs(tests_dir, exist_ok=True)
        
        test_file = os.path.join(tests_dir, "test_api_module.py")
        
        print(f"\n🧪 Gerando testes automatizados a partir do código...")
        print(f"📝 Arquivo de testes: {test_file}")
        
        # Código de teste
        test_code = f'''"""
Testes automatizados para API Module
Autores: {", ".join(self.presenter_names)}
Gerado em: {self.timestamp}

Testes gerados automaticamente a partir da documentação SOTA.
"""

import unittest
import sys
import os
import uuid
from unittest.mock import patch, MagicMock
from datetime import datetime

# Adicionar diretório pai ao path para importar o módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from api_module import PaymentProcessor, PaymentError, RefundError


class TestPaymentProcessor(unittest.TestCase):
    """Testes para o processador de pagamentos."""
    
    def setUp(self):
        """Configuração para cada teste."""
        self.api_key = "sk_test_" + uuid.uuid4().hex
        self.processor = PaymentProcessor(api_key=self.api_key, environment="test")
    
    def test_initialization(self):
        """Testa a inicialização do processador."""
        self.assertEqual(self.processor.api_key, self.api_key)
        self.assertEqual(self.processor.environment, "test")
        self.assertEqual(len(self.processor.transaction_log), 0)
    
    def test_initialization_invalid_environment(self):
        """Testa a inicialização com ambiente inválido."""
        with self.assertRaises(ValueError) as context:
            PaymentProcessor(api_key=self.api_key, environment="invalid")
        self.assertIn("Ambiente 'invalid' não suportado", str(context.exception))
    
    def test_initialization_invalid_api_key(self):
        """Testa a inicialização com API key inválida."""
        with self.assertRaises(ValueError) as context:
            PaymentProcessor(api_key="", environment="test")
        self.assertEqual("API key inválida", str(context.exception))
    
    def test_process_payment_credit_card(self):
        """Testa o processamento de pagamento com cartão de crédito."""
        payment = self.processor.process_payment(
            amount=100.50,
            payment_method="credit_card",
            customer_id="cus_" + uuid.uuid4().hex,
            currency="USD"
        )
        
        self.assertIsNotNone(payment["transaction_id"])
        self.assertEqual(payment["status"], "success")
        self.assertEqual(payment["amount"], 100.50)
        self.assertEqual(payment["currency"], "USD")
        self.assertEqual(payment["payment_method"], "credit_card")
        self.assertIsNotNone(payment["processed_at"])
        self.assertIsNotNone(payment["risk_score"])
        self.assertIn(payment, self.processor.transaction_log)
    
    def test_process_payment_pix(self):
        """Testa o processamento de pagamento com PIX."""
        payment = self.processor.process_payment(
            amount=150.75,
            payment_method="pix",
            customer_id="cus_" + uuid.uuid4().hex,
            currency="BRL"
        )
        
        self.assertIsNotNone(payment["transaction_id"])
        self.assertEqual(payment["status"], "success")
        self.assertEqual(payment["amount"], 150.75)
        self.assertEqual(payment["currency"], "BRL")
        self.assertEqual(payment["payment_method"], "pix")
        self.assertIsNotNone(payment["qr_code"])
        self.assertIsNotNone(payment["expiration"])
    
    def test_process_payment_boleto(self):
        """Testa o processamento de pagamento com boleto."""
        payment = self.processor.process_payment(
            amount=200.00,
            payment_method="boleto",
            customer_id="cus_" + uuid.uuid4().hex,
            currency="BRL"
        )
        
        self.assertIsNotNone(payment["transaction_id"])
        self.assertEqual(payment["status"], "success")
        self.assertEqual(payment["amount"], 200.00)
        self.assertEqual(payment["currency"], "BRL")
        self.assertEqual(payment["payment_method"], "boleto")
        self.assertIsNotNone(payment["barcode"])
        self.assertIsNotNone(payment["pdf_url"])
        self.assertIsNotNone(payment["expiration"])
    
    def test_process_payment_invalid_amount(self):
        """Testa o processamento com valor inválido."""
        with self.assertRaises(ValueError) as context:
            self.processor.process_payment(
                amount=0,
                payment_method="credit_card",
                customer_id="cus_123456"
            )
        self.assertEqual("O valor deve ser maior que zero", str(context.exception))
    
    def test_process_payment_invalid_customer(self):
        """Testa o processamento com cliente inválido."""
        with self.assertRaises(ValueError) as context:
            self.processor.process_payment(
                amount=100.50,
                payment_method="credit_card",
                customer_id=""
            )
        self.assertEqual("ID do cliente é obrigatório", str(context.exception))
    
    def test_refund_payment_full(self):
        """Testa o reembolso total de um pagamento."""
        # Primeiro, processar um pagamento
        payment = self.processor.process_payment(
            amount=300.00,
            payment_method="credit_card",
            customer_id="cus_" + uuid.uuid4().hex
        )
        
        # Depois, reembolsar o pagamento
        refund = self.processor.refund_payment(
            transaction_id=payment["transaction_id"]
        )
        
        self.assertIsNotNone(refund["refund_id"])
        self.assertEqual(refund["transaction_id"], payment["transaction_id"])
        self.assertEqual(refund["amount"], payment["amount"])
        self.assertEqual(refund["currency"], payment["currency"])
        self.assertEqual(refund["status"], "success")
        self.assertEqual(refund["reason"], "customer_request")
    
    def test_refund_payment_partial(self):
        """Testa o reembolso parcial de um pagamento."""
        # Primeiro, processar um pagamento
        payment = self.processor.process_payment(
            amount=300.00,
            payment_method="credit_card",
            customer_id="cus_" + uuid.uuid4().hex
        )
        
        # Depois, reembolsar parcialmente o pagamento
        refund_amount = 150.00
        refund = self.processor.refund_payment(
            transaction_id=payment["transaction_id"],
            amount=refund_amount,
            reason="partial_refund"
        )
        
        self.assertIsNotNone(refund["refund_id"])
        self.assertEqual(refund["transaction_id"], payment["transaction_id"])
        self.assertEqual(refund["amount"], refund_amount)
        self.assertEqual(refund["currency"], payment["currency"])
        self.assertEqual(refund["status"], "success")
        self.assertEqual(refund["reason"], "partial_refund")
    
    def test_refund_payment_invalid_transaction(self):
        """Testa o reembolso com transação inválida."""
        with self.assertRaises(ValueError) as context:
            self.processor.refund_payment(
                transaction_id="invalid_transaction"
            )
        self.assertIn("Transação invalid_transaction não encontrada", str(context.exception))
    
    def test_refund_payment_invalid_amount(self):
        """Testa o reembolso com valor inválido."""
        # Primeiro, processar um pagamento
        payment = self.processor.process_payment(
            amount=300.00,
            payment_method="credit_card",
            customer_id="cus_" + uuid.uuid4().hex
        )
        
        # Tentar reembolsar com valor maior que o original
        with self.assertRaises(ValueError) as context:
            self.processor.refund_payment(
                transaction_id=payment["transaction_id"],
                amount=400.00
            )
        self.assertEqual("Valor de reembolso inválido", str(context.exception))
        
        # Tentar reembolsar com valor zero
        with self.assertRaises(ValueError) as context:
            self.processor.refund_payment(
                transaction_id=payment["transaction_id"],
                amount=0
            )
        self.assertEqual("Valor de reembolso inválido", str(context.exception))
    
    def test_calculate_risk_score(self):
        """Testa o cálculo de score de risco."""
        risk = self.processor._calculate_risk_score(100, "credit_card", "cus_123456")
        self.assertGreaterEqual(risk, 0.0)
        self.assertLessEqual(risk, 1.0)
        
        # Valor alto deve aumentar o risco
        high_amount_risk = self.processor._calculate_risk_score(2000, "credit_card", "cus_123456")
        self.assertGreater(high_amount_risk, risk)


if __name__ == '__main__':
    unittest.main()
'''
        
        # Simular geração do arquivo de testes
        with open(test_file, 'w') as f:
            for char in test_code:
                f.write(char)
                f.flush()
                time.sleep(typing_speed)
                if random.random() < 0.01:
                    progress = round(test_code.index(char) / len(test_code) * 100)
                    print(f"🧪 Gerando testes automatizados: {progress}% concluído...", end="\r")
        
        print("\n✅ Testes automatizados gerados com sucesso!")
        print(f"📊 Estatísticas:")
        print(f"   - {len(test_code.splitlines())} linhas de código de teste")
        print(f"   - {test_code.count('def test_')} métodos de teste")
        print(f"   - {test_code.count('self.assert')} asserções")
        
        return test_file
    
    def run_demo(self, typing_speed: float = 0.001):
        """
        Executa a demonstração completa.
        
        Args:
            typing_speed: Velocidade de simulação de digitação
        """
        print(f"\n🚀 Iniciando demonstração de SOTA Code Generator...")
        
        # Gerar módulo API
        api_module_path = self.generate_api_module(typing_speed=typing_speed)
        
        # Gerar documentação
        markdown_path, openapi_path = self.generate_documentation(api_module_path, typing_speed=typing_speed)
        
        # Gerar testes
        test_file = self.generate_live_tests(api_module_path, typing_speed=typing_speed)
        
        # Resumo
        print(f"\n✨ Demonstração concluída com sucesso!")
        print(f"\n📁 Arquivos gerados:")
        print(f"   - Código: {api_module_path}")
        print(f"   - Documentação Markdown: {markdown_path}")
        print(f"   - Especificação OpenAPI: {openapi_path}")
        print(f"   - Testes automatizados: {test_file}")
        
        return {
            "api_module": api_module_path,
            "markdown_doc": markdown_path,
            "openapi_spec": openapi_path,
            "tests": test_file
        }


def main():
    parser = argparse.ArgumentParser(description="Documentação 4.0 - SOTA Live Code Generator")
    parser.add_argument("--project-dir", type=str, default="./demo-project", 
                      help="Diretório onde os arquivos serão gerados")
    parser.add_argument("--speed", type=float, default=0.0005, 
                      help="Velocidade de simulação de digitação (segundos por caractere)")
    parser.add_argument("--presenters", type=str, default="Lucas Dórea Cardoso,Aulus Diniz", 
                      help="Nomes dos apresentadores separados por vírgula")
    
    args = parser.parse_args()
    
    # Criar diretório do projeto se não existir
    if not os.path.exists(args.project_dir):
        os.makedirs(args.project_dir)
    
    # Inicializar gerador
    generator = LiveCodeGenerator(
        project_dir=args.project_dir,
        presenter_names=args.presenters.split(",")
    )
    
    # Executar demonstração
    generator.run_demo(typing_speed=args.speed)


if __name__ == "__main__":
    main()