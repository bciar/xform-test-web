
const assert = require('assert');
const downloadsFolder = require('downloads-folder');
const fs = require('fs');
const ls = require('ls');
const path = require('path');
const webdriver = require('selenium-webdriver'),
  By = webdriver.By,
  until = webdriver.until;

require('chromedriver');

let defaultUrls = {  // TODO #6a: Set these URLs as environmental variables.
  dev: 'http://localhost:3000',
  // staging: '',
  production: 'http://xform-test.pma2020.org/'
};
const webdriver = require('selenium-webdriver');
const chrome = require('selenium-webdriver/chrome');
const firefox = require('selenium-webdriver/firefox');

let driver = new webdriver.Builder()
    .forBrowser('firefox')
    .setChromeOptions(/* ... */)
    .setFirefoxOptions(/* ... */)
    .build();