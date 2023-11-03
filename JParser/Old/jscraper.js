const pup = require('puppeteer');
const LNconfig = require('../jParserConfig.json');
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
    }
  })
  .argv;


function delay(time) {
  return new Promise(function(resolve) {
      setTimeout(resolve, time)
  });
}

async function getTotalNumberOfPages(page){

  // Use XPath para selecionar a <ul> desejada com a propriedade customizada
  const ulXPath = '//ul[contains(@class, "artdeco-pagination__pages artdeco-pagination__pages--number")]';

  const ulElement = await page.$x(ulXPath);

  let totalNumberOfPages = 0;

  if (ulElement.length > 0) {
    const ul = ulElement[0];

    // Use XPath para selecionar diretamente os nós netos
    const grandchildrenXPath = './*/*';
    const grandchildren = await page.$x(`${ulXPath}/${grandchildrenXPath}`);
    console.log(grandchildren.length)
    totalNumberOfPages = await page.evaluate(el => parseInt(el.textContent), grandchildren[grandchildren.length - 1]);
  }
  return totalNumberOfPages

}
async function gotoNextPage(page){

  const ulXPath = '//ul[contains(@class, "artdeco-pagination__pages artdeco-pagination__pages--number")]';

  const ulElement = await page.$x(ulXPath);

  let totalNumberOfPages = 0;

  if (ulElement.length > 0) {
    const ul = ulElement[0];

    // Use XPath para selecionar diretamente os nós netos
    const grandchildrenXPath = './*/*';
    const grandchildren = await page.$x(`${ulXPath}/${grandchildrenXPath}`);

    for (const grandchild of grandchildren) {

      const text = await page.evaluate(el => el.textContent, grandchild);
      const ariaCurrent = await page.evaluate(el => el.getAttribute('aria-current'), grandchild);

      let currentIndex = grandchildren.indexOf(grandchild);

      if (ariaCurrent) {
        nextPageLoc = currentIndex+1
      }
      if (currentIndex === nextPageLoc){
        await grandchild.click()
        break
      }
    }

  } else {
    console.log('Nó de referência não encontrado.');
  }
}

(async () => {
  const browser = await pup.launch({headless:false});
  const page = await browser.newPage();

  const jobName = argv['job-name'];
  const jobLocation = argv['job-location'];

  // Defina o tamanho da tela visível, por exemplo, 1200x800 pixels
  await page.setViewport({ width: 1200, height: 800 });

  await page.goto('https://www.linkedin.com/jobs');
  //Get the login elements
  const [sessionKeyInput, sessionPasswordInput] = await page.$$('input[name="session_key"], input[name="session_password"]');

  //Fill in the login elements
  await sessionKeyInput.type(LNconfig.userEmail);
  await sessionPasswordInput.type(LNconfig.userPassword);

  //Finds Login button
  const entrarButton = await page.$('button[data-id="sign-in-form__submit-btn"][data-tracking-control-name="homepage-jobseeker_sign-in-submit-btn"]');
  if (entrarButton) {
    // Faça ações no botão, por exemplo, clique nele
    await entrarButton.click();
  } else {
    console.error('Botão "Entrar" não encontrado.');
  }

  //Wait untill the page loads
  await delay(20000)

  // Selecione o elemento cujo atributo 'id' começa com 'jobs-search-box'
  const searchJobInput = await page.$('[id^="jobs-search-box-keyword-id-ember"]');

  if (searchJobInput) {
    // Digite algo no elemento
    await searchJobInput.type(jobName);

    // Pressione "Enter" (opcional)
  } else {
    console.log('Elemento não encontrado.');
  }

  // Wait until the page loads
  await delay(2000);

  // Selecione o elemento cujo atributo 'id' começa com 'jobs-search-box'
  const searchLocationInput = await page.$('[id^="jobs-search-box-location-id-ember"]');

  if (searchLocationInput) {
    // Digite algo no elemento
    await searchLocationInput.type(jobLocation);

    await page.keyboard.press('Enter');
  } else {
    console.log('Elemento não encontrado.');
  }

  // Wait until the page loads
  await delay(4000);


  // Use XPath para selecionar a <ul> desejada com a propriedade customizada
  let totalPages = await getTotalNumberOfPages(page);

  for(let i=0;i < 39;i++){
    await delay(4000);
    gotoNextPage(page);
  }

  console.log(typeof totalPages,"O total de páginas é:", totalPages)

  //await browser.close();
})();
