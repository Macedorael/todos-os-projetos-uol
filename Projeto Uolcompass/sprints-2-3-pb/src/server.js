//import {abrirModal} from './public/js/modal.js'
const express = require('express');
const { engine } = require('express-handlebars');
const app = express();
const port = 3000;
const previsaoAPI = require('./routes/previsao');

// Configuração do middleware e rotas
app.engine('handlebars', engine({ extname: '.hbs', defaultLayout: 'index' }));
app.set('view engine', '.hbs');
app.set('views', './views');   // Diretório onde os arquivos .hbs estão localizados

app.use(express.static('public'));

// Rota para renderizar a página inicial
app.get('/', (req, res) => {
  res.render('index');//
});

// Rota para processar a busca da cidade
app.get('/search', async (req, res) => {
  try {
    const cidade = req.query.cidade; // Obtém o nome da cidade do query string
    const bairro = req.query.bairro.toUpperCase();
    const tratamentoRegex = /^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$/;

     if (!tratamentoRegex.test(cidade)|| !tratamentoRegex.test(bairro)) { 
       return res.status(400).send('Cidade ou bairro com erro de preenchimento. Por favor, preencha corretamente.');
     }
    // Chama a função para obter os dados da previsão do tempo
    const previsao = await previsaoAPI.obterPrevisao(cidade,bairro);

    // Renderiza novamente o template index.hbs com os dados da cidade e da previsão do tempo
    res.render('index', { cidade, previsao, bairro });
  
  } catch (error) {
    console.error('Erro ao mostrar a previsão do tempo:', error);
    res.status(500).send('Cidade ou bairro com erro de preenchimento. Por favor, preencha corretamente.');
  }
  
});


// Inicia o servidor
app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
