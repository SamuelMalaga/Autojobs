const { createLogger, transports, format } = require('winston');

const logger = createLogger({
  // Níveis de logging personalizados
  levels: {
    info: 0,
    success: 1,
    error: 2,
  },
  // Formato de saída do log
  format: format.combine(
    format.timestamp(),
    format.printf(({ level, message, timestamp }) => `[${timestamp}] [${level.toUpperCase()}]: ${message}`)
  ),
  // Transportes (onde os logs serão enviados)
  transports: [
    new transports.Console(), // Saída para o console
    new transports.File({ filename: 'logs/error.log', level: 'error' }), // Saída para um arquivo de erro
    new transports.File({ filename: 'logs/all.log' }) // Saída para um arquivo geral
  ],
});

// Adicione o nível "success"
logger.addColors({ success: 'green' });

module.exports = logger;
