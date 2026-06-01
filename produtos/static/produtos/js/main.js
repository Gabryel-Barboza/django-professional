document.addEventListener("DOMContentLoaded", function () {
    
    /* ==========================================================================
       1. FILTRO DE BUSCA EM TEMPO REAL (VITRINE)
       ========================================================================== */
    const searchInput = document.getElementById("search-product");
    const productItems = document.querySelectorAll(".product-list-item");

    if (searchInput) {
        searchInput.addEventListener("input", function (e) {
            const term = e.target.value.toLowerCase().trim();

            productItems.forEach(item => {
                // Pega o texto de dentro do link do produto
                const productName = item.querySelector(".product-link").textContent.toLowerCase();
                
                // Se o termo estiver no nome, mostra. Se não, esconde.
                if (productName.includes(term)) {
                    item.style.display = "flex"; // Mantém o flexbox do card
                } else {
                    item.style.display = "none";
                }
            });
        });
    }

    /* ==========================================================================
       2. CLIQUE PARA COPIAR O UUID (DETALHES)
       ========================================================================== */
    const uuidBox = document.getElementById("uuid-copy");

    if (uuidBox) {
        uuidBox.addEventListener("click", function () {
            const uuidText = this.getAttribute("data-uuid");

            // API nativa de copiar do navegador
            navigator.clipboard.writeText(uuidText).then(() => {
                // Feedback visual temporário
                const originalText = this.innerHTML;
                this.innerHTML = "✨ Copiado com sucesso!";
                this.style.color = "#28a745";
                this.style.fontWeight = "bold";

                setTimeout(() => {
                    this.innerHTML = originalText;
                    this.style.color = "";
                    this.style.fontWeight = "";
                }, 2000);
            }).catch(err => {
                console.error("Erro ao copiar: ", err);
            });
        });
    }
});