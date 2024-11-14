//Contruct objeto usuário
function criarUsuario(nome, telefone, email, nascimento) {
    return {
        nome: nome,
        telefone: telefone,
        email: email,
        nascimento: nascimento
    };
}

function limparFormulario() {
    document.getElementById('cadastroForm').reset();
    exibirUsuarios();
}
// Função para cadastrar usuário
function cadastrar() {
    
    let nome = document.getElementById('id_nome').value;
    let telefone = document.getElementById('id_telefone').value;
    let email = document.getElementById('id_email').value;
    let nascimento = document.getElementById('id_nascimento').value;
    let usuario = criarUsuario(nome, telefone, email, nascimento);
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

    usuarios.push(usuario);

    localStorage.setItem('usuarios', JSON.stringify(usuarios));
    alert('Usuário cadastrado com sucesso!');

    limparFormulario();
}

// Adicionar evento de submit ao formulário
document.getElementById('cadastroForm').addEventListener('submit', function(e) {
    e.preventDefault();
    cadastrar();
});

function exibirUsuarios() {
    // Obter a lista de usuários do localStorage
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];

    // Construir a tabela 
    let resultadoHtml = '<table class="table table-striped">';
    resultadoHtml += `
        <thead>
            <tr>
                <th>Nome</th>
                <th>Telefone</th>
                <th>Email</th>
                <th>Data de Nascimento</th>
                <th>Ação</th>
            </tr>
        </thead>
        <tbody>`;
    // Adicionar as linhas dos usuários
    if (usuarios.length > 0) {
        usuarios.forEach((usuario, index) => {
            resultadoHtml += `
                <tr>
                    <td>${usuario.nome.toUpperCase()}</td>
                    <td>${usuario.telefone}</td>
                    <td>${usuario.email}</td>
                    <td>${usuario.nascimento}</td>
                    <td><button class="btn btn-danger" onclick="excluirUsuario(${index})">Excluir</button></td>
                </tr>`;
        });
    } else {
        resultadoHtml += '<tr><td colspan="5">Nenhum usuário cadastrado.</td></tr>';
    }

    resultadoHtml += '</tbody></table>';
    // Atualizar o conteúdo do div com a tabela
    document.getElementById('exibirusuarios').innerHTML = resultadoHtml;
}
// Exibir os usuários ao carregar a página
document.addEventListener('DOMContentLoaded', exibirUsuarios);

function excluirUsuario(index) {
    let usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
    let usuario = usuarios[index].nome;
    var confirmacao = confirm("Tem certeza que deseja excluir "+ usuario.toUpperCase() + " ? " );

    if (confirmacao) {
        // Remover o usuário do array
        usuarios.splice(index, 1);
        // Salvar a lista atualizada no localStorage
        localStorage.setItem('usuarios', JSON.stringify(usuarios));
        exibirUsuarios();
}
}