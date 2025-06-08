# API de Pagamentos

*Gerado automaticamente em: 2025-06-08 17:31:14*
*Autores: Lucas Dórea Cardoso, Aulus Diniz*

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
{
    "transaction_id": "tr_1234567890",
    "status": "success",
    "amount": 100.50,
    "currency": "USD",
    "payment_method": "credit_card",
    "customer_id": "cus_123456",
    "risk_score": 0.15,
    "processed_at": "2025-06-08T10:30:00Z",
    "metadata": {"invoice_id": "inv_987"}
}
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
{
    "refund_id": "re_1234567890",
    "transaction_id": "tr_1234567890",
    "amount": 50.25,
    "currency": "USD",
    "reason": "partial_dissatisfaction",
    "status": "success",
    "processed_at": "2025-06-08T11:45:00Z"
}
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
        metadata={"invoice_id": "inv_987"}
    )
    print(f"Pagamento processado: {payment['transaction_id']}")
    
except (ValueError, PaymentError) as e:
    print(f"Erro: {str(e)}")
```

### Processamento de Reembolso

```python
try:
    refund = processor.refund_payment(
        transaction_id="tr_1234567890",
        amount=50.25,
        reason="partial_refund"
    )
    print(f"Reembolso processado: {refund['refund_id']}")
    
except (ValueError, RefundError) as e:
    print(f"Erro: {str(e)}")
```

## Notas de Implementação

- Todas as transações são registradas no log de auditoria
- Os métodos são thread-safe e podem ser chamados concorrentemente
- Nunca use chaves de produção em ambientes sandbox
