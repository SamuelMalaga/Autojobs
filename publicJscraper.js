const pup = require('puppeteer');
const LNconfig = require('./jParserConfig.json');
const yargs = require('yargs');

const argv = yargs
  .options({
    'job-name': {
      describe: 'Nome do trabalho',
      demandOption: true, // Defina como true se o argumento for obrigatório
      type: 'string', // Especifique o tipo do argumento (string neste caso)
    },
    'job-location': {
      describe: 'Localização do trabalho',
      demandOption: true, // Defina como true se o argumento for obrigatório
      type: 'string', // Especifique o tipo do argumento (string neste caso)
    },
    'job-type': {
      describe:'Tipo de trabalho, Presencial (1), Híbrido (2) ou remoto (3)',
      demandOption: true, // Defina como true se o argumento for obrigatório
      type: 'int', // Especifique o tipo do argumento (string neste caso)
    }
  })
  .argv;

function delayTime(time) {
  return new Promise(function(resolve) {
    setTimeout(resolve, time);
  });
}

async function scrollToEnd(page) {
  let previousHeight = 0;

  await page.evaluate(() => {
    window.scrollBy(0, window.innerHeight);
  });

  await delayTime(1000); // Espera 4 segundos.

  const newHeight = await page.evaluate(() => {
    return document.body.scrollHeight;
  });

  const successAlert = await page.evaluate(() => {
    const alertDiv = document.querySelector('div[role="alert"][type="success"]');
    return alertDiv ? alertDiv.classList.contains('hidden') : false;
  });

  if (!successAlert) {
      console.log('A div de alerta de sucesso não está mais oculta. Encerrando a execução.');
      return true;
    }

  // Tente clicar no botão "Ver mais vagas" com tratamento de erro.
  try {
    await page.click('button[aria-label="Ver mais vagas"]');
  } catch (error) {
    console.log('Erro ao clicar no botão "Ver mais vagas":', error.message);
  }

  return false; // A página ainda não atingiu o final.
}
async function extractDataFromPage(page) {
  const data = await page.evaluate(() => {
    const items = [];
    const xpath = '//*[@id="main-content"]/section[2]/ul/li/div';
    const iterator = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

    for (let i = 0; i < iterator.snapshotLength; i++) {
      const item = iterator.snapshotItem(i);
      const dataEntityUrn = item.getAttribute('data-entity-urn');
      items.push({ text: dataEntityUrn });
    }

    return items;
  });

  return data;
}



(async () => {
  const browser = await pup.launch({headless: false});
  const page = await browser.newPage();

  const jobName = encodeURIComponent(argv['job-name']);
  const jobLocation = encodeURIComponent(argv['job-location']);
  const jobType = encodeURIComponent(argv['job-type']);

  // Defina o tamanho da tela visível, por exemplo, 1200x800 pixels
  await page.setViewport({ width: 800, height: 600 });

  await page.goto(`https://www.linkedin.com/jobs/search?keywords=${jobName}&location=${jobLocation}&f_WT=${jobType}`);

  // for( i=0; i < 5; i++){
  //   scrollToEnd(page)
  //   await delayTime(1000)
  // }
  //Infinite scroll
  while (true) {
    const hasReachedEnd = await scrollToEnd(page);

    if (hasReachedEnd) {
      console.log('Página atingiu o final.');
      break;
    }

    await delayTime(1000); // Espera 4 segundos antes de rolar novamente.
  }

  const output = await extractDataFromPage(page);

  console.log(output.length)


  //await browser.close();
})();
