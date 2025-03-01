const puppeteer = require('puppeteer');
const fs = require('fs');

async function getData() {
    // Launch a headless browser
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    // Fetch the page
    await page.goto('https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=1&sort_by=lastChecked&sort_type=desc', { waitUntil: 'networkidle2' });

    // Get the page content
    const data = await page.evaluate(() => document.body.innerText);

    await browser.close();
    return JSON.parse(data);
}

async function main() {
    const data = await getData();
    // console.log(data);

    // Save the data to a JSON file
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
}

main();