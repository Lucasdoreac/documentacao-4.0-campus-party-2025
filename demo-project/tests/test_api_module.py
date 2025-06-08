"""
Testes automatizados para API Module
Autores: Lucas Dórea Cardoso, Aulus Diniz
Gerado em: 2025-06-08 17:31:14

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
