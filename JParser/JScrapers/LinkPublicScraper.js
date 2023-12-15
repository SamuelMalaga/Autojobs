const pup = require('puppeteer');
const sqlite3 = require('sqlite3').verbose();
const yargs = require('yargs');
const logger = require('../CommonModules/LoggingTool');
const commonFunctions = require('../CommonModules/CommonFunctions')

const argv = yargs
  .options({
    'job_link': {
      describe: 'Job link',
      demandOption: true, // Defina como true se o argumento for obrigatório
      type: 'string', // Especifique o tipo do argumento (string neste caso)
    }
  })
  .argv;

// function delayTime(time) {
//   return new Promise(function(resolve) {
//     setTimeout(resolve, time);
//   });
// }


// // /**
// //  * Insere os objetos job em uma tabela SQLite.
// //  * @param {string} databaseName - O nome do banco de dados SQLite.
// //  * @param {Array} jobs - Um array de objetos job a serem inseridos na tabela.
// //  */
// async function insertJobIntoDatabase(databaseName, job) {
//   const db = new sqlite3.Database(databaseName);

//   const insertJobQuery = `
//       INSERT INTO JobsAPI_job (job_id, job_title, company_name, job_link, job_description, double_check, source)
//       VALUES (?, ?, ?, ?, ?, ?, ?);
//   `;

//   db.run(insertJobQuery, [
//     job.job_id,
//     job.job_title,
//     job.company_name,
//     job.job_link,
//     job.job_description,
//     job.double_Check,
//     "linkedin"
//     ], (err) => {
//         if (!err) {
//             console.log(`Inserido`);
//         } else {
//             console.error(`Erro ao inserir`);
//         }
//     });

//   db.close();
// }
// // async function getInnerHTMLByXPath(page, xpath) {
// //   return page.evaluate((xpath) => {
// //     const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
// //     return element ? element.innerHTML : null;
// //   }, xpath);
// // }
// async function getInnerHTMLByXPath(page, xpath) {
//   try {
//     logger.info(`Iniciando getInnerHTMLByXPath com XPath: ${xpath}`);

//     const innerHTML = await page.evaluate((xpath) => {
//       const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
//       return element ? element.innerHTML : '';
//     }, xpath);

//     logger.success(`getInnerHTMLByXPath concluído com sucesso para XPath: ${xpath}`);

//     return innerHTML;
//   } catch (error) {
//     logger.error(`Erro em getInnerHTMLByXPath para XPath: ${xpath}`, error);
//     throw error;
//   }
// }
// async function getTextContentByXPath(page, xpath) {
//   return page.evaluate((xpath) => {
//     const element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
//     return element ? element.textContent : null;
//   }, xpath);
// }

(async () => {
  const startTime = new Date();
  //console.log(`Iniciando scraping em ${startTime.getHours()}:${startTime.getMinutes()}:${startTime.getSeconds()}`)
  const browser = await pup.launch();
  const page = await browser.newPage();

  const jobLink = argv['job_link'];
  //console.log(jobLink)

  await page.goto(jobLink)

  const jobDescriptionHTMLContent = await commonFunctions.getInnerHTMLByXPath(page, '/html/body/main/section[1]/div/div/section[1]/div/div/section/div','Getting job description');
  //await getInnerHTMLByXPath(page, '/html/body/main/section[1]/div/div/section[1]/div/div/section/div')
  const jobTitle = await commonFunctions.getTextContentByXPath(page,'/html/body/main/section[1]/div/section[2]/div/div[1]/div/h1','Getting job title')
  //await getTextContentByXPath(page,'/html/body/main/section[1]/div/section[2]/div/div[1]/div/h1')
  const jobCompany = await commonFunctions.getTextContentByXPath(page, '/html/body/main/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]','Getting job company')
  const jobLocation = await commonFunctions.getTextContentByXPath(page,'/html/body/main/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]','Getting job location')

  const job = {
    "job_id": null,
    "job_title": await jobTitle.trim(),
    "company_name": await jobCompany.trim(),
    "job_link": jobLink,
    "job_description" : await jobDescriptionHTMLContent.trim(),
    "double_Check": false,
    "source" : "linkedin"
  }

  await commonFunctions.insertJobIntoDatabase('C:/Users/SamuelMendesMalaga/Documents/Autojobs/SQLiteDB/autojobs.db',job)

  await browser.close();

})();
