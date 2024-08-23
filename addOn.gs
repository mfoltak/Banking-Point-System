function onInstall(e) {
  onOpen(e);
}

function onOpen(e) {
  var ui = SpreadsheetApp.getUi();
  ui.createAddonMenu()
    .addItem('Set Up Expense Tracker', 'setup')
    .addToUi();
}

function setup() {
  var sheet = SpreadsheetApp.getActiveSheet();

  sheet.setFrozenRows(2);

  var headers = [
    "Date", 
    "Category", 
    "Description", 
    "Amount", 
    "Payment Method", 
    "Notes"
  ];
  var numCols = headers.length;
  sheet.getRange(1, 1, 1, numCols).setValues([headers]);

  sheet.getRange(1, 1, 1, numCols).setBackground('#0F9D58')
       .setFontColor('white')
       .setFontWeight("bold");

  sheet.getRange(2, numCols + 1).setValue("Total Expenses:");
  sheet.getRange(2, numCols + 2).setFormula("=SUM(D3:D)");

  sheet.setColumnWidths(1, 1, 100); // Date
  sheet.setColumnWidths(2, 1, 150); // Category
  sheet.setColumnWidths(3, 1, 250); // Description
  sheet.setColumnWidths(4, 1, 100); // Amount
  sheet.setColumnWidths(5, 1, 150); // Payment Method
  sheet.setColumnWidths(6, 1, 200); // Notes

  sheet.getRange("A:A").setNumberFormat("MM/dd/yyyy");

  sheet.getRange("D:D").setNumberFormat("$#,##0.00");

  sheet.getRange(1, 1, sheet.getMaxRows(), numCols).setBorder(true, true, true, true, true, true);

  sheet.setActiveSelection("A1");
}
