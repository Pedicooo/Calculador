from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

INGREDIENTES_MASSA = ['Fermento', 'Farinha', 'Leite', 'Leite em Pó', 'Óleo', 'Ovo', 'Sal']
INGREDIENTES_RECHEIO = ['Presunto', 'Queijo', 'Tomate', 'Calabresa', 'Frango', 'Requeijão']
MATERIAIS_EMBALAGEM = ['Papel Alumínio', 'Adesivo', 'Embalagem Plástica']

@app.route('/')
def home():
    return render_template('index.html',
                         ingredientes_massa=INGREDIENTES_MASSA,
                         ingredientes_recheio=INGREDIENTES_RECHEIO,
                         materiais_embalagem=MATERIAIS_EMBALAGEM)

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    
    total_massa = 0
    total_recheio = 0
    total_embalagem = 0
    
    detalhes_massa = []
    for item in dados['massa']:
        custo = (float(item['preco']) / float(item['qtd_total'])) * float(item['qtd_usada'])
        total_massa += custo
        detalhes_massa.append({'nome': item['nome'], 'custo': round(custo, 2)})

    detalhes_recheio = []
    for item in dados['recheio']:
        custo = (float(item['preco']) / float(item['qtd_total'])) * float(item['qtd_usada'])
        total_recheio += custo
        detalhes_recheio.append({'nome': item['nome'], 'custo': round(custo, 2)})

    detalhes_embalagem = []
    for item in dados['embalagem']:
        custo = (float(item['preco']) / float(item['qtd_total'])) * float(item['qtd_usada'])
        total_embalagem += custo
        detalhes_embalagem.append({'nome': item['nome'], 'custo': round(custo, 2)})

    total_geral = total_massa + total_recheio + total_embalagem
    quantidade_salgados = int(dados['quantidade_salgados'])
    custo_por_unidade = total_geral / quantidade_salgados if quantidade_salgados > 0 else 0
    margem_lucro = float(dados['margem_lucro'])
    preco_venda = custo_por_unidade * (1 + (margem_lucro/100))

    return jsonify({
        'detalhes_massa': detalhes_massa,
        'detalhes_recheio': detalhes_recheio,
        'detalhes_embalagem': detalhes_embalagem,
        'total_massa': round(total_massa, 2),
        'total_recheio': round(total_recheio, 2),
        'total_embalagem': round(total_embalagem, 2),
        'total_geral': round(total_geral, 2),
        'custo_por_unidade': round(custo_por_unidade, 2),
        'preco_venda': round(preco_venda, 2)
    })

if __name__ == '__main__':
    app.run(debug=True)