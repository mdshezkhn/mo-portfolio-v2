const { chromium } = require('playwright');
const path = require('path');

async function generatePDF() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  const htmlPath = path.resolve(__dirname, '../mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.html');
  const pdfPath = path.resolve(__dirname, '../mo-portfolio-v2/assets/documents/Mohammed_Shehzad_Khan_CV.pdf');
  
  console.log(`Loading HTML from: ${htmlPath}`);
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle' });
  
  console.log(`Generating PDF to: ${pdfPath}`);
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '0',
      right: '0',
      bottom: '0',
      left: '0'
    }
  });

  await browser.close();
  console.log('CV PDF generated successfully!');
}

generatePDF().catch(console.error);
