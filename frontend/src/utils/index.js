export const isArchivePath = (path) => {
  const archiveTypes = ["zip", "tar", "gz"];
  return archiveTypes.includes(path.split(".").pop());
};

export const parseResult = (result) => {
  const resultParsed = {
    originalFile: "",
    fileState: {
      fileFound: result.fileState?.fileFound,
      fileProcessed: result.fileState?.fileProcessed,
      phraseFound: result.found,
    },
  };
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
