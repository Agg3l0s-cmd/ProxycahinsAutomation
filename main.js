const puppeteer = require('puppeteer');
const fs = require('fs');

// Detect if Firefox is installed
const isFirefox = process.argv.includes("--firefox"); // Run with "--firefox" to use Firefox
const executablePath = isFirefox ? "/usr/bin/firefox" : undefined; // Change this if Firefox is installed elsewhere

async function getData() {
    // Launch Puppeteer with dynamic browser selection
    const browser = await puppeteer.launch({ 
        headless: true,
        product: isFirefox ? "firefox" : "chrome", // Choose browser
        executablePath: executablePath // Use system Firefox if specified
    });

    const page = await browser.newPage();

    // Fetch the page
    await page.goto('https://proxylist.geonode.com/api/proxy-list?protocols=socks5&limit=500&page=1&sort_by=lastChecked&sort_type=desc', { 
        waitUntil: 'networkidle2' 
    });

    // Get the page content
    const data = await page.evaluate(() => document.body.innerText);

    await browser.close();
    return JSON.parse(data);
}

async function main() {
    const data = await getData();

    // Save the data to a JSON file
    fs.writeFileSync('data.json', JSON.stringify(data, null, 2));
}

// Run script normally (Chrome) or with "--firefox" argument to use Firefox
main();
