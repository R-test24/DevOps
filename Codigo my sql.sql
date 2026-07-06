create table pedido(
id int auto_increment primary key,
idcliente int,
idproduto int,
datapedido date,
foreign key(idcliente) references cliente(id),
foreign key(idproduto) references produto(id)
)