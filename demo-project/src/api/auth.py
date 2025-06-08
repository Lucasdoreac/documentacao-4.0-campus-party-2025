"""
Módulo de autenticação da API.
"""

def authenticate(api_key):
    """
    Autentica um usuário com base na API key.
    
    Args:
        api_key: Chave API do usuário
    
    Returns:
        Token de autenticação ou None se falhar
    """
    # Simulação de autenticação
    if api_key and len(api_key) > 10:
        return f"Bearer {api_key[:5]}...{api_key[-5:]}"
    return None
