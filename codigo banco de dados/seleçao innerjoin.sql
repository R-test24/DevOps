select alunos.nome, count(emprestimo.id_emprestimo) as total_emprestimo from emprestimo
inner join alunos
on emprestimo.id_alunos = alunos.id_alunos
group by alunos.nome