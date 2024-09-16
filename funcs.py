import plotly.express as px

def gerar_cores(n):
    # Paleta de cores categóricas disponíveis no Plotly
    cores_disponiveis = px.colors.qualitative.Antique # Você pode escolher outras paletas como 'D3', 'G10', 'Bold', etc.

    # Replicando a paleta até alcançar o tamanho n
    cores = (cores_disponiveis * ((n // len(cores_disponiveis)) + 1))[:n]
    
    return cores

def ajustar_intensidade(cor, fator):
    """Retorna a cor ajustada, clareando ou escurecendo de acordo com o fator"""
    cor = cor.lstrip('#')
    rgb = tuple(int(cor[i:i+2], 16) for i in (0, 2, 4))
    ajustado = tuple(min(255, int(c * fator)) for c in rgb)
    return '#{:02x}{:02x}{:02x}'.format(*ajustado)

