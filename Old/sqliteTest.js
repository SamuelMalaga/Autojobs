const sqlite3 = require('sqlite3').verbose();

// Abra o banco de dados (ou crie um novo se não existir)
const db = new sqlite3.Database('autojobs.db');

// Script SQL para criar a tabela
const createTableQuery = `
    CREATE TABLE IF NOT EXISTS jobs (
        job_id INTEGER,
        job_title TEXT,
        company_name TEXT,
        job_link TEXT,
        job_description TEXT,
        double_Check BOOLEAN
    );
`;

// Execute o script SQL para criar a tabela
db.serialize(() => {
    db.run(createTableQuery, (err) => {
        if (!err) {
            console.log('Tabela "jobs" criada com sucesso.');
        } else {
            console.error('Erro ao criar a tabela:', err.message);
        }
    });
});

// Feche o banco de dados quando terminar
db.close();
