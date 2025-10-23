
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS anexo;
DROP TABLE IF EXISTS comentario;
DROP TABLE IF EXISTS relatorio;
DROP TABLE IF EXISTS tempo_gasto;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS tarefa;
DROP TABLE IF EXISTS usuario;
SET FOREIGN_KEY_CHECKS = 1;


CREATE TABLE usuario (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_usuario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE categoria (
    id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    descricao TEXT,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO categoria (id, nome, descricao) VALUES
(1, 'trabalho', 'Profissional'),
(2, 'estudo', 'materia'),
(3, 'pessoal', 'privado');


CREATE TABLE tarefa (
    id_tarefa INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    data_inicio DATE NOT NULL,
    data_fim DATE,
    status VARCHAR(20) DEFAULT 'pendente',
    tempo_gasto DECIMAL(5,2) DEFAULT 0,
    id_usuario INT NOT NULL,
    categoria_id INT,
    PRIMARY KEY (id_tarefa),
    CONSTRAINT fk_tarefa_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE,
    CONSTRAINT fk_tarefa_categoria FOREIGN KEY (categoria_id)
        REFERENCES categoria (id)
        ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE tempo_gasto (
    id INT NOT NULL AUTO_INCREMENT,
    tarefa_id INT NOT NULL,
    horas DECIMAL(5,2) NOT NULL,
    data_registro DATE NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_tempo_tarefa FOREIGN KEY (tarefa_id)
        REFERENCES tarefa (id_tarefa)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE relatorio (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    total_tarefas INT DEFAULT 0,
    tarefas_concluidas INT DEFAULT 0,
    tempo_total DECIMAL(8,2) DEFAULT 0,
    data_geracao DATE NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_relatorio_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE comentario (
    id INT NOT NULL AUTO_INCREMENT,
    tarefa_id INT NOT NULL,
    usuario_id INT NOT NULL,
    texto TEXT NOT NULL,
    data_comentario DATE NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_comentario_tarefa FOREIGN KEY (tarefa_id)
        REFERENCES tarefa (id_tarefa)
        ON DELETE CASCADE,
    CONSTRAINT fk_comentario_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuario (id_usuario)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE anexo (
    id INT NOT NULL AUTO_INCREMENT,
    tarefa_id INT NOT NULL,
    nome_arquivo VARCHAR(200) NOT NULL,
    tipo_arquivo VARCHAR(50),
    caminho VARCHAR(255) NOT NULL,
    PRIMARY KEY (id),
    CONSTRAINT fk_anexo_tarefa FOREIGN KEY (tarefa_id)
        REFERENCES tarefa (id_tarefa)
        ON DELETE CASCADE

) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

