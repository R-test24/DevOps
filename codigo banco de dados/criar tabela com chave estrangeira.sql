CREATE TABLE Consulta (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    data_consulta DATE NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    diagnostico VARCHAR(200),
    id_animal INT,
    id_veterinario INT,

    FOREIGN KEY (id_animal) REFERENCES Animal(id_animal),
    FOREIGN KEY (id_veterinario) REFERENCES Veterinario(id_veterinario)
)
