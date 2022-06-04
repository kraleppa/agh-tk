export const isArchivePath = (path) => {
  const archiveTypes = ["zip", "tar", "gz"];
  return archiveTypes.includes(path.split(".").pop());
};

const parseState = (fileState) => {
  let parsedState;
  if (fileState.phraseFound != null) {
    !!fileState.phraseFound
      ? (parsedState = "PHRASE_FOUND")
      : (parsedState = "PHRASE_NOT_FOUND");
  } else if (fileState.fileProcessed != null) {
    parsedState = "PROCESSED";
  } else if (fileState.fileProcessingError != null) {
    parsedState = "ERROR";
  } else {
    parsedState = "PROCESSING";
  }
  return parsedState;
};

export const parseResult = (result) => {
  const resultParsed = {
    originalFile: "",
    fileState: {
      fileFound: result.fileState?.fileFound,
      fileProcessed: result.fileState?.fileProcessed,
      fileProcessingError: result.fileState?.fileProcessingError,
      phraseFound: result.found,
    },
    parsedFileState: "",
  };

  resultParsed.parsedFileState = parseState(resultParsed.fileState);

  if (!!result.video) {
    resultParsed.originalFile = result.originalFile
      ? result.originalFile
      : result.file;
  } else if (!!result.archive) {
    resultParsed.originalFile = result.archive.filePathInArchive;
  } else {
    resultParsed.originalFile = result.file;
  }

  resultParsed.text = result.text;
  resultParsed.words = result.words;

  return resultParsed;
};

//function checking if result should be replaced
//based on if its state change is valid
export const resultShouldBeReplaced = (oldResult, newResult) => {
  //valid state changes
  const oldProcessingNewAny = oldResult.parsedFileState === "PROCESSING";
  const oldProcessedNewPhraseFoundOrNotFound =
    oldResult.parsedFileState === "PROCESSED" &&
    (newResult.parsedFileState === "PHRASE_FOUND" ||
      newResult.parsedFileState === "PHRASE_NOT_FOUND");
  const oldAnyNewPhraseFound = newResult.parsedFileState === "PHRASE_FOUND";
  const oldAnyNewError = newResult.parsedFileState === "ERROR";

  return (
    oldProcessingNewAny ||
    oldProcessedNewPhraseFoundOrNotFound ||
    oldAnyNewPhraseFound ||
    oldAnyNewError
  );
};

export const sendRequest = (client, phrase, path, fileTypes, searchModes, languages) => {
  const message = {
    phrase: phrase,
    path: path.replace(/\\/g, "/"),
    filters: {
      fileTypes: fileTypes,
      searchModes: [...searchModes, "scraper"],
    },
    words: phrase.split(" "),
    languages
  };

  const destination = "/exchange/words/words." + message.filters.searchModes[0];
  const stringMessage = JSON.stringify(message);

  console.info("Sending message: " + stringMessage);

  client.publish({
    destination: destination,
    body: stringMessage,
    headers: {},
  });
};
