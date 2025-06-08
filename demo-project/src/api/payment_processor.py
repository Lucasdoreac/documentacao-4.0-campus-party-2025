"""
Módulo de processamento de pagamentos.
"""

def process_payment(amount, payment_method, customer_id, currency="USD"):
    """
    Processa um pagamento usando o método especificado.
    
    Args:
        amount: Valor da transação
        payment_method: Método de pagamento
        customer_id: ID do cliente
        currency: Código da moeda (padrão: USD)
    
    Returns:
        Dicionário com detalhes da transação
    """
    # Validação avançada de segurança
    if not validate_payment_security(amount, payment_method, customer_id):
        raise SecurityError("Falha na validação de segurança")
        
    # Nova validação anti-fraude
    risk_score = calculate_fraud_risk(customer_id, amount, payment_method)
    if risk_score > 0.8:
        raise FraudSuspicionError("Alto risco de fraude detectado")
    
    # Processamento normal
    # ...código omitido para brevidade...
    
    return {
        "transaction_id": "tr_123456",
        "status": "success",
        "amount": amount,
        "currency": currency,
        "risk_score": risk_score  # Novo campo adicionado
    }

def validate_payment_security(amount, payment_method, customer_id):
    """Valida a segurança do pagamento.""    # Implementação fictícia
    return True

def calculate_fraud_risk(customer_id, amount, payment_method):
    """Calcula o risco de fraude.""    # Implementação fictícia
    return 0.2
