const templateHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>A4</title>
  <style>
    @import url("https://fonts.googleapis.com/css2?family=Zilla+Slab:ital,wght@0,300;0,400;0,500;0,600;0,700&display=swap");
    * {
      font-family: "Zilla Slab";
      padding: 0;
      margin: 0;
      box-sizing: border-box;
      line-height: 0.9;
      list-style: none;
    }
    body {
      background: rgb(204, 204, 204);
    }
    .a4-div > p,
    span,
    li,
    td {
      font-size: 13.5pt;
    }
    .a4-div {
      display: flex;
      flex-direction: column;
      background: white;
      margin: 0 auto;
      margin-bottom: 0.5cm;
      box-shadow: 0 0 0.5cm rgba(0, 0, 0, 0.5);
      flex-wrap: wrap;
      gap: 1px;
      padding: 0;
      width: 21cm;
      height: 29.7cm;
    }
    .a4-div[size="A4"] {
      width: 21cm;
      height: 29.7cm;
    }
    .a4-div[size="A4"][layout="portrait"] {
      width: 29.7cm;
      height: 21cm;
    }
    @media print {
      body,
      page {
        margin: 0;
        box-shadow: 0;
      }
    }
    .word-card {
      width: calc(33.33% - 1px);
      height: calc(20% - 1px);
      border: 1px solid black;
      background-color: rgb(239, 239, 239);
      box-sizing: border-box;
    }
    .word {
      display: flex;
      justify-content: space-between;
      font-weight: bold;
      border-bottom: 1px solid black;
      padding-bottom: 2px;
      margin-bottom: 2px;
    }
    .topic {
      font-style: italic;
      border-bottom: 1px solid black;
      padding-bottom: 2px;
      margin-bottom: 2px;
    }
    .definition-and-pronunciation {
      border-bottom: 1px solid black;
      padding-bottom: 2px;
      margin-bottom: 2px;
    }
    .examples {
      line-height: 0.9;
    }
    .examples li {
      margin-bottom: 1px;
    }
  </style>
</head>
<body>
  <div class="a4-div" size="A4">
    <!-- FLASHCARDS_PLACEHOLDER -->
  </div>
</body>
</html>
`;
