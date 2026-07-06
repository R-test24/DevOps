// teste.js

// Mensagem ao carregar a página
console.log("JavaScript carregado com sucesso!");

// Variáveis
let nome = "Ronald";
let idade = 25;

// Função de boas-vindas
function boasVindas() {
    alert(`Olá, ${nome}! Bem-vindo ao sistema.`);
}

// Função de soma
function somar(a, b) {
    return a + b;
}

// Teste da função
let resultado = somar(10, 20);
console.log("Resultado da soma:", resultado);

// Evento de clique
document.addEventListener("DOMContentLoaded", () => {
    console.log("Página carregada.");

    const botao = document.getElementById("btnTeste");

    if (botao) {
        botao.addEventListener("click", boasVindas);
    }
});