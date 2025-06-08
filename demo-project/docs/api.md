# API de Pagamentos - Documentação

Versão: 1.0.0

API para processamento de pagamentos e gestão de transações financeiras

## Endpoint: POST /api/v1/payments

Processa um novo pagamento

### Parâmetros:

- amount (number): Valor da transação - Obrigatório
- currency (string): Código da moeda - Opcional (padrão: USD)
- payment_method (string): Método de pagamento - Obrigatório
- customer_id (string): ID do cliente - Obrigatório

### Exemplo de Requisição:

```json
{
  "amount": 100.5,
  "payment_method": "credit_card",
  "customer_id": "cus_123456",
  "currency": "BRL"
}
```

### Exemplo de Resposta:

```json
{
  "transaction_id": "tr_123456",
  "status": "success",
  "amount": 100.5,
  "currency": "BRL"
}
```

