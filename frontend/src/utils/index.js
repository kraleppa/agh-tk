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
    parsedState = "FILE_PROCESSED";
  } else if (fileState.fileProcessingError != null) {
    parsedState = "FILE_ERROR";
  } else {
    parsedState = "FILE_PROCESSING";
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

  return resultParsed;
};

export const resultShouldBeReplaced = (oldResult, newResult) => {
  //file found -> file processed -> phrase found true/false

  // return false if the phrase was found for the oldResult, and for newResult it was not
  // checked to handle the video which consists of many frames that are being sent to frontend
  if (
    newResult.fileState?.phraseFound != null &&
    !newResult.fileState?.phraseFound &&
    oldResult.fileState?.phraseFound != null &&
    !!oldResult.fileState?.phraseFound
  ) {
    return false;
  }
  return true;
};

export const sendRequest = (client, phrase, path, fileTypes, searchModes) => {
  const message = {
    phrase: phrase,
    path: path.replace(/\\/g, "/"),
    filters: {
      fileTypes: fileTypes,
      searchModes: [...searchModes, "scraper"],
    },
    words: phrase.split(" "),
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
