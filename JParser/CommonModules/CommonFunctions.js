const pup = require('puppeteer');
const sqlite3 = require('sqlite3').verbose();
const logger = require('./LoggingTool');

async function getInnerHTMLByXPath(page, xpath, customMessage) {
  try {
    logger.info(`${customMessage || 'Iniciando'} getInnerHTMLByXPath com XPath: ${xpath}`);

    const innerHTML = await page.evaluate((xpath) => {
      const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
      return element ? element.innerHTML : '';
    }, xpath);

    logger.success(`${customMessage || ''} getInnerHTMLByXPath concluído com sucesso para XPath: ${xpath}`);

    return innerHTML;
  } catch (error) {
    logger.error(`${customMessage || 'Erro em'} getInnerHTMLByXPath para XPath: ${xpath}`, error);
    throw error;
  }
}
async function getTextContentByXPath(page, xpath, customMessage) {
  try {
    logger.info(`${customMessage || 'Iniciando'} getTextContentByXPath com XPath: ${xpath}`);

    const textContent = await page.evaluate((xpath) => {
      const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
      return element ? element.textContent : null;
    }, xpath);

    logger.success(`${customMessage || ''} getTextContentByXPath concluído com sucesso para XPath: ${xpath}`);

    return textContent;
  } catch (error) {
    logger.error(`${customMessage || 'Erro em'} getTextContentByXPath para XPath: ${xpath}`, error);
    throw error;
  }
}
async function delayTime(time) {
  try {
    const defaultMessage = `Delaying ${time / 1000} seconds`;
    logger.info(defaultMessage);

    await new Promise((resolve) => setTimeout(resolve, time));

    logger.success(`Delay concluído com sucesso: ${defaultMessage}`);
  } catch (error) {
    logger.error(`Erro durante o atraso: ${defaultMessage}`, error);
    throw error;
  }
}
async function insertJobIntoDatabase(databaseName, job) {
  const db = new sqlite3.Database(databaseName);

  const insertJobQuery = `
      INSERT INTO JobsAPI_job (job_id, job_title, company_name, job_link, job_description, double_check, source)
      VALUES (?, ?, ?, ?, ?, ?, ?);
  `;
  try {
    await new Promise((resolve, reject) => {
      db.run(insertJobQuery, [
        job.job_id,
        job.job_title,
        job.company_name,
        job.job_link,
        job.job_description,
        job.double_Check,
        "linkedin"
      ], function (err) {
        if (!err) {
          resolve();
        } else {
          reject(err);
        }
      });
    });

    logger.success(`Job Inserted into DB`);
  } catch (error) {
    logger.error(`Error during job inserting.`, error);
    throw error;
  } finally {
    db.close();
  }
}
async function findAllChildrenByXpath(page, xpathString, customMessage) {
  try {
    logger.info(`${customMessage || 'Iniciando'} findAllChildrenByXpath with XPath: ${xpathString}`);

    const elements = await page.$x(xpathString);

    logger.success(`${customMessage || ''} findAllChildrenByXpath concluded with success using XPath: ${xpathString}`);

    return elements;
  } catch (error) {
    logger.error(`${customMessage || 'Erro em'} error using XPath: ${xpathString}`, error);
    throw error;
  }
}
async function getPropertyWithFallback(page, xpath, property, maxRetries, customMessage) {
  let retries = 0;
  let result = null;

  try {
    logger.info(`${customMessage || 'Iniciando'} getPropertyWithFallback para XPath: ${xpath}`);

    while (retries < maxRetries) {
      const element = await page.waitForXPath(xpath);
      result = await element.evaluate((el, prop) => el.getAttribute(prop), property);
      if (result) {
        break; // Se tiver sucesso, saia do loop.
      } else {
        retries++;
      }
    }

    logger.success(`${customMessage || ''} getPropertyWithFallback concluído com sucesso para XPath: ${xpath}`);
    return result;
  } catch (error) {
    logger.error(`${customMessage || 'Erro em'} getPropertyWithFallback para XPath: ${xpath}`, error);
    throw error;
  }
}
async function getHrefByXPath(page, xpath, customMessage) {
  try {
    logger.info(`${customMessage || 'Iniciando'} getHrefByXPath para XPath: ${xpath}`);

    const element = await page.waitForXPath(xpath, { visible: true });

    const href = await element.evaluate((el) => el.getAttribute('href'));

    if (href) {
      logger.success(`${customMessage || ''} getHrefByXPath concluído com sucesso para XPath: ${xpath}`);
      return href;
    } else {
      throw new Error(`Elemento encontrado em ${xpath} não possui atributo 'href'.`);
    }
  } catch (error) {
    logger.error(`${customMessage || 'Erro em'} getHrefByXPath para XPath: ${xpath}`, error);
    throw error;
  }
}
async function insertJobsIntoDatabase(databaseName, jobs) {
  const db = new sqlite3.Database(databaseName);

  const insertJobQuery = `
      INSERT INTO JobsAPI_job (job_id, job_title, company_name, job_link, job_description, double_check, source)
      VALUES (?, ?, ?, ?, ?, ?, ?);
  `;

  try {
    for (const job of jobs) {
      await new Promise((resolve, reject) => {
        db.run(insertJobQuery, [
          job.job_id,
          job.job_title,
          job.company_name,
          job.job_link,
          job.job_description,
          job.double_Check,
          "linkedin"
        ], function (err) {
          if (!err) {
            resolve();
          } else {
            reject(err);
          }
        });
      });


    }
    logger.success(`Jobs Inserted into DB`);
  } catch (error) {
    logger.error(`Error during job insertion.`, error);
    throw error;
  } finally {
    db.close();
  }
}
module.exports = {
  getInnerHTMLByXPath,
  getTextContentByXPath,
  delayTime,
  insertJobIntoDatabase,
  findAllChildrenByXpath,
  getPropertyWithFallback,
  getHrefByXPath,
  insertJobsIntoDatabase
  // Adicione outras funções exportadas aqui, se necessário
};
