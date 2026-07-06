select categoria, COUNT(*) AS quantidade_livro
from livro
group by categoria