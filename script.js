// script.js

let flashcards = [];
let currentFlashcard = 1;
const maxExamplesChars = 130;
const maxDefPronChars = 180;

document.addEventListener("DOMContentLoaded", () => {
  loadProgress();
  updateCharCount();
  updateFlashcardLabel();

  document.querySelectorAll("textarea").forEach((textarea) => {
    textarea.addEventListener("input", updateCharCount);
  });
});

function updateCharCount() {
  const example1 = document.getElementById("example1").value;
  const example2 = document.getElementById("example2").value;
  const totalExampleChars = example1.length + example2.length;

  const definition = document.getElementById("definition").value;
  const pronunciation = document.getElementById("pronunciation").value;
  const totalDefPronChars = definition.length + pronunciation.length;

  const charCountElement = document.getElementById("char-count");
  charCountElement.innerText = `${totalExampleChars}/${maxExamplesChars} (Examples), ${totalDefPronChars}/${maxDefPronChars} (Definition + Pronunciation)`;

  if (
    totalExampleChars > maxExamplesChars ||
    totalDefPronChars > maxDefPronChars
  ) {
    charCountElement.style.color = "red";
  } else {
    charCountElement.style.color = "black";
  }
}

function generateHtml() {
  const word = document.getElementById("word").value.trim();
  const topic = document.getElementById("topic").value.trim();
  const definition = document.getElementById("definition").value.trim();
  const example1 = document.getElementById("example1").value.trim();
  const example2 = document.getElementById("example2").value.trim();
  const pronunciation = document.getElementById("pronunciation").value.trim();

  if (example1.length + example2.length > maxExamplesChars) {
    alert("Examples combined length exceeds 130 characters.");
    return;
  }

  if (definition.length + pronunciation.length > maxDefPronChars) {
    alert(
      "Definition and pronunciation combined length exceeds 180 characters."
    );
    return;
  }

  const formattedExample1 = example1.replace(word, `<strong>${word}</strong>`);
  const formattedExample2 = example2.replace(word, `<strong>${word}</strong>`);

  const flashcard = `
    <div class="word-card">
        <div class="word"><strong>Word: </strong>${word}</div>
        <div class="topic"><strong>Topic: </strong>${topic}</div>
        <div class="definition-and-pronunciation"><em>[ ${pronunciation} ]</em> ${definition}</div>
        <div class="examples">
            <strong>Examples: </strong>
            <li>${formattedExample1}</li>
            <li>${formattedExample2}</li>
        </div>
    </div>
    `;

  flashcards.push(flashcard);
  if (flashcards.length === 15) {
    writeHtmlFile();
    flashcards = [];
    currentFlashcard = 1;
  } else {
    currentFlashcard++;
  }

  clearInputFields();
  updateFlashcardLabel();
}

function writeHtmlFile() {
  const fileName =
    document.getElementById("file-name").value.trim() || "flashcards";
  const htmlContent = `
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
      ${flashcards.join("")}
      <!-- FLASHCARDS_PLACEHOLDER -->

      <!-- The code below what python code will generate, commented if it is not used in order to change the style of html -->

      <!-- <div class="word-card">
        <div class="word">
          <span>{word}</span>
          <span>{pronunciation}</span>
        </div>
        <div class="topic">{topic}</div>
        <div class="definition-and-pronunciation">
          <p>{definition}</p>
        </div>
        <div class="examples">
          <ul>
            <li>{example1}</li>
            <li>{example2}</li>
          </ul>
        </div>
      </div> -->
    </div>
  </body>
</html>`;

  const blob = new Blob([htmlContent], { type: "text/html" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${fileName}_${Math.floor(currentFlashcard / 15)}.html`;
  link.click();

  alert("HTML file generated successfully!");
}

function updateFlashcardLabel() {
  document.getElementById(
    "flashcard-count"
  ).innerText = `Creating Flashcard: ${currentFlashcard}/15`;
}

function saveProgress() {
  const progress = {
    flashcards,
    currentFlashcard,
  };
  localStorage.setItem("flashcardProgress", JSON.stringify(progress));
  alert("Progress saved successfully!");
}

function loadProgress() {
  const savedProgress = localStorage.getItem("flashcardProgress");
  if (savedProgress) {
    const {
      flashcards: savedFlashcards,
      currentFlashcard: savedCurrentFlashcard,
    } = JSON.parse(savedProgress);
    flashcards = savedFlashcards || [];
    currentFlashcard = savedCurrentFlashcard || 1;
    updateFlashcardLabel();
  }
}

function clearProgress() {
  localStorage.removeItem("flashcardProgress");
  flashcards = [];
  currentFlashcard = 1;
  updateFlashcardLabel();
  alert("Progress cleared successfully!");
}

function clearInputFields() {
  document.getElementById("word").value = "";
  document.getElementById("definition").value = "";
  document.getElementById("example1").value = "";
  document.getElementById("example2").value = "";
  document.getElementById("pronunciation").value = "";
}
