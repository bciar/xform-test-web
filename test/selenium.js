/* TODOs
* 1. Do we need to handle promises marked (1)?
* */
/* const assert = require('assert');
const fs = require('fs'); */
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

let globals = {
    failCount: 0, 
    passCount: 0,
    errorCount: 0
};

let testConfig = {
  urlBase: defaultUrls['production'], 
};


const handleSeleniumErr = (err, rejectionHandler, options) => {
  const isAssertionError = err.name.toLowerCase().substring(0, 6) === 'assert' || err.name === 'AssertionError [ERR_ASSERTION]';
  const possiblyCascadedError = `${err}`.match('ENOENT') !== null && `${err}`.match(testConfig.svgFileName) !== null;
  const commonErrorMsgStartTxt = '  - Message: Encountered common test error';
  const unanticipatedErrorMsgStartTxt = '  - Message: Encountered unanticipated error';
  let commonErrorMessage = `${commonErrorMsgStartTxt}: '${err.name}'\n` +
    '    This type of error is typically due to latency fluctuations in the selenium driver ' +
    'and is not typically the cause of a failing test case, unless 100% of test cases are failing.';
  commonErrorMessage += '\n' + err + '\n\n';
  
  if (isAssertionError) {
      globals.failCount++;
      console.log('Throwing AssertionError and exiting now.\n');
      throw(err);
  } else {
    // const errAlreadyHandled = `${err}`.match(commonErrorMsgStartTxt) !== null ||
    //   `${err}`.match(unanticipatedErrorMsgStartTxt) !== null;
    if (options) {
    // if (!errAlreadyHandled) {
      globals.errorCount++;
      if (options) {
        const spacer = options.testCaseNum <= 1 ? '' : '\n';
        console.log(`${spacer}Test case ${options.testCaseNum}/${options.totTestCases}: (error)`);
      }
      // TODO: Test re-running is not actually working. Instead, going with error threshold method instead.
      if (err.name === 'NoSuchElementError' ||
          err.name === 'TimeoutError' ||
          err.name === 'StaleElementReferenceError') {
        console.log(commonErrorMessage);
        // Don't actually need to print anything... this is printed elsewhere.
        // console.log('Test case may be re-attempted. If not re-attempted or if ' +
        //   're-attempts fail, this will increase the running error count.');
      } else if (
          err.name === 'NoSuchSessionError' ||
          err.name === 'WebDriverError') {
        console.log(commonErrorMessage);
      } else if (possiblyCascadedError) {
        console.log(commonErrorMessage);
        // This seems to usually immediately follow "WebDriverError: element not visible", so it could be redundant.
        // Hence, I have called it "cascaded". However, given that I am not 100% sure if this error can't appear on its own,
        // it is considered "possibly cascaded", and we are printing the error if it hasn't been handled before.
      } else {
        console.log(`${unanticipatedErrorMsgStartTxt}` + (err.name ? ': ' + err.name : '') + '\n' +
          '  - Error details:\n' +
          `    ${err}`);
      }
      if (!rejectionHandler ||
          rejectionHandler === null ||
          typeof rejectionHandler === 'undefined') {
        // Do nothing.
      } else {
        rejectionHandler(err);
      }
    } else {  // TODO: Is it better if this is above, below, or in both places?
      if (!rejectionHandler ||
          rejectionHandler === null ||
          typeof rejectionHandler === 'undefined') {
        // Do nothing.
      } else {
        rejectionHandler(err);
      }
    }
  }
};

const uploadFile = (resolve, rejectionHandler, driver, testFilePath, reattemptSlowdownMultiplier) => {
  const url = testConfig.urlBase;
  driver.get(url)
  .then().catch(err => { handleSeleniumErr(err, rejectionHandler); });
  const dropZone = driver.findElement(webdriver.By.css('.dropzone'));
  const fileInput = dropZone.findElement(webdriver.By.tagName('input'));
  console.log('test file path=', testFilePath);
  fileInput.sendKeys(testFilePath);
  driver.wait(until.elementLocated(By.css('.message-bar')), 400000*testConfig.slowdownMultiplier*reattemptSlowdownMultiplier)
  .then(() => {
    const message_bar = driver.findElement(webdriver.By.css('.message-bar'));
    resolve(message_bar.findElement(webdriver.By.tagName('pre')).getText());
  }).catch(err => { handleSeleniumErr(err, rejectionHandler); });
};

const singleTestCase = (driverName, driver, testCaseNum, totTestCases, testFilePath, attemptNumber) => {
  return new Promise((resolve, reject) => {
    uploadFile(resolve, reject, driver, testFilePath, attemptNumber)
  }).then(result => {
    console.log(result);
  }).catch(err => {
    const options = {
      testCaseNum: testCaseNum,
      totTestCases: totTestCases
    };
    handleSeleniumErr(err, null, options);
  });
};

async function testOnBrowser(driverName, driver, testFilePaths, attemptNumber) {
  let testCaseNum = 0;
  const totTestsToRun = testFilePaths.length;
  for (let testFilePath of testFilePaths) {
    testCaseNum++;
    await singleTestCase(driverName, driver, testCaseNum, totTestsToRun , testFilePath, 1);
  }
  driver.quit();
}

const buildBrowser = (testFilePaths) => {
  const seleniumBrowserDrivers = ['chrome'];  // TODO @Bciar: Other browsers.
  for (let driverName of seleniumBrowserDrivers) {
    // TODO: Put this in a global function, so it can be re-used in other places that are quitting and restarting the driver to do re-attempts.
    const driver = {'chrome': new webdriver.Builder().forBrowser('chrome').build()}[driverName];
    console.log(`Starting: Selenium SVG similarity test, ${driverName}`);
    testOnBrowser(driverName, driver, testFilePaths, 1);
  }
}

const getTestFilePathArray = () => {
  let testParams = {};
  let testFilePaths = [];
  const directory = ['static/CRVS/input/', 'static/MultipleFiles/input/', 'static/MultipleTestCases/input/', 
      'static/NA/input/', 'static/ShortForm/input/', 'static/ValueAssertionError/input/', 'static/ValueAssertionError2/input/',
      'static/ValueAssertionError3/input/', 'static/ValueAssertionError4/input/', 'static/ValueAssertionError5/input/',
      'static/XformTest/input/'];
  directory.forEach(d => {
    const xmlFilePath = path.join(__dirname, d+'*.xml');
    for (let file of ls(xmlFilePath)) {
      testFilePaths.push(path.join(__dirname, d+file.name+'.xml'));
    }
  });
  testParams.testFilePaths = testFilePaths;
  return testParams;
};

const setUpErrorHandling = () => {
  process.on('unhandledRejection', (reason) => {
    // Recommended: send the information to sentry.io or crash reporting service.
    console.log('Unhandled Rejection at:', reason.stack || reason);
    throw('Exiting with error status 1.')
  });
};
const XFormTest = () => {
  setUpErrorHandling();
  const testParams = getTestFilePathArray();
  console.log('start xform test...');
  buildBrowser(testParams.testFilePaths);
}

XFormTest();
