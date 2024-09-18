import plotly.express as px
from dash.dependencies import Output
from dash import html

def gerar_cores(n):
    # Paleta de cores categóricas disponíveis no Plotly
    cores_disponiveis = px.colors.qualitative.Antique # Você pode escolher outras paletas como 'D3', 'G10', 'Bold', etc.

    # Replicando a paleta até alcançar o tamanho n
    cores = (cores_disponiveis * ((n // len(cores_disponiveis)) + 1))[:n]
    
    return cores

# Função para criar a lista de opções com os círculos coloridos
def criar_opcoes(dados, cores_personalizadas):
    opcoes = [{"label": "Todos", "value": "Todos"}]
    for nome in dados["NOME"].unique():
        cor = cores_personalizadas.get(nome, 'rgb(0, 0, 0)')  # Cor preta como fallback
        opcoes.append({
            'label': html.Span([
                nome,  # Nome do político
                html.Span(  # Círculo colorido
                    style={
                        'display': 'inline-block',
                        'width': '12px',
                        'height': '12px',
                        'border-radius': '50%',
                        'background-color': cor,
                        'margin-left': '10px'
                    }
                )
            ], style={'display': 'flex', 'justify-content': 'space-between', 'width': '100%'}),
            'value': nome
        })
    return opcoes

def ajustar_intensidade(cor, fator):
    """Retorna a cor ajustada, clareando ou escurecendo de acordo com o fator"""
    cor = cor.lstrip('#')
    rgb = tuple(int(cor[i:i+2], 16) for i in (0, 2, 4))
    ajustado = tuple(min(255, int(c * fator)) for c in rgb)
    return '#{:02x}{:02x}{:02x}'.format(*ajustado)

def make_postcard_output():

    outs = []

    for i in range(1, 4):

        aux = []

        likes = Output(f"likes-{i}", "value")
        comentarios = Output(f"comentarios-{i}", "value")
        impressoes = Output(f"impressoes-{i}", "value")
        liftconteudo = Output(f"lift-conteudo-{i}", "value")
        taxaengajamento = Output(f"taxa-engajamento-{i}", "value")
        compartilhamentos = Output(f"compartilhamentos-{i}", "value")

        aux.append(likes)
        aux.append(comentarios)
        aux.append(impressoes)
        aux.append(liftconteudo)
        aux.append(taxaengajamento)
        aux.append(compartilhamentos)

        outs.extend(aux)
    
    return outs